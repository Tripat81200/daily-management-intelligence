from src.ai.analyst import ManagementIntelligenceAnalyst, generate_tailored_story_analysis
from src.ai.concepts import get_concept_for_category
from src.newsletter.generator import NewsletterGenerator
from src.news.ranking import StoryRanker
from src.utils.history import HistoryTracker


def test_no_empty_sections_and_concept_injection():
    cfg = {
        "ranking": {"weights": {}, "threshold_min_score": 0.1},
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
    # Test with empty candidates: every section should receive a concept and not be empty!
    ranker = StoryRanker(cfg, HistoryTracker())
    sections = ranker.filter_and_rank([])

    for cat in ["operations", "marketing", "strategy_finance", "tech_ai", "india_business", "global_business"]:
        assert len(sections[cat]) >= 1
        assert "[" in sections[cat][0]["title"] or "[" in sections[cat][0]["headline"]


def test_story_specific_unique_analysis():
    story1 = {
        "title": "Paramount Skydance completes $110 billion Warner Bros merger",
        "summary": "Major media deal closed."
    }
    story2 = {
        "title": "Dario Amodei earned $18 million as Anthropic CEO with stock grants",
        "summary": "Executive compensation package revealed."
    }

    analysis1 = generate_tailored_story_analysis(story1, "top_5", 1)
    analysis2 = generate_tailored_story_analysis(story2, "top_5", 2)

    # Analyses must NOT be the same boilerplate!
    assert analysis1["why_it_matters"] != analysis2["why_it_matters"]
    assert analysis1["management_takeaway"] != analysis2["management_takeaway"]
    assert "merger" in analysis1["why_it_matters"].lower() or "consolidation" in analysis1["why_it_matters"].lower()
    assert "principal-agent" in analysis2["why_it_matters"].lower() or "compensation" in analysis2["why_it_matters"].lower()


def test_dark_mode_support_in_html():
    cfg = {
        "edition": {
            "name": "Daily Management Intelligence",
            "tagline": "Executive Briefing for MBA Leaders",
            "reading_time_minutes": 10,
            "timezone": "Asia/Kolkata"
        }
    }
    generator = NewsletterGenerator(cfg)
    mock_data = {
        "big_picture": "Test big picture",
        "top_5": [],
        "operations": [],
        "marketing": [],
        "strategy_finance": [],
        "tech_ai": [],
        "india_business": [],
        "global_business": [],
        "lesson_of_the_day": {"title": "Test", "explanation": "Test explanation"},
        "sixty_second_scan": []
    }
    _, html, _ = generator.generate(mock_data)
    assert 'prefers-color-scheme: dark' in html
    assert 'color-scheme' in html
    assert '[data-ogsc]' in html
