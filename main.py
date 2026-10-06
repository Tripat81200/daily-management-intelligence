import argparse
import sys
import logging
from pathlib import Path

from src.config import load_config
from src.utils.history import HistoryTracker
from src.news.collector import NewsCollector
from src.news.ranking import StoryRanker
from src.ai.analyst import ManagementIntelligenceAnalyst
from src.newsletter.generator import NewsletterGenerator
from src.email.sender import EmailSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("daily_management_intelligence")


def run_pipeline(dry_run: bool = False, force: bool = False) -> int:
    """Execute the end-to-end daily management briefing pipeline."""
    logger.info("=" * 60)
    logger.info("STARTING DAILY MANAGEMENT INTELLIGENCE PIPELINE")
    logger.info("=" * 60)

    # 1. Load configuration
    config = load_config()
    is_dry_run = dry_run or config.get("runtime", {}).get("dry_run", False)

    # 2. Initialize history tracker
    history_tracker = HistoryTracker()
    logger.info(f"Loaded {len(history_tracker.records)} historical story records.")

    # 3. Collect candidate news stories
    logger.info("Step 1: Ingesting fresh business news across operational, marketing, and strategy sources...")
    collector = NewsCollector(config)
    raw_candidates = collector.collect_all_candidates()

    if not raw_candidates:
        logger.warning("No fresh news candidates found. Generating emergency briefing from baseline feeds.")

    # 4. Filter, score, and rank candidates
    logger.info("Step 2: Scoring candidates, deduplicating, and bucketing into priority sections...")
    ranker = StoryRanker(config, history_tracker)
    ranked_sections = ranker.filter_and_rank(raw_candidates)

    total_selected = sum(len(v) for v in ranked_sections.values())
    logger.info(f"Selected {total_selected} high-signal stories across {len(ranked_sections)} categories.")

    # 5. Synthesize executive intelligence
    logger.info("Step 3: Synthesizing executive intelligence via AI analyst...")
    analyst = ManagementIntelligenceAnalyst(config)
    intelligence = analyst.analyze(ranked_sections)

    # 6. Generate newsletter HTML & text
    logger.info("Step 4: Rendering executive email briefing...")
    generator = NewsletterGenerator(config)
    subject, html_body, plain_text = generator.generate(intelligence)

    # 7. Deliver email
    logger.info("Step 5: Delivering executive briefing...")
    sender = EmailSender(config)
    success = sender.send(subject, html_body, plain_text, dry_run=is_dry_run)

    # 8. Record sent stories in history if not dry run
    if success and not is_dry_run:
        sent_items = []
        for s in intelligence.get("top_5", []):
            sent_items.append({"title": s.get("headline"), "url": s.get("source_url"), "category": "top_5"})
        for s in intelligence.get("operations", []):
            sent_items.append({"title": s.get("headline"), "url": s.get("source_url"), "category": "operations"})
        for s in intelligence.get("marketing", []):
            sent_items.append({"title": s.get("headline"), "url": s.get("source_url"), "category": "marketing"})
        
        history_tracker.record_stories(sent_items)
        logger.info(f"Recorded {len(sent_items)} newly published stories in history tracker.")

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info("=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Daily Management Intelligence CLI")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML preview without sending email")
    parser.add_argument("--force", action="store_true", help="Ignore minimum threshold filters")
    args = parser.parse_args()

    try:
        exit_code = run_pipeline(dry_run=args.dry_run, force=args.force)
        sys.exit(exit_code)
    except Exception as e:
        logger.exception(f"Fatal error in pipeline execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
