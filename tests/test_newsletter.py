from src.newsletter.generator import NewsletterGenerator


def test_newsletter_html_generation():
    cfg = {
        "edition": {
            "name": "Daily Management Intelligence",
            "tagline": "Executive Briefing for MBA Leaders",
            "reading_time_minutes": 10,
            "timezone": "Asia/Kolkata"
        }
    }
    generator = NewsletterGenerator(cfg)
    mock_intelligence = {
        "big_picture": "Macro economic conditions tighten across supply chains.",
        "top_5": [
            {
                "headline": "Foxconn and Tata Expand Semiconductor Packaging Operations",
                "what_happened": "Major capacity addition underway in India.",
                "why_it_matters": "De-risks global supply chains from single-country exposure.",
                "management_takeaway": "Operational resilience requires diversified geographic footprint.",
                "competitive_advantage": "Early movers capture subsidized capital and favorable tax structures.",
                "source_name": "Reuters",
                "source_url": "https://reuters.com/mock"
            }
        ],
        "operations": [
            {
                "headline": "Amazon Redesigns Regional Fulfillment Hubs",
                "what_happened": "Shifting inventory closer to consumers.",
                "why_it_matters_operationally": "Lowers middle-mile transport costs and transit times.",
                "operational_lesson": "Decentralized warehousing trades holding costs for transportation savings.",
                "source_name": "Supply Chain Brain",
                "source_url": "https://supplychainbrain.com/mock"
            }
        ],
        "marketing": [
            {
                "headline": "Nike Pivots Strategy Back to Wholesale Distribution",
                "what_happened": "Re-establishing relationships with department stores.",
                "why_it_matters_marketing": "D2C customer acquisition costs exceeded projected margins.",
                "marketing_lesson": "Omnichannel distribution provides higher customer reach than purely digital acquisition.",
                "source_name": "Marketing Dive",
                "source_url": "https://marketingdive.com/mock"
            }
        ],
        "strategy_finance": [
            {
                "headline": "Private Equity Megadeals Slow as Borrowing Costs Persist",
                "what_happened": "Leveraged buyout volumes contracted 15%.",
                "strategic_takeaway": "Organic growth models outperform debt-funded rollups.",
                "source_name": "CNBC",
                "source_url": "https://cnbc.com/mock"
            }
        ],
        "tech_ai": [
            {
                "headline": "Enterprise Software Vendors Bundle Autonomous Agents",
                "what_happened": "ERP providers integrate agentic workflows.",
                "business_implication": "Moves from seat-based licensing to consumption/outcome pricing.",
                "source_name": "Tech Review",
                "source_url": "https://tech.com/mock"
            }
        ],
        "india_business": [
            {
                "headline": "UPI Cross-Border Remittances Cross New Record",
                "what_happened": "Digital payments footprint deepens.",
                "india_market_insight": "Fintech infrastructure creates structural operational efficiencies.",
                "source_name": "Livemint",
                "source_url": "https://livemint.com/mock"
            }
        ],
        "global_business": [
            {
                "headline": "EU Approves Stricter ESG Supply Chain Due Diligence Rules",
                "what_happened": "Mandates audit of Tier 1 and Tier 2 suppliers.",
                "macro_impact": "Raises compliance costs for multinational procurement organizations.",
                "source_name": "Financial Times",
                "source_url": "https://ft.com/mock"
            }
        ],
        "lesson_of_the_day": {
            "title": "The Bullwhip Effect in Volatile Demand Cycles",
            "explanation": "Small shifts in retail demand amplify into massive swings up the supply chain. Managers must share POS data directly with tier-1 suppliers to avoid inventory whiplash."
        },
        "sixty_second_scan": [
            {"pillar": "Operations", "takeaway": "Amazon regionalizes inventory"},
            {"pillar": "Marketing", "takeaway": "Nike balances wholesale and D2C"}
        ]
    }

    subject, html_body, plain_text = generator.generate(mock_intelligence)
    assert "Daily Management Intelligence" in subject or "Executive Briefing" in subject
    assert "Foxconn and Tata Expand Semiconductor" in html_body
    assert "The Bullwhip Effect in Volatile Demand Cycles" in html_body
    assert "Nike Pivots Strategy" in plain_text
    assert "Decentralized warehousing" in html_body
