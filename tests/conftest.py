import sys
from pathlib import Path

# Ensure project root and src directory are on sys.path so tests can import `src`.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))
