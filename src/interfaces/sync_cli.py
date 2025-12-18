#!/usr/bin/env python3
"""CLI for syncing NBA data to local SQLite database.

This script fetches NBA data from NBA.com via nba_api and stores it locally
to avoid rate limiting issues during normal operation.

Usage:
    uv run python src/interfaces/sync_cli.py           # Full sync (14 days)
    uv run python src/interfaces/sync_cli.py --days 7  # Sync last 7 days
    uv run python src/interfaces/sync_cli.py --status  # Show sync status
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.nba_api_client import NBASyncService
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Sync NBA data to local SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Full sync of last 14 days
    uv run python src/interfaces/sync_cli.py

    # Sync last 7 days only
    uv run python src/interfaces/sync_cli.py --days 7

    # Show current sync status
    uv run python src/interfaces/sync_cli.py --status

    # Sync only standings and star players (fast)
    uv run python src/interfaces/sync_cli.py --metadata-only

    # Force re-sync of games (clears existing game data)
    uv run python src/interfaces/sync_cli.py --force
        """,
    )

    parser.add_argument(
        "--days",
        "-d",
        type=int,
        default=14,
        help="Number of days of games to sync (default: 14)",
    )

    parser.add_argument(
        "--status", "-s", action="store_true", help="Show current sync status and exit"
    )

    parser.add_argument(
        "--metadata-only",
        "-m",
        action="store_true",
        help="Only sync teams, standings, and star players (no games)",
    )

    parser.add_argument(
        "--games-only",
        "-g",
        action="store_true",
        help="Only sync games (assumes teams already synced)",
    )

    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force re-sync by clearing existing data first",
    )

    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default="config.yaml",
        help="Path to config file (default: config.yaml)",
    )

    args = parser.parse_args()

    try:
        sync_service = NBASyncService(config_path=args.config)

        if args.status:
            log_status(sync_service)
            return

        if args.force:
            logger.warning("Force flag set - clearing existing data...")
            sync_service.db.clear_all()

        if args.metadata_only:
            logger.info("Syncing NBA metadata (teams, standings, star players)...")
            results = {
                "teams": sync_service.sync_teams(),
                "standings": sync_service.sync_standings(),
                "star_players": sync_service.sync_star_players(),
            }
        elif args.games_only:
            logger.info(f"Syncing NBA games for last {args.days} days...")
            results = {"games": sync_service.sync_games(days=args.days)}
        else:
            logger.info(f"Starting full NBA data sync (last {args.days} days)...")
            logger.info("This may take a few minutes due to rate limiting.")
            results = sync_service.sync_all(days=args.days)

        logger.info("=" * 50)
        logger.info("Sync Complete!")
        logger.info("=" * 50)
        for key, value in results.items():
            logger.info(f"  {key}: {value}")

        log_status(sync_service)

    except KeyboardInterrupt:
        logger.warning("Sync interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Sync failed: {e}")
        sys.exit(1)


def log_status(sync_service: NBASyncService):
    """Log current sync status."""
    status = sync_service.get_sync_status()

    logger.info("Database Status:")
    logger.info("=" * 50)
    logger.info(f"  Database: {status.get('db_path', 'N/A')}")
    logger.info(f"  Size: {status.get('db_size_mb', 0)} MB")
    logger.info("  Records:")
    logger.info(f"    Teams: {status.get('teams_count', 0)}")
    logger.info(f"    Players: {status.get('players_count', 0)}")
    logger.info(f"    Star Players: {status.get('star_players_count', 0)}")
    logger.info(f"    Games: {status.get('games_count', 0)}")
    logger.info(f"    Game Player Stats: {status.get('game_players_count', 0)}")
    logger.info(f"    Standings: {status.get('standings_count', 0)}")

    date_range = status.get("games_date_range", {})
    if date_range.get("min") and date_range.get("max"):
        logger.info(f"  Games Date Range: {date_range['min']} to {date_range['max']}")

    logger.info("  Last Sync Times:")
    for sync_type in ["teams", "standings", "star_players", "games"]:
        last_sync = status.get(f"last_{sync_type}_sync")
        if last_sync:
            logger.info(f"    {sync_type}: {last_sync}")
        else:
            logger.info(f"    {sync_type}: Never")


if __name__ == "__main__":
    main()
