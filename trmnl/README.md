# NBA Game Recommender - TRMNL Plugin

Display the most engaging NBA game of the week on your TRMNL e-ink display!

## Overview

This plugin shows NBA game recommendations on your TRMNL device with engagement scores based on:
- Lead changes (more exciting games)
- Game closeness (final margin)
- Top 5 team participation
- Star player participation
- Favorite team bonus

## Features

- **Multiple Layout Sizes**: Supports full screen, half horizontal, half vertical, and quadrant displays
- **Real-time Updates**: Automatically refreshes to show the latest exciting games
- **Customizable**: Set your favorite team and lookback period
- **Smart Scoring**: Advanced algorithm evaluates games for entertainment value

## Setup Instructions

### Option 1: Using TRMNL Private Plugin (Recommended)

1. **Get your webhook URL from TRMNL**:
   - Log in to your TRMNL account at https://usetrmnl.com
   - Navigate to Plugins → Create Private Plugin
   - Copy your webhook URL

2. **Deploy your NBA Game Recommender API**:
   - Deploy this repository to Railway, Heroku, or your preferred platform
   - Note your deployed URL (e.g., `https://your-app.railway.app`)

3. **Configure the plugin markup**:
   - In TRMNL, create a new Private Plugin
   - Set the **Strategy** to "Polling"
   - Set the **Endpoint URL** to: `https://your-app.railway.app/api/trmnl?days=7&team=LAL`
     - Replace `LAL` with your favorite team's 3-letter code (or omit `&team=LAL` if you don't have a favorite)
     - Adjust `days=7` to look back more or fewer days
   - Set **Refresh Interval** to 3600 seconds (1 hour)

4. **Add the markup template**:
   - Copy the contents of one of the following files from this repository:
     - `trmnl/src/full.liquid` - Full screen layout
     - `trmnl/src/half_horizontal.liquid` - Half screen (horizontal)
     - `trmnl/src/half_vertical.liquid` - Half screen (vertical)
     - `trmnl/src/quadrant.liquid` - Quarter screen
   - Paste it into the Markup editor in TRMNL
   - Choose the appropriate screen size for your layout

5. **Save and activate**:
   - Click "Save Plugin"
   - Add the plugin to your TRMNL playlist
   - Your device will start displaying NBA game recommendations!

## How to Use

Once your plugin is set up and added to your TRMNL playlist, it will automatically:

1. **Fetch game data** from your deployed API endpoint every hour (or at your configured refresh interval)
2. **Display the most engaging game** from the past 7 days (or your configured lookback period)
3. **Show detailed information** including:
   - Team names and final scores
   - Overall engagement score
   - Lead changes, final margin, star players
   - Favorite team indicator (if configured)
4. **Auto-refresh** to always show the latest recommendations

### Daily Usage

Your TRMNL device will show:
- **During NBA season**: The most exciting recent game based on the scoring algorithm
- **Off-season**: An empty state with a message indicating no games were found
- **After big games**: Updated scores highlighting the best matchups

### Best Practices

- **Set your favorite team** in the URL to prioritize games featuring your team
- **Adjust the lookback period** based on your preferences:
  - `days=3` - Only very recent games
  - `days=7` - Full week (recommended)
  - `days=14` - Two weeks for catching up
- **Choose the right layout** for your TRMNL configuration:
  - Full screen for dedicated NBA tracking
  - Half/quadrant for mixed content playlists
- **Refresh interval**: 1 hour (3600 seconds) is recommended to balance freshness with API usage

### What You'll See

The plugin displays:
- **Game matchup**: Team abbreviations and full names
- **Final scores**: Large, easy-to-read numbers
- **Engagement score**: Overall entertainment rating (higher is better)
- **Score breakdown**: How the engagement score was calculated
  - Lead changes (more is better)
  - Final margin (closer is better)
  - Star player count
  - Top 5 team participation
  - Favorite team bonus indicator
- **Last updated time**: Confirms data freshness

### Example Display

```
🏀 MOST ENGAGING GAME
2024-01-15

LAL     @     BOS
118           115

ENGAGEMENT SCORE
     425.5

Lead Changes: 12 (120.0 pts)
Final Margin: 3 pts (100.0 pts)
Star Players: 4 (80.0 pts)
⭐ Favorite Team Bonus
```

### Option 2: Using trmnlp Development Server

For local development and testing:

1. **Install trmnlp**:
   ```bash
   # Using RubyGems
   gem install trmnlp

   # Or using Docker
   docker pull trmnl/trmnlp
   ```

2. **Navigate to the plugin directory**:
   ```bash
   cd trmnl
   ```

3. **Start the development server**:
   ```bash
   trmnlp serve
   ```

4. **View the plugin**:
   - Open your browser to `http://localhost:3000`
   - The plugin will render with sample data

5. **Customize the data**:
   - Edit `.trmnlp.yml` to add custom variables
   - Modify the liquid templates in `src/`
   - Changes will auto-reload in your browser

## API Endpoint

### GET `/api/trmnl`

Returns game data in TRMNL-compatible format.

**Query Parameters**:
- `days` (optional): Number of days to look back (1-14, default: 7)
- `team` (optional): Favorite team 3-letter abbreviation (e.g., LAL, BOS, GSW)

**Example**:
```bash
curl "https://your-app.railway.app/api/trmnl?days=7&team=LAL"
```

**Response Format**:
```json
{
  "merge_variables": {
    "game": {
      "game_date": "2024-01-15",
      "away_team": {
        "name": "Los Angeles Lakers",
        "abbr": "LAL",
        "score": 118
      },
      "home_team": {
        "name": "Boston Celtics",
        "abbr": "BOS",
        "score": 115
      }
    },
    "score": "425.5",
    "breakdown": {
      "lead_changes": {
        "count": 12,
        "points": "120.0"
      },
      "top5_teams": {
        "count": 2,
        "points": "100.0"
      },
      "close_game": {
        "margin": 3,
        "points": "100.0"
      },
      "star_power": {
        "count": 4,
        "points": "80.0"
      },
      "favorite_team": {
        "has_favorite": true,
        "points": "75.0"
      }
    },
    "updated_at": "02:30 PM"
  }
}
```

## Template Variables

The following variables are available in all liquid templates:

### `game` (object)
- `game.game_date` - Date of the game (e.g., "2024-01-15")
- `game.away_team.name` - Full away team name
- `game.away_team.abbr` - Away team abbreviation
- `game.away_team.score` - Away team score
- `game.home_team.name` - Full home team name
- `game.home_team.abbr` - Home team abbreviation
- `game.home_team.score` - Home team score

### `score` (string)
Overall engagement score (formatted to 1 decimal place)

### `breakdown` (object)
Detailed score breakdown:
- `breakdown.lead_changes.count` - Number of lead changes
- `breakdown.lead_changes.points` - Points from lead changes
- `breakdown.top5_teams.count` - Number of top 5 teams playing
- `breakdown.top5_teams.points` - Points from top 5 teams
- `breakdown.close_game.margin` - Final point margin
- `breakdown.close_game.points` - Points from game closeness
- `breakdown.star_power.count` - Number of star players
- `breakdown.star_power.points` - Points from star players
- `breakdown.favorite_team.has_favorite` - Boolean if favorite team played
- `breakdown.favorite_team.points` - Points from favorite team bonus

### `updated_at` (string)
Last update time (e.g., "02:30 PM")

### `error_message` (string, optional)
Error or empty state message when no games found

## Customization

### Change the Lookback Period

Modify the `days` parameter in your TRMNL webhook URL:
```
https://your-app.railway.app/api/trmnl?days=3
```

### Set a Favorite Team

Add the `team` parameter with your team's 3-letter code:
```
https://your-app.railway.app/api/trmnl?days=7&team=GSW
```

**Common Team Codes**:
- LAL - Los Angeles Lakers
- BOS - Boston Celtics
- GSW - Golden State Warriors
- MIA - Miami Heat
- CHI - Chicago Bulls
- NYK - New York Knicks
- BKN - Brooklyn Nets
- PHI - Philadelphia 76ers
- MIL - Milwaukee Bucks
- PHX - Phoenix Suns

### Modify the Design

Edit the liquid template files in `trmnl/src/`:
- Adjust styles in the `<style>` blocks
- Modify the HTML structure
- Add or remove data fields
- Change fonts, colors, spacing, etc.

## Troubleshooting

### Plugin shows "No Games"
- Check that your API endpoint is accessible
- Verify the `days` parameter allows enough time for games
- Ensure the current period has NBA games (check the season schedule)

### Plugin shows old data
- Increase the refresh interval in TRMNL settings
- Check that your API is returning fresh data
- Verify the NBA API is accessible from your deployment

### Markup doesn't display correctly
- Ensure you copied the complete liquid template
- Check for syntax errors in the liquid code
- Verify all CSS styles are included
- Test locally with `trmnlp serve`

### API returns errors
- Check your deployment logs
- Verify the NBA API is accessible
- Ensure all dependencies are installed
- Check the `config.yaml` settings

## File Structure

```
trmnl/
├── src/
│   ├── full.liquid              # Full screen layout
│   ├── half_horizontal.liquid   # Half screen (horizontal)
│   ├── half_vertical.liquid     # Half screen (vertical)
│   ├── quadrant.liquid          # Quarter screen layout
│   ├── shared.liquid            # Shared components
│   └── settings.yml             # Plugin configuration
└── README.md                    # This file
```

## Resources

- [TRMNL Documentation](https://docs.usetrmnl.com/go/)
- [TRMNL Framework](https://usetrmnl.com/framework)
- [Liquid Template Documentation](https://help.usetrmnl.com/en/articles/10671186-liquid-101)
- [trmnlp GitHub](https://github.com/usetrmnl/trmnlp)

## Support

For issues or questions:
1. Check the main project README
2. Review TRMNL documentation
3. Open an issue in the GitHub repository
4. Contact TRMNL support for display-specific issues

## License

MIT License - Same as the main NBA Game Recommender project
