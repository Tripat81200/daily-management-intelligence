from typing import List, Dict, Any
import urllib.parse

def build_google_news_rss(query: str, gl: str = "IN", hl: str = "en-IN", ceid: str = "IN:en") -> str:
    """Build Google News RSS search URL with proper encoding."""
    encoded_query = urllib.parse.quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}&hl={hl}&gl={gl}&ceid={ceid}"


DEFAULT_SEARCH_QUERIES = {
    "operations": [
        ('("supply chain" OR logistics OR "freight rates" OR warehousing) when:2d', "IN"),
        ('("manufacturing operations" OR "industrial automation" OR "robotics in factory" OR "procurement strategy") when:2d', "US"),
        ('("India manufacturing" OR "PLI scheme" OR "Foxconn India" OR "semiconductor plant") when:2d', "IN"),
    ],
    "marketing": [
        ('("brand strategy" OR "customer acquisition cost" OR "consumer behavior" OR "D2C brand") when:2d', "IN"),
        ('("pricing strategy" OR "advertising campaign" OR "social commerce" OR "influencer marketing") when:2d', "US"),
        ('("Gen Z consumers" OR "customer retention" OR "retail media" OR "ad tech") when:2d', "US"),
    ],
    "strategy_finance": [
        ('("merger" OR "acquisition" OR "private equity" OR "venture capital" OR "corporate restructuring") when:2d', "US"),
        ('("interest rates" OR "GDP growth" OR "inflation rate" OR "quarterly results" OR "IPO") when:2d', "IN"),
    ],
    "tech_ai": [
        ('("enterprise AI" OR "generative AI adoption" OR "corporate AI deployment" OR "cloud spending") when:2d', "US"),
        ('("automation in business" OR "IT services" OR "SaaS pricing" OR "cybersecurity enterprise") when:2d', "US"),
    ],
    "india_business": [
        ('("Reserve Bank of India" OR "SEBI" OR "Tata Group" OR "Reliance Industries" OR "Adani Group") when:2d', "IN"),
        ('("quick commerce" OR "Blinkit" OR "Zepto" OR "Swiggy" OR "Zomato" OR "Flipkart" OR "Indian startup") when:2d', "IN"),
    ],
    "global_business": [
        ('("global trade" OR "tariffs" OR "Federal Reserve" OR "European Central Bank" OR "China economy") when:2d', "US"),
        ('("OPEC oil prices" OR "foreign exchange" OR "cross-border investment") when:2d', "US"),
    ]
}

DIRECT_RSS_FEEDS = [
    {
        "name": "LiveMint Companies",
        "url": "https://www.livemint.com/rss/companies",
        "category": "india_business",
        "weight": 1.25
    },
    {
        "name": "LiveMint Industry",
        "url": "https://www.livemint.com/rss/industry",
        "category": "operations",
        "weight": 1.25
    },
    {
        "name": "Economic Times Corporate",
        "url": "https://economictimes.indiatimes.com/news/company/corporate-trends/rssfeeds/2143429.cms",
        "category": "india_business",
        "weight": 1.2
    },
    {
        "name": "CNBC Business",
        "url": "https://search.cnbc.com/rs/search/combinedlist/view.xml?partnerId=wrss01&id=10001147",
        "category": "strategy_finance",
        "weight": 1.15
    },
    {
        "name": "Supply Chain Brain",
        "url": "https://www.supplychainbrain.com/rss/articles",
        "category": "operations",
        "weight": 1.3
    },
    {
        "name": "Marketing Dive",
        "url": "https://www.marketingdive.com/feeds/news/",
        "category": "marketing",
        "weight": 1.3
    }
]
