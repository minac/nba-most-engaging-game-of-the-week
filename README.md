# NBA Game Recommender

Finds the most engaging NBA game from the past week using real NBA API data. Scores games based on closeness, star power, top teams, and custom preferences.

## Features

- **Multiple Interfaces**: CLI, REST API, Web UI, or TRMNL E-ink Display
- **Smart Scoring**: Evaluates games on top team participation, closeness, star players, and favorite team
- **Configurable**: Customize weights and preferences via `config.yaml`
- **Cached**: File-based caching reduces API calls and improves performance
- **Real NBA Data**: Uses Ball Don't Lie API for live game data

## Quick Start

```bash
# Install dependencies
uv sync

# Run CLI
uv run python src/interfaces/cli.py

# Run API server (localhost:3000)
uv run python src/interfaces/api_server.py

# Run web interface (localhost:8080)
uv run python src/interfaces/web/app.py
```

## CLI Usage

```bash
uv run python src/interfaces/cli.py              # Best game, last 7 days
uv run python src/interfaces/cli.py -d 3         # Last 3 days
uv run python src/interfaces/cli.py -t LAL       # Set favorite team
uv run python src/interfaces/cli.py --all        # Show all games ranked
```

## API Endpoints

Start server: `uv run python src/interfaces/api_server.py`

- `GET /api/health` - Health check
- `GET /api/best-game?days=7&team=LAL` - Best game
- `GET /api/games?days=7&team=LAL` - All games ranked
- `GET /api/config` - Current configuration
- `GET /api/trmnl?days=7&team=LAL` - TRMNL webhook format

Example:
```bash
curl "http://localhost:3000/api/best-game?days=7&team=LAL"
```

## Web Interface

```bash
uv run python src/interfaces/web/app.py
open http://localhost:8080
```

Visit `/trmnl-viewer` to preview TRMNL layouts.

## TRMNL E-ink Display Setup

1. Deploy app to hosting service (see Deployment below)
2. In TRMNL: Create Private Plugin with "Polling" strategy
3. Set webhook: `https://your-app.com/api/trmnl?days=7&team=LAL`
4. Copy markup from `trmnl/src/full.liquid` (or other layouts: `half_horizontal.liquid`, `half_vertical.liquid`, `quadrant.liquid`)
5. Set refresh to 3600 seconds
6. Add to playlist

**Local TRMNL Development:**
```bash
cd trmnl
gem install trmnlp
trmnlp serve  # Opens http://localhost:3000
```

## Testing

```bash
# Install test dependencies
uv sync --extra test

# Run all tests
uv run pytest

# Run without coverage (faster)
uv run pytest --no-cov

# Unit or integration tests only
uv run pytest tests/unit/
uv run pytest tests/integration/

# With coverage
uv run pytest --cov=src --cov-report=html
```

**Cache Management:**
Tests use `/tmp/nba_cache` by default.
```bash
# Clear cache
rm -rf /tmp/nba_cache

# Check cache
ls -lh /tmp/nba_cache/scoreboards/
```

## Configuration

Edit `config.yaml` to customize:

```yaml
favorite_team: "LAL"  # or null

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
  api_key: null  # Or set BALLDONTLIE_API_KEY env var
```

## Deployment to Render

**Option 1: Blueprint (Recommended)**
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. New + → Blueprint
3. Connect repository
4. Auto-deploys using `render.yaml`

**Option 2: Manual**
1. New Web Service on Render
2. Connect repository
3. Build: `pip install uv && uv sync`
4. Start: `uv run gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 'src.interfaces.web.app:app'`
5. Environment: Python 3.11

Access at: `https://your-app-name.onrender.com`

## Architecture

```
src/
├── core/              # Business logic
│   ├── game_scorer.py      # Scoring algorithm
│   └── recommender.py      # Recommendation engine
├── api/               # External APIs
│   └── nba_client.py       # Ball Don't Lie client + caching
├── utils/             # Utilities
│   ├── logger.py           # Logging
│   └── cache.py            # File-based cache
└── interfaces/        # User interfaces
    ├── cli.py              # Command-line
    ├── api_server.py       # REST API
    └── web/app.py          # Web UI

trmnl/src/            # E-ink display layouts
tests/                # Unit and integration tests
```

## Common Team Codes

LAL, BOS, GSW, MIA, CHI, NYK, BKN, PHI, MIL, PHX, DAL, DEN, MEM, TOR, ATL

See `claude.md` for detailed technical documentation.
