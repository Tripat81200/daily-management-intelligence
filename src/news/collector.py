import re
import html
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import feedparser
import requests
from dateutil import parser as date_parser

from src.news.sources import build_google_news_rss, DEFAULT_SEARCH_QUERIES, DIRECT_RSS_FEEDS

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


def strip_html_tags(text: str) -> str:
    """Clean raw HTML snippets down to clean text."""
    if not text:
        return ""
    text = html.unescape(text)
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse various RSS date formats to UTC datetime."""
    if not date_str:
        return None
    try:
        dt = date_parser.parse(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt
    except Exception:
        return None


class NewsCollector:
    """Collects business news from RSS feeds and Google News topic queries."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.news_cfg = config.get("news_sources", {})
        self.max_age_hours = self.news_cfg.get("max_age_hours", 36)
        self.exclude_keywords = [
            k.lower() for k in config.get("filters", {}).get("exclude_keywords", [])
        ]

    def _fetch_feed(self, url: str) -> Optional[feedparser.FeedParserDict]:
        try:
            headers = {"User-Agent": USER_AGENT}
            resp = requests.get(url, headers=headers, timeout=12)
            if resp.status_code == 200:
                return feedparser.parse(resp.content)
            else:
                logger.warning(f"HTTP {resp.status_code} fetching feed: {url}")
                return None
        except Exception as e:
            logger.warning(f"Error fetching feed {url}: {e}")
            return None

    def _is_noisy(self, title: str, summary: str) -> bool:
        """Filter out clickbait, sports, gossip, and non-business items."""
        full_text = f"{title} {summary}".lower()
        for kw in self.exclude_keywords:
            if kw in full_text:
                return True
        return False

    def collect_all_candidates(self) -> List[Dict[str, Any]]:
        """Fetch candidates across all categories and direct feeds."""
        candidates: List[Dict[str, Any]] = []
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=self.max_age_hours)

        # 1. Direct RSS feeds
        direct_feeds = self.news_cfg.get("direct_rss_feeds", DIRECT_RSS_FEEDS)
        for feed in direct_feeds:
            name = feed.get("name", "Direct Feed")
            category = feed.get("category", "general")
            weight = feed.get("weight", 1.0)
            url = feed.get("url")
            if not url:
                continue

            parsed = self._fetch_feed(url)
            if not parsed or not parsed.entries:
                continue

            for entry in parsed.entries[:15]:
                title = strip_html_tags(entry.get("title", ""))
                summary = strip_html_tags(entry.get("summary", entry.get("description", "")))
                link = entry.get("link", "")
                pub_date_str = entry.get("published", entry.get("pubDate"))
                dt = parse_date(pub_date_str) or now

                if dt < cutoff:
                    continue
                if self._is_noisy(title, summary):
                    continue

                candidates.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "source": name,
                    "published_at": dt.isoformat(),
                    "category": category,
                    "weight_multiplier": weight,
                    "feed_type": "direct_rss"
                })

        # 2. Google News targeted queries
        configured_queries = self.news_cfg.get("google_news_queries")
        queries_to_run = configured_queries if configured_queries else DEFAULT_SEARCH_QUERIES

        for category, query_list in queries_to_run.items():
            for item in query_list:
                if isinstance(item, tuple) or isinstance(item, list):
                    q, region = item[0], item[1]
                else:
                    q = item
                    region = "IN" if "india" in category else "US"

                hl = "en-IN" if region == "IN" else "en-US"
                ceid = f"{region}:en"
                url = build_google_news_rss(q, gl=region, hl=hl, ceid=ceid)

                parsed = self._fetch_feed(url)
                if not parsed or not parsed.entries:
                    continue

                for entry in parsed.entries[:12]:
                    title = strip_html_tags(entry.get("title", ""))
                    summary = strip_html_tags(entry.get("summary", ""))
                    link = entry.get("link", "")
                    
                    # Extract source if Google News appends "- Publisher"
                    source_name = "Google News"
                    if " - " in title:
                        parts = title.rsplit(" - ", 1)
                        if len(parts) == 2 and len(parts[1]) < 30:
                            title = parts[0]
                            source_name = parts[1]
                    elif entry.get("source", {}).get("title"):
                        source_name = entry["source"]["title"]

                    pub_date_str = entry.get("published", entry.get("pubDate"))
                    dt = parse_date(pub_date_str) or now

                    if dt < cutoff:
                        continue
                    if self._is_noisy(title, summary):
                        continue

                    candidates.append({
                        "title": title,
                        "summary": summary,
                        "url": link,
                        "source": source_name,
                        "published_at": dt.isoformat(),
                        "category": category,
                        "weight_multiplier": 1.1 if region == "IN" else 1.0,
                        "feed_type": "google_news"
                    })

        logger.info(f"Total raw candidates collected: {len(candidates)}")
        return candidates
