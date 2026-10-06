import json
import re
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_HISTORY_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "history" / "sent_stories.json"


def normalize_title(title: str) -> str:
    """Normalize headline for comparison by lowercasing and removing punctuation/stopwords."""
    title = title.lower()
    # Remove common publisher suffixes like ' - Reuters', ' | Bloomberg'
    title = re.sub(r"[\-|]\s*[A-Za-z0-9\.\s]+$", "", title).strip()
    # Remove non-alphanumeric characters
    tokens = re.findall(r"\b[a-z0-9]{3,}\b", title)
    stopwords = {
        "the", "and", "for", "with", "from", "that", "this", "have", "are",
        "has", "will", "its", "say", "says", "said", "after", "into", "over",
        "more", "news", "report", "reports", "today", "live", "amid"
    }
    filtered = [t for t in tokens if t not in stopwords]
    return " ".join(filtered)


def calculate_similarity(t1: str, t2: str) -> float:
    """Jaccard similarity between two normalized strings."""
    s1 = set(normalize_title(t1).split())
    s2 = set(normalize_title(t2).split())
    if not s1 or not s2:
        return 0.0
    intersection = len(s1.intersection(s2))
    union = len(s1.union(s2))
    return intersection / union if union > 0 else 0.0


class HistoryTracker:
    """Tracks sent stories across workflow executions to prevent duplicate coverage."""

    def __init__(self, history_file: Path = DEFAULT_HISTORY_FILE, retention_days: int = 14):
        self.history_file = history_file
        self.retention_days = retention_days
        self.records: List[Dict[str, Any]] = self._load()

    def _load(self) -> List[Dict[str, Any]]:
        if not self.history_file.exists():
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "stories" in data:
                    return data["stories"]
                return []
        except Exception as e:
            logger.warning(f"Failed to read history file {self.history_file}: {e}")
            return []

    def save(self) -> None:
        """Prune old stories and save history."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=self.retention_days)

        pruned = []
        for r in self.records:
            sent_at = r.get("sent_at")
            if sent_at:
                try:
                    dt = datetime.fromisoformat(sent_at)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    if dt >= cutoff:
                        pruned.append(r)
                except Exception:
                    pruned.append(r)
            else:
                pruned.append(r)

        self.records = pruned
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.records, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.records)} history records to {self.history_file}")
        except Exception as e:
            logger.error(f"Failed to write history file: {e}")

    def is_duplicate(self, title: str, url: str = "", threshold: float = 0.55) -> bool:
        """Check if article was already reported recently."""
        norm_title = normalize_title(title)
        clean_url = url.split("?")[0].rstrip("/") if url else ""

        for r in self.records:
            # Direct URL match
            rec_url = r.get("url", "").split("?")[0].rstrip("/")
            if clean_url and rec_url and clean_url == rec_url:
                return True

            # Headline similarity
            rec_title = r.get("title", "")
            if calculate_similarity(norm_title, rec_title) >= threshold:
                return True

        return False

    def record_stories(self, stories: List[Dict[str, Any]]) -> None:
        """Add newly sent stories to history."""
        now_iso = datetime.now(timezone.utc).isoformat()
        for s in stories:
            title = s.get("title", "")
            url = s.get("url", "")
            if not title:
                continue
            self.records.append({
                "title": title,
                "url": url,
                "category": s.get("category", "general"),
                "sent_at": now_iso
            })
        self.save()
