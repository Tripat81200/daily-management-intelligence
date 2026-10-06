import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Dict, Any, Tuple
from jinja2 import Template

from src.newsletter.template import HTML_TEMPLATE

logger = logging.getLogger(__name__)


def generate_plain_text(data: Dict[str, Any], date_str: str) -> str:
    """Generate a clean plain-text fallback version of the executive newsletter."""
    lines = [
        f"DAILY MANAGEMENT INTELLIGENCE — {date_str}",
        "=" * 50,
        "",
        "TODAY'S BIG PICTURE:",
        data.get("big_picture", ""),
        "",
        "🔥 TOP 5 — MUST KNOW",
        "-" * 30
    ]

    for idx, item in enumerate(data.get("top_5", []), 1):
        lines.append(f"{idx}. {item.get('headline')}")
        lines.append(f"What happened: {item.get('what_happened')}")
        lines.append(f"Why it matters: {item.get('why_it_matters')}")
        lines.append(f"Management takeaway: {item.get('management_takeaway')}")
        if item.get("competitive_advantage"):
            lines.append(f"Second-Order Implication: {item.get('competitive_advantage')}")
        lines.append(f"Source: {item.get('source_name')} ({item.get('source_url')})")
        lines.append("")

    lines.append("⚙️ OPERATIONS INTELLIGENCE")
    lines.append("-" * 30)
    for item in data.get("operations", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"What happened: {item.get('what_happened')}")
        lines.append(f"Operational impact: {item.get('why_it_matters_operationally')}")
        lines.append(f"Operational lesson: {item.get('operational_lesson')}")
        lines.append(f"Source: {item.get('source_name')} ({item.get('source_url')})")
        lines.append("")

    lines.append("📣 MARKETING INTELLIGENCE")
    lines.append("-" * 30)
    for item in data.get("marketing", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"What happened: {item.get('what_happened')}")
        lines.append(f"Marketing impact: {item.get('why_it_matters_marketing')}")
        lines.append(f"Marketing lesson: {item.get('marketing_lesson')}")
        lines.append(f"Source: {item.get('source_name')} ({item.get('source_url')})")
        lines.append("")

    lines.append("📊 STRATEGY & FINANCE")
    lines.append("-" * 30)
    for item in data.get("strategy_finance", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"Strategic takeaway: {item.get('strategic_takeaway')}")
        lines.append("")

    lines.append("🤖 TECHNOLOGY & AI")
    lines.append("-" * 30)
    for item in data.get("tech_ai", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"Business implication: {item.get('business_implication')}")
        lines.append("")

    lines.append("🇮🇳 INDIA BUSINESS")
    lines.append("-" * 30)
    for item in data.get("india_business", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"Market insight: {item.get('india_market_insight')}")
        lines.append("")

    lines.append("🌎 GLOBAL BUSINESS")
    lines.append("-" * 30)
    for item in data.get("global_business", []):
        lines.append(f"• {item.get('headline')}")
        lines.append(f"Macro impact: {item.get('macro_impact')}")
        lines.append("")

    lotd = data.get("lesson_of_the_day")
    if lotd:
        lines.append("🧠 THE MANAGEMENT LESSON OF THE DAY")
        lines.append("-" * 30)
        lines.append(lotd.get("title", ""))
        lines.append(lotd.get("explanation", ""))
        lines.append("")

    scans = data.get("sixty_second_scan", [])
    if scans:
        lines.append("⚡ 60-SECOND SCAN")
        lines.append("-" * 30)
        for s in scans:
            lines.append(f"[{s.get('pillar')}] {s.get('takeaway')}")
        lines.append("")

    lines.append("Sent via Daily Management Intelligence")
    return "\n".join(lines)


class NewsletterGenerator:
    """Renders executive email from synthesized intelligence data."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.edition_cfg = config.get("edition", {})
        self.template = Template(HTML_TEMPLATE)

    def generate(self, intelligence: Dict[str, Any]) -> Tuple[str, str, str]:
        """Generate (subject, html_body, plain_text_body)."""
        tz_name = self.edition_cfg.get("timezone", "Asia/Kolkata")
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            tz = timezone.utc

        now_local = datetime.now(tz)
        formatted_date = now_local.strftime("%A, %B %d, %Y")
        short_date = now_local.strftime("%b %d")

        subject = f"Executive Briefing: {short_date} - Daily Management Intelligence"

        context = {
            "edition_name": self.edition_cfg.get("name", "Daily Management Intelligence"),
            "tagline": self.edition_cfg.get("tagline", "Executive Briefing for MBA Leaders"),
            "reading_time_minutes": self.edition_cfg.get("reading_time_minutes", 10),
            "formatted_date": formatted_date,
            "big_picture": intelligence.get("big_picture", ""),
            "top_5": intelligence.get("top_5", []),
            "operations": intelligence.get("operations", []),
            "marketing": intelligence.get("marketing", []),
            "strategy_finance": intelligence.get("strategy_finance", []),
            "tech_ai": intelligence.get("tech_ai", []),
            "india_business": intelligence.get("india_business", []),
            "global_business": intelligence.get("global_business", []),
            "lesson_of_the_day": intelligence.get("lesson_of_the_day"),
            "sixty_second_scan": intelligence.get("sixty_second_scan", [])
        }

        html_body = self.template.render(**context)
        plain_text_body = generate_plain_text(intelligence, formatted_date)

        return subject, html_body, plain_text_body
