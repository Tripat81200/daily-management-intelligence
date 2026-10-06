import tempfile
from pathlib import Path
from src.utils.history import HistoryTracker, normalize_title, calculate_similarity
from src.news.ranking import StoryRanker


def test_normalize_title_and_similarity():
    t1 = "Tata Steel expands manufacturing operations in Odisha plant - Livemint"
    t2 = "Tata Steel expands manufacturing operations at Odisha facility"
    sim = calculate_similarity(t1, t2)
    assert sim > 0.5


def test_history_tracker():
    with tempfile.TemporaryDirectory() as tmpdir:
        hist_path = Path(tmpdir) / "test_history.json"
        tracker = HistoryTracker(history_file=hist_path, retention_days=7)
        assert tracker.is_duplicate("Apple launches new logistics hub in India") is False

        tracker.record_stories([{
            "title": "Apple launches new logistics hub in India",
            "url": "https://example.com/apple-hub",
            "category": "operations"
        }])
        assert tracker.is_duplicate("Apple launches new logistics hub in India") is True
        assert tracker.is_duplicate("Apple launches logistics center in India") is True


def test_story_ranker_scoring():
    with tempfile.TemporaryDirectory() as tmpdir:
        hist_path = Path(tmpdir) / "test_history.json"
        tracker = HistoryTracker(history_file=hist_path)
        cfg = {
            "ranking": {
                "weights": {
                    "business_impact": 0.25,
                    "management_relevance": 0.20,
                    "operations_relevance": 0.15,
                    "marketing_relevance": 0.15,
                    "strategic_importance": 0.10,
                    "recency": 0.10,
                    "novelty": 0.05
                },
                "threshold_min_score": 0.1
            },
            "content": {
                "top_stories_count": 2,
                "operations_stories_count": 1,
                "marketing_stories_count": 1,
                "strategy_finance_stories_count": 1,
                "tech_ai_stories_count": 1,
                "india_business_stories_count": 1,
                "global_business_stories_count": 1
            }
        }
        ranker = StoryRanker(cfg, tracker)
        story = {
            "title": "Reliance Retail announces $1B supply chain expansion and logistics automation",
            "summary": "Major investment to optimize warehouse capacity and lower delivery cost.",
            "url": "https://reuters.com/article1",
            "source": "Reuters",
            "published_at": "2026-10-06T12:00:00+00:00",
            "category": "operations",
            "weight_multiplier": 1.2
        }
        score = ranker.score_story(story)
        assert score > 0.4
