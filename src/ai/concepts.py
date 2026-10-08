"""Curated knowledge base of core MBA concepts, strategic frameworks, and mental models.

Used to enrich sections when daily news is scarce or to inject high-value conceptual learning.
"""

from typing import Dict, List, Any
import random

MBA_CONCEPTS_BY_CATEGORY: Dict[str, List[Dict[str, Any]]] = {
    "operations": [
        {
            "headline": "[Core Framework] The Bullwhip Effect & Point-of-Sale Data Synchronization",
            "what_happened": "In supply chain management, the Bullwhip Effect describes how minor fluctuations in end-consumer retail demand amplify into massive, chaotic swings in demand forecasts for tier-1 suppliers and raw material manufacturers. Without real-time data sharing, each node in the supply chain artificially inflates safety stock to hedge against stockout risk.",
            "why_it_matters_operationally": "Distorts production schedules, causes costly warehouse inventory bloat, and spikes holding costs during economic slowdowns while causing sudden stockouts during demand spikes.",
            "operational_lesson": "Operations leaders must bypass intermediate distributor forecasts and establish direct, API-level POS (Point-of-Sale) demand visibility with upstream suppliers to dampen demand variance.",
            "source_name": "MIT Sloan Management Review (Hau Lee Supply Chain Research)",
            "source_url": "https://sloanreview.mit.edu/article/the-bullwhip-effect-in-supply-chains/"
        },
        {
            "headline": "[Operations Model] Goldratt's Theory of Constraints: The Drum-Buffer-Rope Architecture",
            "what_happened": "Eliyahu Goldratt's Theory of Constraints dictates that any operational system is limited by exactly one bottleneck. Maximizing the efficiency or output of non-bottleneck machines does not increase total throughput; it merely creates piles of expensive work-in-progress (WIP) inventory that clogs factory floors.",
            "why_it_matters_operationally": "Misallocating capital to optimize non-bottleneck steps burns cash without improving system fulfillment velocity or revenue recognition.",
            "operational_lesson": "Subordinate all other operational processes to the pace of the constraint (the 'Drum'), protect it with inventory (the 'Buffer'), and synchronize release of raw materials to its consumption rate (the 'Rope').",
            "source_name": "The Goal: A Process of Ongoing Improvement (Goldratt)",
            "source_url": "https://www.tocinstitute.org/theory-of-constraints.html"
        },
        {
            "headline": "[Inventory Strategy] Economic Order Quantity (EOQ) in High-Interest Regimes",
            "what_happened": "The classical EOQ model balances the fixed cost of placing an order against the variable cost of holding inventory. In an era where interest rates and cost of working capital exceed 8-10%, the holding cost component rises dramatically relative to order setup costs.",
            "why_it_matters_operationally": "Firms running legacy batch-size formulas suffer severe cash-flow traps as excess buffer stock locks up expensive operating capital.",
            "operational_lesson": "High-interest rate environments mandate smaller, frequent delivery batches and vendor-managed inventory (VMI) agreements to minimize days-sales-of-inventory (DSI).",
            "source_name": "Harvard Business Review (Working Capital Strategy)",
            "source_url": "https://hbr.org/2023/11/managing-working-capital-in-a-high-interest-rate-environment"
        }
    ],
    "marketing": [
        {
            "headline": "[Marketing Principle] The CAC/LTV Death Spiral & Channel Saturation",
            "what_happened": "In digital commerce and subscription businesses, the Customer Acquisition Cost (CAC) to Lifetime Value (LTV) ratio measures unit economic viability. As digital ad auctions saturate, acquisition costs inflate while customer retention degrades due to switching ease, driving the LTV/CAC ratio below the sustainable 3:1 benchmark.",
            "why_it_matters_marketing": "Relying purely on performance marketing creates an 'ad-spend addiction' where top-line growth evaporates the moment venture subsidies or marketing budgets are trimmed.",
            "marketing_lesson": "Sustainable brand advantage requires shifting capital from rented media (Meta/Google ad auctions) to owned audience channels, zero-party data capture, and product-led word-of-mouth referral loops.",
            "source_name": "Harvard Business Review (Customer Lifetime Economics)",
            "source_url": "https://hbr.org/2014/10/the-value-of-keeping-the-right-customers"
        },
        {
            "headline": "[Brand Positioning] The Law of Duality & Category Ownership (Ries & Trout)",
            "what_happened": "Al Ries and Jack Trout's foundational positioning research demonstrates that in the mature phase of any consumer category, the market inevitably bifurcates into a battle between two dominant players (e.g., Coke vs. Pepsi, Nike vs. Adidas, Apple vs. Samsung). Mid-tier brands that attempt to be 'all things to all customers' get squeezed out of consumer consideration sets.",
            "why_it_matters_marketing": "Attempting to copy the market leader's positioning results in commoditization; challenger brands must position as the explicit philosophical alternative to the incumbent.",
            "marketing_lesson": "If your brand cannot be first in an existing product category, create a new sub-category where you can establish undisputed mental primacy.",
            "source_name": "Positioning: The Battle for Your Mind (Al Ries & Jack Trout)",
            "source_url": "https://www.ries.com/thought-leadership/"
        },
        {
            "headline": "[Pricing Architecture] Decoy Effect & Anchoring in Tiered Product Portfolios",
            "what_happened": "Behavioral economics reveals that consumers rarely evaluate prices in isolation; they evaluate prices relative to reference anchors. By introducing an asymmetric 'decoy' tier (a premium package with slight incremental value at a much higher price), marketers nudge consumer preference toward the targeted high-margin middle tier.",
            "why_it_matters_marketing": "Directly expands Average Order Value (AOV) and Gross Margin without increasing customer acquisition spend or raw material cost.",
            "marketing_lesson": "Price is not merely a cost-recovery mechanism; price is communication. Strategic price architecture influences consumer perception of product value before features are even examined.",
            "source_name": "MIT Sloan (Behavioral Pricing Dynamics)",
            "source_url": "https://sloanreview.mit.edu/article/the-art-and-science-of-pricing/"
        }
    ],
    "strategy_finance": [
        {
            "headline": "[Strategic Moats] Network Effects vs. Scale Economies: Hamilton Helmer's 7 Powers",
            "what_happened": "Strategy theorist Hamilton Helmer identifies seven structural sources of sustained superior returns: Scale Economies, Network Effects, Counter-Positioning, Switching Costs, Branding, Cornered Resources, and Process Power. Crucially, scale alone does not guarantee a moat unless protected by high switching costs or network density.",
            "why_it_matters": "Confusing market share with a defensible moat leads executives to pursue unprofitable revenue growth that quickly erodes when competitors enter.",
            "strategic_takeaway": "Management must explicitly identify which of the 7 Powers defends their operating margin before approving capital expenditure or geographic expansion.",
            "source_name": "7 Powers: The Foundations of Business Strategy (Hamilton Helmer)",
            "source_url": "https://7powers.com/"
        },
        {
            "headline": "[Corporate Finance] The M&A Winner's Curse & Synergistic Integration Risk",
            "what_happened": "Academic research across thousands of corporate acquisitions reveals that over 70% of mergers fail to create shareholder value for the acquiring firm. The root causes are the 'winner's curse' (overpaying in competitive bidding auctions) and aggressive underestimation of cultural and IT integration costs.",
            "why_it_matters": "Financial models often assume aggressive revenue and cost synergies that fail to materialize in real-world post-merger integration (PMI).",
            "strategic_takeaway": "Top-tier CFOs structure acquisitions with earnouts linked to post-close operating cash flows rather than all-cash upfront valuations.",
            "source_name": "McKinsey on Finance (Why Mergers Fail)",
            "source_url": "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-keys-to-successful-ma"
        }
    ],
    "tech_ai": [
        {
            "headline": "[Enterprise Tech] Amara's Law & The Horizon of AI Productivity Dividends",
            "what_happened": "Amara's Law states: 'We tend to overestimate the effect of a technology in the short run and underestimate the effect in the long run.' Organizations investing billions in generative AI proofs-of-concept frequently experience an initial trough of disillusionment as legacy ERP workflows resist change.",
            "why_it_matters": "Chief Information Officers who write off emerging tech during the early hype trough get disrupted when autonomous agent infrastructure matures 3-5 years later.",
            "business_implication": "Enterprise AI ROI is realized not by deploying chat interfaces, but by fundamentally re-architecting underlying business logic and reducing human friction in transactional workflows.",
            "source_name": "Gartner Technology Adoption Research",
            "source_url": "https://www.gartner.com/en/research/methodologies/gartner-hype-cycle"
        },
        {
            "headline": "[Software Economics] The Cloud Repatriation Paradox & Gross Margin Protection",
            "what_happened": "While public cloud infrastructure (AWS/Azure/GCP) provides unmatched agility during early-stage scaling, mature enterprises operating predictable, high-throughput compute workloads face severe gross margin degradation if they remain entirely on on-demand cloud pricing.",
            "why_it_matters": "As tech companies scale past $100M ARR, cloud hosting bills can represent up to 30-50% of cost of goods sold (COGS), depressing enterprise valuation multiples.",
            "business_implication": "Leading technology executives pursue hybrid infrastructure architectures: public cloud for bursting and edge delivery, and colocation/bare-metal for steady-state baseline compute.",
            "source_name": "Andreessen Horowitz (The Cost of Cloud: A Trillion Dollar Paradox)",
            "source_url": "https://a16z.com/the-cost-of-cloud-paradox-market-cap-cloud-spend/"
        }
    ],
    "india_business": [
        {
            "headline": "[India Macro Strategy] The Digital Public Infrastructure (DPI) & India Stack Flywheel",
            "what_happened": "India's three-tier DPI architecture—Identity (Aadhaar), Payments (UPI), and Data Governance (Account Aggregator)—has driven formal financial inclusion from under 35% in 2014 to over 85% today. Unlike Western proprietary platforms (Apple Pay, PayPal), India's open, interoperable rails drastically compress consumer transaction costs.",
            "why_it_matters": "Lowers customer onboarding and transaction friction to near zero, enabling D2C, fintech, and retail distribution models previously impossible in lower-income demographics.",
            "india_market_insight": "Corporate strategists targeting India cannot simply port Western SaaS or retail playbooks; they must build natively on open DPI rails to capture Tier 2 and Tier 3 purchasing power.",
            "source_name": "Reserve Bank of India (DPI Working Paper)",
            "source_url": "https://www.rbi.org.in/"
        },
        {
            "headline": "[Retail Operations] Quick Commerce & The Dark Store Density Flywheel in Metro India",
            "what_happened": "India's quick commerce giants (Blinkit, Zepto, Instamart) are transforming urban retail operations by establishing decentralized micro-warehouses (dark stores) within 2-3 kilometer radii. Profitability in this model is strictly a function of order density per dark store (hitting 1,200+ orders/day) and gross margin expansion via high-margin non-grocery categories.",
            "why_it_matters": "Disrupts traditional mom-and-pop (Kirana) and organized modern trade distribution for FMCG, beauty, and consumer electronics.",
            "india_market_insight": "Brands are reallocating trade marketing budgets away from traditional distributor margins toward quick-commerce sponsored listings and dark store placement fees.",
            "source_name": "Economic Times Corporate (Quick Commerce Landscape)",
            "source_url": "https://economictimes.indiatimes.com/"
        }
    ],
    "global_business": [
        {
            "headline": "[Global Macro] Tariff Pass-Through, Terms of Trade & Supply Chain Realignment",
            "what_happened": "Classical international trade economics dictates that import tariffs are rarely absorbed entirely by foreign exporters. Instead, domestic import-competing firms raise prices, while downstream manufacturers and consumers bear the deadweight loss through higher input costs and compressed operating margins.",
            "why_it_matters": "Geopolitical tariff barriers alter optimal manufacturing locations, accelerating the shift toward 'China+1' sourcing in Vietnam, Mexico, and India.",
            "macro_impact": "Multinational procurement executives must calculate total landed cost—including tariffs, logistics insurance, and buffer inventory carrying costs—rather than FOB factory-gate price.",
            "source_name": "Peterson Institute for International Economics (PIIE)",
            "source_url": "https://www.piie.com/"
        },
        {
            "headline": "[Global Finance] The Dollar Smile Theory & Cross-Border Capital Allocation",
            "what_happened": "Formulated by economist Stephen Jen, the Dollar Smile Theory explains why the US Dollar appreciates under two opposing macroeconomic extremes: during deep global recessions (safe-haven flows on the left of the smile) AND during strong US economic outperformance (yield-seeking investment on the right). It only weakens when the rest of the world outpaces US growth (the bottom of the smile).",
            "why_it_matters": "Emerging market corporates borrowing in USD face severe debt-servicing spikes during periods of global stress, triggering currency mismatch risk.",
            "macro_impact": "Corporate treasurers operating across global markets must maintain disciplined foreign exchange hedging policies rather than speculating on directional currency moves.",
            "source_name": "International Monetary Fund (Global Financial Stability Report)",
            "source_url": "https://www.imf.org/"
        }
    ]
}


def get_concept_for_category(category: str, index: int = 0) -> Dict[str, Any]:
    """Retrieve an MBA conceptual framework for a given category."""
    concept_list = MBA_CONCEPTS_BY_CATEGORY.get(category, [])
    if not concept_list:
        return {
            "headline": f"[Strategic Concept] Core {category.replace('_', ' ').title()} Mental Model",
            "what_happened": "Operational resilience and disciplined capital allocation define enduring competitive advantages.",
            "why_it_matters": "Leaders who master fundamental business unit economics outperform competitors reliant on market euphoria.",
            "management_takeaway": "Continuous focus on contribution margin, customer retention, and process standardization builds sustainable shareholder value.",
            "competitive_advantage": "Proactive capability building protects operating margins during economic contractions.",
            "source_name": "Harvard Business Review Strategy Archive",
            "source_url": "https://hbr.org/"
        }
    # Pick deterministically or by index so it stays consistent within a day
    item = dict(concept_list[index % len(concept_list)])
    if "title" not in item and "headline" in item:
        item["title"] = item["headline"]
    if "summary" not in item and "what_happened" in item:
        item["summary"] = item["what_happened"]
    return item
