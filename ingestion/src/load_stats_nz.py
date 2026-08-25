import pandas as pd

from config import STATS_NZ_SOURCE_FILE
from validate_data import validate_required_columns


def load_stats_nz_data() -> pd.DataFrame:
    return pd.read_csv(STATS_NZ_SOURCE_FILE)


if __name__ == "__main__":
    df = load_stats_nz_data()

    validate_required_columns(df)

    print("Required column validation: PASSED")
    print(f"Rows loaded: {len(df):,}")
    print(f"Columns: {len(df.columns)}")