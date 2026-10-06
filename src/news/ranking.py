import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
from src.utils.history import HistoryTracker, calculate_similarity

logger = logging.getLogger(__name__)

# Keywords associated with specific managerial dimensions
KEYWORD_MAP = {
    "business_impact": [
        "revenue", "profit", "billion", "trillion", "million", "market cap", "shares",
        "earnings", "acquisition", "merger", "regulatory", "penalty", "valuation",
        "ipo", "layoffs", "expansion", "investment", "deal", "bankruptcy"
    ],
    "management_relevance": [
        "strategy", "ceo", "leadership", "decision", "restructuring", "governance",
        "workforce", "talent", "culture", "operating model", "transformation",
        "board", "risk management", "crisis", "executive"
    ],
    "operations_relevance": [
        "supply chain", "logistics", "manufacturing", "procurement", "inventory",
        "warehousing", "distribution", "last-mile", "automation", "robotics",
        "factory", "capacity", "cost reduction", "plant", "pli", "reshoring",
        "nearshoring", "freight", "shipping", "chipmaker", "semiconductor", "foxconn"
    ],
    "marketing_relevance": [
        "brand", "customer", "advertising", "campaign", "pricing", "consumer",
        "cac", "ltv", "retention", "d2c", "e-commerce", "retail", "influencer",
        "social media", "market share", "gen z", "positioning", "adtech", "launch"
    ],
    "strategic_importance": [
        "competitive advantage", "moat", "market entry", "partnership", "pivot",
        "monopoly", "antitrust", "diversification", "vertical integration", "jv",
        "joint venture", "long-term", "synergy"
    ]
}

TIER_1_SOURCES = {
    "reuters", "bloomberg", "financial times", "wall street journal", "wsj",
    "cnbc", "the economist", "harvard business review", "hbr", "livemint",
    "economic times", "business standard", "techcrunch", "supply chain brain",
    "marketing dive", "forbes", "fortune"
}


class StoryRanker:
    """Scores, deduplicates, and organizes candidate stories for executive analysis."""

    def __init__(self, config: Dict[str, Any], history_tracker: HistoryTracker):
        self.config = config
        self.history_tracker = history_tracker
        self.weights = config.get("ranking", {}).get("weights", {
            "business_impact": 0.25,
            "management_relevance": 0.20,
            "operations_relevance": 0.15,
            "marketing_relevance": 0.15,
            "strategic_importance": 0.10,
            "recency": 0.10,
            "novelty": 0.05
        })
        self.min_score = config.get("ranking", {}).get("threshold_min_score", 0.30)

    def _score_text_dimension(self, text: str, keywords: List[str]) -> float:
        """Count keyword hits normalized to a 0.0 - 1.0 scale."""
        text_lower = text.lower()
        hits = sum(1 for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", text_lower))
        return min(hits / 3.0, 1.0)

    def _score_recency(self, published_at_str: str) -> float:
        """Score based on how fresh the article is within the last 48 hours."""
        try:
            pub_dt = datetime.fromisoformat(published_at_str)
            now = datetime.now(timezone.utc)
            hours_old = max(0.0, (now - pub_dt).total_seconds() / 3600.0)
            if hours_old <= 6:
                return 1.0
            elif hours_old <= 12:
                return 0.85
            elif hours_old <= 24:
                return 0.70
            elif hours_old <= 36:
                return 0.50
            return 0.30
        except Exception:
            return 0.50

    def _score_source_credibility(self, source_name: str) -> float:
        src_clean = source_name.lower()
        for t1 in TIER_1_SOURCES:
            if t1 in src_clean:
                return 1.0
        return 0.70

    def score_story(self, story: Dict[str, Any]) -> float:
        """Calculate composite weighted score for a single candidate."""
        combined_text = f"{story.get('title', '')} {story.get('summary', '')}"

        biz_impact = self._score_text_dimension(combined_text, KEYWORD_MAP["business_impact"])
        mgmt_rel = self._score_text_dimension(combined_text, KEYWORD_MAP["management_relevance"])
        ops_rel = self._score_text_dimension(combined_text, KEYWORD_MAP["operations_relevance"])
        mkt_rel = self._score_text_dimension(combined_text, KEYWORD_MAP["marketing_relevance"])
        strat_imp = self._score_text_dimension(combined_text, KEYWORD_MAP["strategic_importance"])
        recency = self._score_recency(story.get("published_at", ""))
        novelty = self._score_source_credibility(story.get("source", ""))

        # Boost by category relevance if the article came from a targeted query
        cat = story.get("category", "")
        if cat == "operations":
            ops_rel = max(ops_rel, 0.75)
        elif cat == "marketing":
            mkt_rel = max(mkt_rel, 0.75)

        raw_score = (
            biz_impact * self.weights.get("business_impact", 0.25) +
            mgmt_rel * self.weights.get("management_relevance", 0.20) +
            ops_rel * self.weights.get("operations_relevance", 0.15) +
            mkt_rel * self.weights.get("marketing_relevance", 0.15) +
            strat_imp * self.weights.get("strategic_importance", 0.10) +
            recency * self.weights.get("recency", 0.10) +
            novelty * self.weights.get("novelty", 0.05)
        )

        final_score = raw_score * story.get("weight_multiplier", 1.0)
        return round(final_score, 4)

    def filter_and_rank(self, candidates: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Deduplicate against history and within batch, score, and group by category."""
        # Step 1: Filter out items already sent in previous days
        new_candidates: List[Dict[str, Any]] = []
        for c in candidates:
            if not self.history_tracker.is_duplicate(c.get("title", ""), c.get("url", "")):
                new_candidates.append(c)

        # Step 2: Score candidates
        scored_list: List[Dict[str, Any]] = []
        for c in new_candidates:
            s_score = self.score_story(c)
            if s_score >= self.min_score:
                item = dict(c)
                item["score"] = s_score
                scored_list.append(item)

        # Step 3: Sort by score descending
        scored_list.sort(key=lambda x: x["score"], reverse=True)

        # Step 4: Intra-batch deduplication (keep highest scoring variant)
        deduped: List[Dict[str, Any]] = []
        for s in scored_list:
            is_dup = False
            for existing in deduped:
                if calculate_similarity(s["title"], existing["title"]) > 0.45:
                    is_dup = True
                    break
            if not is_dup:
                deduped.append(s)

        logger.info(f"Filtered {len(candidates)} candidates down to {len(deduped)} high-signal unique stories.")

        # Step 5: Distribute into designated newsletter sections
        content_cfg = self.config.get("content", {})
        top_n = content_cfg.get("top_stories_count", 5)
        ops_n = content_cfg.get("operations_stories_count", 3)
        mkt_n = content_cfg.get("marketing_stories_count", 3)
        strat_n = content_cfg.get("strategy_finance_stories_count", 3)
        tech_n = content_cfg.get("tech_ai_stories_count", 2)
        india_n = content_cfg.get("india_business_stories_count", 3)
        global_n = content_cfg.get("global_business_stories_count", 2)

        # Select Top 5 first (highest scoring overall)
        top_5 = deduped[:top_n]
        remaining = deduped[top_n:]

        # Bucketing helper
        def extract_for_category(category_name: str, count: int, fallback_keywords: List[str]) -> List[Dict[str, Any]]:
            picked = []
            nonlocal remaining
            # First pick explicit category matches
            for item in list(remaining):
                if item.get("category") == category_name and len(picked) < count:
                    picked.append(item)
                    remaining.remove(item)

            # Second pick keyword matches if quota not met
            if len(picked) < count and fallback_keywords:
                for item in list(remaining):
                    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
                    if any(kw in text for kw in fallback_keywords) and len(picked) < count:
                        picked.append(item)
                        remaining.remove(item)

            return picked

        operations = extract_for_category("operations", ops_n, KEYWORD_MAP["operations_relevance"][:6])
        marketing = extract_for_category("marketing", mkt_n, KEYWORD_MAP["marketing_relevance"][:6])
        strategy_finance = extract_for_category("strategy_finance", strat_n, KEYWORD_MAP["strategic_importance"][:4])
        tech_ai = extract_for_category("tech_ai", tech_n, ["ai", "software", "cloud", "automation", "tech"])
        india_business = extract_for_category("india_business", india_n, ["india", "indian", "rbi", "bse", "nifty"])
        global_business = extract_for_category("global_business", global_n, ["us", "europe", "china", "global", "fed"])

        # If any section is empty, backfill from remaining high-scoring pool if possible
        def backfill_if_needed(section_list: List[Dict[str, Any]], target: int, cat_label: str):
            nonlocal remaining
            while len(section_list) < min(target, 2) and remaining:
                item = remaining.pop(0)
                item["category"] = cat_label
                section_list.append(item)

        backfill_if_needed(operations, ops_n, "operations")
        backfill_if_needed(marketing, mkt_n, "marketing")
        backfill_if_needed(strategy_finance, strat_n, "strategy_finance")
        backfill_if_needed(tech_ai, tech_n, "tech_ai")
        backfill_if_needed(india_business, india_n, "india_business")
        backfill_if_needed(global_business, global_n, "global_business")

        return {
            "top_5": top_5,
            "operations": operations,
            "marketing": marketing,
            "strategy_finance": strategy_finance,
            "tech_ai": tech_ai,
            "india_business": india_business,
            "global_business": global_business
        }
