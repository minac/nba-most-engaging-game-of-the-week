# NBA Game Recommender

Finds the most engaging NBA game from the past week using real NBA API data. Scores games based on lead changes, closeness, star power, and top teams.

## Quick Start

- **Modular Architecture**: Run as CLI, REST API, Web Application, or TRMNL E-ink Display
- **TRMNL Integration**: Display on your e-ink dashboard with multiple layout options
- **Smart Scoring Algorithm**: Evaluates games based on:
  - Lead changes (more exciting)
  - Top 5 team participation
  - Final margin (closer games score higher)
  - Minimum 200 points threshold
  - Star player participation
  - Favorite team bonus
- **Configurable**: Customize scoring weights and preferences via `config.yaml`
- **Real NBA Data**: Fetches actual game data from the NBA Stats API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/minac/nba-most-engaging-game-of-the-week.git
cd nba-most-engaging-game-of-the-week
```

2. Install dependencies:
```bash
# Install
uv sync

# Run CLI
uv run python src/interfaces/cli.py

# Run API server
uv run python src/interfaces/api_server.py

# Run web interface
uv run python src/interfaces/web/app.py
```

## Commands

### CLI
```bash
uv run python src/interfaces/cli.py              # Best game, last 7 days
uv run python src/interfaces/cli.py -d 3         # Last 3 days
uv run python src/interfaces/cli.py -t LAL       # Set favorite team
uv run python src/interfaces/cli.py --all        # Show all games ranked
```

### API Server (localhost:3000)
```bash
uv run python src/interfaces/api_server.py
curl "http://localhost:3000/api/best-game?days=7&team=LAL"
```

**Endpoints**: `/api/health`, `/api/best-game`, `/api/games`, `/api/config`, `/api/trmnl`

### Web Interface (localhost:8080)
```bash
uv run python src/interfaces/web/app.py
open http://localhost:8080
```

### TRMNL Screen Viewer
Preview TRMNL layouts before deploying. Start web server, then visit:
<http://localhost:8080/trmnl-viewer>

### TRMNL E-ink Display
Deploy to Render, then use endpoint:
<https://your-app-name.onrender.com/api/trmnl?days=7&team=LAL>

**See [trmnl/README.md](trmnl/README.md)** for complete TRMNL setup, layouts, and configuration.

## Testing

```bash
uv sync --extra test              # Install test dependencies
uv run pytest                     # Run all tests
uv run pytest --no-cov           # Skip coverage
uv run pytest tests/unit/        # Unit tests only
```

**See [tests/README.md](tests/README.md)** for full testing commands, cache management, and coverage.

## Deploy to Render

### Option 1: Connect via Dashboard (Recommended)
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and deploy

### Option 2: Manual Setup
1. Create new **Web Service** on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install uv && uv sync`
   - **Start Command**: `uv run gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 'src.interfaces.web.app:app'`
   - **Environment**: Python 3.11
4. Deploy

Your app will be available at: `https://your-app-name.onrender.com`
