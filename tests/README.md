# NBA Game Recommender Tests

This directory contains comprehensive tests for the NBA Game Recommender project.

## Test Philosophy

This test suite follows a **real-data-first approach**:

- **Use REAL API calls** for normal functionality tests (validates against actual NBA data)
- **Use MOCKS only** for error conditions that can't be easily triggered (500 errors, timeouts)
- **Use REAL file I/O** for cache tests (validates actual disk operations)
- **Leverage caching** to avoid rate limiting and speed up test execution

This approach ensures tests validate real-world behavior while maintaining good performance.

## Test Structure

```
tests/
├── unit/                      # Unit tests for individual components
│   ├── test_cache.py         # Tests for DateBasedCache (72 tests)
│   ├── test_game_scorer.py   # Tests for GameScorer class
│   ├── test_nba_client.py    # Tests for NBAClient class (uses real API)
│   └── test_recommender.py   # Tests for GameRecommender class
├── integration/               # Integration tests
│   ├── test_api_server.py    # Tests for Flask API endpoints
│   └── test_cli.py           # Tests for CLI interface
├── fixtures/                  # Test fixtures and sample data
│   └── sample_data.py        # Sample data for mocked error tests
└── conftest.py               # Shared pytest fixtures

```

## Running Tests

### Basic Commands

```bash
# Run all tests (includes real API calls)
uv run pytest

# Run all tests without coverage reporting (faster)
uv run pytest --no-cov

# Run with verbose output
uv run pytest -v --no-cov

# Run with output capture disabled (see print statements)
uv run pytest -s --no-cov
```

### Run Specific Test Categories

```bash
# Unit tests only
uv run pytest tests/unit/ --no-cov

# Integration tests only
uv run pytest tests/integration/ --no-cov

# Specific test file
uv run pytest tests/unit/test_game_scorer.py --no-cov

# Specific test class or function
uv run pytest tests/unit/test_game_scorer.py::TestGameScorer::test_lead_changes_scoring -v
```

### Run Tests by Speed

```bash
# Run only fast tests (skip slow API tests)
uv run pytest -m "not slow" --no-cov

# Run only slow tests (real API calls)
uv run pytest -m "slow" --no-cov
```

### Cache Management

```bash
# Run tests with fresh cache (clears before running)
rm -rf /tmp/nba_cache && uv run pytest --no-cov

# Check cache statistics
ls -lh /tmp/nba_cache/scoreboards/
ls -lh /tmp/nba_cache/games/

# Clear cache manually
rm -rf /tmp/nba_cache
```

## Test Coverage

### Coverage by Component

The test suite provides comprehensive coverage:

- **GameScorer** (28 tests): All scoring criteria, edge cases, penalties
- **NBAClient** (18 tests): Real API calls + error handling with mocks
- **DateBasedCache** (72 tests): Real file I/O in temp directories
- **GameRecommender** (19 tests): Game ranking and formatting with mocked client
- **API Server** (25 tests): All endpoints and error handling
- **CLI** (25+ tests): Command-line argument parsing and output

**Total: 125+ tests | 99.2% pass rate**

### Real API vs Mocked Tests

**NBAClient Tests (Real API):**
- ✅ `test_top5_teams_property_fetches_real_data` - Fetches real standings
- ✅ `test_star_players_property_fetches_real_data` - Fetches real league leaders
- ✅ `test_get_games_last_n_days_with_real_api` - Fetches real game data
- ✅ `test_cache_integration_with_real_data` - Tests real cache behavior
- ✅ `test_scoreboard_returns_only_final_games` - Uses real API

**NBAClient Tests (Mocked for Errors):**
- ✅ `test_fetch_top_teams_handles_error` - 500 error handling
- ✅ `test_fetch_star_players_handles_error` - 500 error handling
- ✅ `test_get_game_details_handles_error` - 404 error handling

### Viewing Coverage Reports

```bash
# View coverage in terminal with missing lines
uv run pytest --cov=src --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html  # Opens coverage report in browser

# Generate XML coverage report (for CI/CD)
uv run pytest --cov=src --cov-report=xml
```

## Test Fixtures

Reusable test data is available in `fixtures/sample_data.py`. These are used **sparingly**, primarily for:
- Mocking error responses from NBA API
- Testing data transformation logic
- Providing sample configurations

### Available Fixtures

- `get_sample_game()`: Creates sample game data with customizable parameters
- `get_sample_config()`: Provides default scoring configuration
- `get_sample_scoreboard_response()`: Mock NBA API scoreboard response (for error tests)
- `get_sample_playbyplay_response()`: Mock play-by-play data (for error tests)
- `get_sample_boxscore_response()`: Mock box score with star players (for error tests)
- `get_sample_standings_response()`: Mock standings response (for error tests)
- `get_sample_league_leaders_response()`: Mock league leaders (for error tests)

### Shared Fixtures (conftest.py)

- `temp_cache_dir`: Provides temporary cache directory for cache tests
- `sample_config`: Default scoring configuration
- `top5_teams`: Sample set of top 5 teams
- `star_players`: Sample set of star players
- `mock_nba_api_responses`: Full set of mocked API responses (for error scenarios)

## Writing New Tests

### Example Unit Test (No Mocks)

```python
from src.core.game_scorer import GameScorer
from tests.fixtures.sample_data import get_sample_game, get_sample_config

def test_score_calculation():
    """Test scoring calculation with sample data."""
    scorer = GameScorer(get_sample_config())
    game = get_sample_game(lead_changes=10)
    result = scorer.score_game(game)

    assert result['score'] > 0
    assert result['breakdown']['lead_changes']['count'] == 10
```

### Example API Test (Real API)

```python
from src.api.nba_client import NBAClient

def test_real_api_call():
    """Test with real NBA API call."""
    client = NBAClient()

    # This makes a REAL API call
    top_teams = client.TOP_5_TEAMS

    assert isinstance(top_teams, set)
    assert len(top_teams) == 5
```

### Example Error Handling Test (Mocked)

```python
import responses
from src.api.nba_client import NBAClient

@responses.activate
def test_api_error_handling():
    """Test error handling with mocked error response."""
    responses.add(
        responses.GET,
        'https://stats.nba.com/stats/leaguestandingsv3',
        json={'error': 'Server error'},
        status=500
    )

    client = NBAClient()
    teams = client.TOP_5_TEAMS

    # Should return fallback without crashing
    assert isinstance(teams, set)
    assert len(teams) == 5
```

### Example Cache Test (Real File I/O)

```python
from src.utils.cache import DateBasedCache

def test_cache_persistence(temp_cache_dir):
    """Test cache with real file operations."""
    cache = DateBasedCache(cache_dir=temp_cache_dir)

    # Write to real temp directory
    cache.set_scoreboard('2024-01-15', [{'game_id': '001'}])

    # Read from real temp directory
    data = cache.get_scoreboard('2024-01-15')

    assert data == [{'game_id': '001'}]
```

### Example Integration Test

```python
from src.interfaces.api_server import app

def test_api_endpoint():
    """Test Flask API endpoint."""
    client = app.test_client()
    response = client.get('/api/health')

    assert response.status_code == 200
    assert response.json['status'] == 'ok'
```

## Performance Considerations

### Cache Benefits

The test suite uses a persistent cache (`/tmp/nba_cache`) that:
- **Reduces API calls**: Subsequent test runs use cached data
- **Avoids rate limiting**: NBA API won't throttle repeated test runs
- **Speeds up execution**: Cached tests run ~10x faster
- **Enables offline testing**: Can run tests without internet after first run

### Slow Tests

Tests marked with `@pytest.mark.slow` make real API calls:
- First run: ~5-10 seconds (fetches data from NBA API)
- Subsequent runs: <1 second (uses cache)

Skip slow tests during rapid development:
```bash
uv run pytest -m "not slow" --no-cov
```

## Dependencies

Test dependencies are managed in `pyproject.toml`:
- `pytest>=7.4.0`: Test framework
- `pytest-cov>=4.1.0`: Coverage plugin
- `pytest-mock>=3.11.0`: Mocking utilities
- `responses>=0.23.0`: HTTP response mocking (for error tests)
- `freezegun>=1.2.0`: Time mocking (if needed)

Install test dependencies:
```bash
uv sync --extra test
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    uv sync --extra test
    uv run pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're using `uv run`:
```bash
uv run pytest  # Correct - uses project's virtual environment
pytest         # May fail - uses system Python
```

### API Rate Limiting
If you hit NBA API rate limits:
```bash
# Let cache persist (it already does by default)
uv run pytest --no-cov

# Or wait 60 seconds between test runs
```

### Cache Issues
If you suspect cache corruption:
```bash
# Clear cache and re-run
rm -rf /tmp/nba_cache
uv run pytest --no-cov
```

### Coverage Not Working
Ensure pytest-cov is installed:
```bash
uv sync --extra test
uv run pytest --cov=src
```

### Mock Issues for Error Tests
When mocking for error conditions:
- Patch where the object is **used**, not where it's defined
- Use `@responses.activate` decorator for HTTP mocking
- Create fresh instances after mocking to trigger the mock

## Test Execution Times

Approximate execution times:

| Command | Time (First Run) | Time (Cached) |
|---------|------------------|---------------|
| All tests | ~10 seconds | ~3 seconds |
| Unit tests only | ~8 seconds | ~2 seconds |
| Fast tests only | ~2 seconds | ~1 second |
| Single test file | ~1-3 seconds | <1 second |

*Times assume normal NBA API response times and working cache*
