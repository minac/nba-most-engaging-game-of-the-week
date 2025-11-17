# Tests

See main [README.md](../README.md#testing) for testing commands.

## Test Structure

- `unit/` - Component tests (scorer, client, cache, recommender)
- `integration/` - Interface tests (CLI, API)
- `fixtures/` - Shared test data

Uses real NBA API calls and file I/O. Mocks only for error conditions.
