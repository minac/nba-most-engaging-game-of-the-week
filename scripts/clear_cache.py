#!/usr/bin/env python3
"""Clear NBA game cache on deployment."""
import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.cache import DateBasedCache
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_config():
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Clear cache based on configuration."""
    try:
        config = load_config()
        cache_config = config.get('cache', {})

        if not cache_config.get('enabled', True):
            logger.info("Cache is disabled, nothing to clear")
            return

        cache_dir = cache_config.get('directory', '/tmp/nba_cache')

        logger.info(f"Clearing cache at {cache_dir}")
        cache = DateBasedCache(cache_dir=cache_dir)

        # Get stats before clearing
        stats_before = cache.get_cache_stats()
        logger.info(f"Cache before clearing: {stats_before.get('total_entries', 0)} entries, "
                   f"{stats_before.get('total_size_mb', 0)} MB")

        # Clear all cache
        cache.clear_all()

        logger.info("✅ Cache cleared successfully")

    except Exception as e:
        logger.error(f"❌ Error clearing cache: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
