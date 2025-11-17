# Claude.md - NBA Game Recommender Technical Guide

Technical documentation for developers and AI assistants working with the NBA Game Recommender codebase.

## Project Overview

Modular NBA game recommendation system that analyzes past week's games using Ball Don't Lie API. Scores games on engagement factors (closeness, star power, top teams) and ranks them. Supports CLI, REST API, Web UI, and TRMNL e-ink display.

## Architecture

### Modular Design

```
src/
├── core/              # Business logic
│   ├── game_scorer.py      # Scoring algorithm (5 criteria)
│   └── recommender.py      # Orchestration
├── api/
│   └── nba_client.py       # Ball Don't Lie API + caching
├── utils/
│   ├── logger.py           # Centralized logging
│   └── cache.py            # Date-based file cache
└── interfaces/
    ├── cli.py              # Command-line
    ├── api_server.py       # REST API (Flask)
    └── web/app.py          # Web UI

trmnl/src/            # Liquid templates for e-ink
tests/                # Unit + integration tests
```

### Key Components

**GameScorer** (`src/core/game_scorer.py`)
- Pure scoring logic, no side effects
- Configurable weights from `config.yaml`
- Returns score + detailed breakdown

**GameRecommender** (`src/core/recommender.py`)
- Fetches games via NBAClient
- Applies GameScorer to each game
- Returns sorted results

**NBAClient** (`src/api/nba_client.py`)
- Ball Don't Lie API client
- Rate limiting: 100 req/min
- Integrated with DateBasedCache
- Fetches: scoreboards, game details, standings, season leaders

**DateBasedCache** (`src/utils/cache.py`)
- File-based cache: `/tmp/nba_cache/`
- Organized by date (scoreboards) and game ID (details)
- Configurable TTL (default: 30 days)
- Auto-cleanup on startup

**Logger** (`src/utils/logger.py`)
- Centralized config using stdlib logging
- Consistent formatting across all modules

## Scoring Algorithm

See `src/core/game_scorer.py`:

1. **Top 5 Teams** (20 pts/team) - Dynamically fetched from standings API
2. **Game Closeness** (up to 50 pts) - 0-3 margin: 50pts, 4-5: 40pts, 6-10: 25pts, 11-15: 12.5pts
3. **Total Points Threshold** (200+ min) - 90% penalty if below
4. **Star Power** (20 pts/star) - Top 30 scorers from season leaders API
5. **Favorite Team** (100 pts) - User preference bonus

All weights configurable in `config.yaml`.

## Configuration

Single `config.yaml` controls everything:

```yaml
favorite_team: "LAL"
scoring:
  top5_team_bonus: 20
  close_game_bonus: 50
  min_total_points: 200
  star_power_weight: 20
  favorite_team_bonus: 100
cache:
  enabled: true
  directory: "/tmp/nba_cache"
  scoreboard_ttl_days: 30
  game_details_ttl_days: 30
  auto_cleanup: true
nba_api:
  api_key: null  # Or BALLDONTLIE_API_KEY env var
```

Changes take effect on restart (no hot reload).

## Data Flow

1. User request → Interface layer (CLI/API/Web/TRMNL)
2. Interface → `GameRecommender.get_best_game(days, team)`
3. Recommender → `NBAClient.fetch_games()`
4. NBAClient checks `DateBasedCache`
   - HIT: Return cached (fast)
   - MISS: Fetch from API, cache, return
5. For each game: `GameScorer.score_game()` calculates score
6. Sort by score, return results

## Development Patterns

### Adding Scoring Criteria

1. Add weight to `config.yaml` scoring section
2. Load in `GameScorer.__init__()`
3. Add logic in `GameScorer.score_game()`
4. Update breakdown dict
5. Update tests

### Adding API Endpoints

1. Add route in `src/interfaces/api_server.py`
2. Use existing `recommender` instance
3. Return JSON response
4. Add integration test

### Modifying Data Points

1. Check Ball Don't Lie API support
2. Update `NBAClient` methods
3. Update game dict in `recommender.py`
4. Make available to `GameScorer`
5. Consider cache implications

## Important Files

- `config.yaml` - All configuration
- `src/core/game_scorer.py` - Scoring algorithm
- `src/core/recommender.py` - Main orchestration
- `src/api/nba_client.py` - API client + caching
- `src/utils/cache.py` - Caching system
- `pyproject.toml` - Dependencies (managed by uv)

## Working with the Codebase

**CRITICAL**: Always use `uv` - never use `pip`, `python`, or `python3` directly.

### Common Commands

```bash
# Dependencies
uv sync                    # Install production deps
uv sync --extra test       # Include test deps
uv add <package>           # Add dependency
uv remove <package>        # Remove dependency

# Running
uv run python src/interfaces/cli.py
uv run python src/interfaces/api_server.py
uv run python src/interfaces/web/app.py

# Testing
uv run pytest                          # All tests
uv run pytest --cov=src               # With coverage
uv run pytest tests/unit/             # Unit only
uv run pytest tests/integration/      # Integration only
```

### Caching System

**Performance Impact:**
- Without cache: 2-5 sec/game (API latency)
- With cache: 0.01 sec (file read)

**Cache Structure:**
```
/tmp/nba_cache/
├── scoreboards/
│   └── 2024-01-15.json    # All games for date
└── games/
    └── 0022300123.json    # Game details
```

**Management:**
- Clear: `rm -rf /tmp/nba_cache`
- Stats: `cache.get_cache_stats()`
- Auto-cleanup: Set `auto_cleanup: true` in config

### API Endpoints

- `GET /api/health` - Health check
- `GET /api/best-game?days=7&team=LAL` - Best game
- `GET /api/games?days=7&team=LAL` - All ranked
- `GET /api/config` - Current config
- `GET /api/trmnl?days=7&team=LAL` - TRMNL webhook

### TRMNL Integration

E-ink display endpoint returns Liquid template variables:

```json
{
  "merge_variables": {
    "home_team": "LAL",
    "home_score": 118,
    "away_team": "BOS",
    "away_score": 115,
    "engagement_score": 425.5,
    "is_favorite": "yes",
    "breakdown_*": "..."
  }
}
```

Layouts in `trmnl/src/`: `full.liquid`, `half_horizontal.liquid`, `half_vertical.liquid`, `quadrant.liquid`

## Error Handling

- NBA API errors caught and logged in `NBAClient`
- Config validation at startup
- Missing data falls back to defaults
- Top teams/stars fall back if API fails
- Cache errors logged but don't block (falls back to API)

## Testing

**Test Structure:**
- `tests/unit/` - Component tests (scorer, recommender, client, cache)
- `tests/integration/` - Interface tests (CLI, API)
- `tests/fixtures/` - Shared test data

**Key Practices:**
- Mock NBA API for reliability (using `responses` library)
- Real file I/O for cache tests
- Use `freezegun` for date mocking
- Test edge cases: no games, API failures, tied games

## Code Style

- Python 3.11+
- Docstrings on classes and public methods
- Type hints (Dict, Optional, etc.)
- Configuration over hardcoding
- Use `get_logger(__name__)` from `src.utils.logger`
- No `print()` in production code

## Dependencies

**Production:**
- requests, flask, pyyaml, python-dateutil, gunicorn, python-dotenv

**Test (optional):**
- pytest, pytest-cov, pytest-mock, responses, freezegun

Managed in `pyproject.toml` via uv.

## Tips for AI Assistants

1. **Always use uv** - Never use pip/python directly
2. **Use logger utility** - `get_logger(__name__)` not `print()`
3. **Understand caching** - Automatic in NBAClient, check config first
4. **Read config first** - Check `config.yaml` for current settings
5. **Follow architecture** - Keep core in `src/core/`, interfaces separate
6. **Preserve modularity** - Changes work across all interfaces
7. **Run tests** - Use `uv run pytest` to verify changes
8. **Check data structure** - Look at NBAClient returns before using
9. **Scoring is configurable** - Don't hardcode, use config weights
10. **Test TRMNL** - Verify `/api/trmnl` endpoint if changing data structure

## Future Enhancements

- Historical game database (beyond file cache)
- ML for personalized weights
- Live game recommendations
- Playoff importance factor
- Advanced metrics (limited by API)
- Redis/memcached for distributed caching
