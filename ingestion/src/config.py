from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

STATS_NZ_SOURCE_FILE = RAW_DATA_DIR / "selected-price-indexes-june-2026.csv"