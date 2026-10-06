from datetime import datetime, timezone
from src.news.collector import strip_html_tags, parse_date, NewsCollector


def test_strip_html_tags():
    raw = "<p>This is a <b>major</b> supply chain story.<br><a href='https://example.com'>Read more</a></p>"
    clean = strip_html_tags(raw)
    assert clean == "This is a major supply chain story. Read more"


def test_parse_date():
    date_str = "Tue, 06 Oct 2026 14:30:00 GMT"
    dt = parse_date(date_str)
    assert dt is not None
    assert dt.tzinfo is not None
    assert dt.year == 2026
    assert dt.month == 10


def test_noise_filtering():
    cfg = {
        "filters": {
            "exclude_keywords": ["horoscope", "cricket score", "celebrity gossip"]
        }
    }
    collector = NewsCollector(cfg)
    assert collector._is_noisy("Today's Daily Horoscope", "Find out what stars say") is True
    assert collector._is_noisy("IPL Cricket Score Update", "Match highlights") is True
    assert collector._is_noisy("Foxconn Expands Factory Operations", "New industrial plant in Tamil Nadu") is False
