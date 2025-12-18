<!-- AGENT_CONTEXT
status: active development
current_focus: nba_api + SQLite implementation complete and tested
blockers: none
next_steps: Merge PR, production deployment
last_updated: 2025-12-18 20:36
-->

# Project Log

## 2025-12-18 20:36

**Did:** Tested full pipeline with live December 2025 NBA data

- Fixed score retrieval: scores come from LineScore dataframe (index 1), not GameHeader
- Fixed CLI to show Margin/Stars instead of removed lead_changes field
- Updated test mocks to match new breakdown structure
- Synced 3 games from Dec 8, 2025 (season just starting)
- CLI recommendation working: Spurs @ Pelicans (135-132) ranked #1 with 60 pts
- All 144 tests passing

**Learned:** scoreboardv2 API returns multiple dataframes - GameHeader (index 0) has game metadata, LineScore (index 1) has actual scores by team ID.

---

## 2025-12-18 20:20

**Did:** Replaced Ball Don't Lie API with free nba_api + SQLite caching

Major changes:

- Added `nba_api` library (free, scrapes NBA.com directly)
- Created `src/utils/database.py` - SQLite database for persistent storage
- Created `src/api/nba_api_client.py` - New NBAClient using nba_api + SQLite
- Created `src/interfaces/sync_cli.py` - CLI to sync NBA data to local DB
- Updated `src/core/recommender.py` to use new client
- Updated `config.yaml` to remove Ball Don't Lie config, add database config
- All 144 tests passing

New workflow:

1. Run `uv run python src/interfaces/sync_cli.py` to populate database
2. Run `uv run python src/interfaces/cli.py` to get recommendations

Key benefits:

- No API key required (free!)
- Data stored locally in SQLite (fast, no rate limits after sync)
- Sync can be scheduled via cron for fresh data
- Built-in delays (600ms) prevent rate limiting during sync

**Learned:** nba_api needs delays between requests to avoid rate limiting from NBA.com. Using 600ms between calls works well.

---
