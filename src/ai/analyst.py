import json
import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Dict, Any, List

from src.ai.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.ai.client import AIClient

logger = logging.getLogger(__name__)


def create_offline_fallback_intelligence(ranked_sections: Dict[str, List[Dict[str, Any]]], current_date: str) -> Dict[str, Any]:
    """Generate high-quality rule-based fallback if AI API key is not yet configured or temporarily unavailable."""
    top_5 = []
    for s in ranked_sections.get("top_5", [])[:5]:
        top_5.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Key strategic business development reported.",
            "why_it_matters": "Demonstrates evolving market dynamics and reallocation of corporate capital in response to shifting industry demand.",
            "management_takeaway": "Leaders must continuously stress-test unit economics and operational flexibility against structural industry shifts.",
            "competitive_advantage": "Organizations adapting supply networks early capture first-mover margin advantages.",
            "source_name": s.get("source", "Business Wire"),
            "source_url": s.get("url", "#")
        })

    operations = []
    for s in ranked_sections.get("operations", [])[:3]:
        operations.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Operational expansion and supply chain realignment.",
            "why_it_matters_operationally": "Directly impacts delivery lead times, buffer inventory levels, and logistics cost structures.",
            "operational_lesson": "Decentralized warehousing and process automation mitigate single-point supply chain bottlenecks.",
            "source_name": s.get("source", "Supply Chain Intelligence"),
            "source_url": s.get("url", "#")
        })

    marketing = []
    for s in ranked_sections.get("marketing", [])[:3]:
        marketing.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Customer positioning and brand campaign development.",
            "why_it_matters_marketing": "Reflects shifting consumer acquisition strategies and customer lifetime value optimization.",
            "marketing_lesson": "Sustainable brand moats depend on organic retention and community trust rather than ad-spend arbitrage.",
            "source_name": s.get("source", "Marketing Intelligence"),
            "source_url": s.get("url", "#")
        })

    strategy_finance = []
    for s in ranked_sections.get("strategy_finance", [])[:3]:
        strategy_finance.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Corporate finance or M&A transaction.",
            "strategic_takeaway": "Prudent balance sheet management and capital discipline outweigh speculative growth.",
            "source_name": s.get("source", "Financial Review"),
            "source_url": s.get("url", "#")
        })

    tech_ai = []
    for s in ranked_sections.get("tech_ai", [])[:2]:
        tech_ai.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Enterprise technology deployment.",
            "business_implication": "Companies moving from experimental AI proofs-of-concept to measured workflow automation unlock measurable EBITDA gains.",
            "source_name": s.get("source", "Enterprise Tech"),
            "source_url": s.get("url", "#")
        })

    global_business = []
    for s in ranked_sections.get("global_business", [])[:2]:
        global_business.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "International market shift.",
            "macro_impact": "Cross-border supply chains face evolving regulatory and geopolitical realignments.",
            "source_name": s.get("source", "Global Bureau"),
            "source_url": s.get("url", "#")
        })

    india_business = []
    for s in ranked_sections.get("india_business", [])[:3]:
        india_business.append({
            "headline": s.get("title", ""),
            "what_happened": s.get("summary", "") or "Indian corporate and regulatory milestone.",
            "india_market_insight": "India's domestic consumption resilience and manufacturing policy incentives continue driving capacity additions.",
            "source_name": s.get("source", "India Bureau"),
            "source_url": s.get("url", "#")
        })

    return {
        "big_picture": (
            "Global business leaders are navigating tightening capital cycles and supply-chain reconfiguration. "
            "Corporate strategy is decisively pivoting toward operational resilience, cost predictability, "
            "and disciplined customer acquisition, with India emerging as a pivotal growth and manufacturing hub."
        ),
        "top_5": top_5,
        "operations": operations,
        "marketing": marketing,
        "strategy_finance": strategy_finance,
        "tech_ai": tech_ai,
        "global_business": global_business,
        "india_business": india_business,
        "lesson_of_the_day": {
            "title": "Operational Resilience as a Strategic Competitive Moat",
            "explanation": (
                "Historically, operational efficiency focused narrowly on just-in-time inventory and lowest-cost sourcing. "
                "Today, top-tier management treats buffer capacity, multisourcing, and regional logistics as competitive moats. "
                "When supply shocks occur, firms with resilient operations maintain fulfillment while competitors stall."
            )
        },
        "sixty_second_scan": [
            {"pillar": "Operations", "takeaway": "Logistics networks shifting to regional fulfillment nodes"},
            {"pillar": "Marketing", "takeaway": "Brands shifting spend toward retention and zero-party customer data"},
            {"pillar": "Strategy", "takeaway": "Corporates rationalizing non-core assets to fund strategic tech upgrades"},
            {"pillar": "Finance", "takeaway": "Disciplined margin management replaces debt-funded customer acquisition"},
            {"pillar": "Technology", "takeaway": "Enterprise AI spending refocuses on measurable operational ROI"},
            {"pillar": "India", "takeaway": "Domestic manufacturing incentives accelerate industrial CAPEX"}
        ]
    }


class ManagementIntelligenceAnalyst:
    """Orchestrates candidate synthesis into executive intelligence."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ai_client = AIClient(config)

    def analyze(self, ranked_sections: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Synthesize candidate stories into the complete briefing."""
        # Get formatted date in configured timezone (default Asia/Kolkata)
        tz_name = self.config.get("edition", {}).get("timezone", "Asia/Kolkata")
        try:
            tz = ZoneInfo(tz_name)
        except Exception:
            tz = timezone.utc

        now_local = datetime.now(tz)
        formatted_date = now_local.strftime("%A, %B %d, %Y")

        # Prepare trimmed JSON representation of candidates to save tokens while providing full facts
        curated_for_prompt = {}
        for section, stories in ranked_sections.items():
            curated_for_prompt[section] = [
                {
                    "title": s.get("title"),
                    "summary": s.get("summary")[:300] if s.get("summary") else "",
                    "source": s.get("source"),
                    "url": s.get("url")
                }
                for s in stories
            ]

        user_prompt = USER_PROMPT_TEMPLATE.format(
            current_date=formatted_date,
            curated_stories_json=json.dumps(curated_for_prompt, indent=2)
        )

        try:
            logger.info("Calling AI analyst for executive intelligence synthesis...")
            intel = self.ai_client.generate_intelligence(SYSTEM_PROMPT, user_prompt)
            # Basic validation
            if not isinstance(intel, dict) or "top_5" not in intel:
                raise ValueError("AI returned invalid briefing structure.")
            logger.info("Successfully synthesized executive briefing via AI.")
            return intel
        except Exception as e:
            logger.error(f"AI synthesis failed: {e}. Generating offline fallback briefing.")
            return create_offline_fallback_intelligence(ranked_sections, formatted_date)
