import sys
from pathlib import Path

# Make tools/ importable so `verify_template`, `collect_links`, `repositorykit` resolve.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
