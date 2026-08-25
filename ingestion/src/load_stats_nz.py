import pandas as pd

from config import STATS_NZ_SOURCE_FILE
from validate_data import (
    standardise_missing_values,
    validate_data_types,
    validate_duplicate_records,
    validate_invalid_values,
    validate_required_columns,
)


def load_stats_nz_data() -> pd.DataFrame:
    return pd.read_csv(STATS_NZ_SOURCE_FILE)


def parse_period(df: pd.DataFrame) -> pd.DataFrame:
    """Add a month-start date parsed from the Stats NZ ``Period`` field."""
    parsed_df = df.copy()
    period_parts = (
        parsed_df["Period"]
        .astype("string")
        .str.strip()
        .str.extract(r"^(?P<year>\d{4})\.(?P<month>\d{1,2})$")
    )

    parsed_df["Period_date"] = pd.to_datetime(
        {
            "year": period_parts["year"].astype(int),
            "month": period_parts["month"].astype(int),
            "day": 1,
        }
    )
    return parsed_df


def produce_ingestion_summary(df: pd.DataFrame) -> str:
    """Return a concise, human-readable summary of the validated source data."""
    status_counts = df["STATUS"].value_counts().sort_index()
    unit_counts = df["UNITS"].value_counts().sort_index()
    period_start = df["Period_date"].min().date().isoformat()
    period_end = df["Period_date"].max().date().isoformat()

    lines = [
        "Ingestion summary",
        "-----------------",
        f"Rows processed: {len(df):,}",
        f"Columns after parsing: {len(df.columns)}",
        f"Unique series: {df['Series_reference'].nunique():,}",
        f"Period range: {period_start} to {period_end}",
        f"Missing Data_value: {df['Data_value'].isna().sum():,}",
        "STATUS distribution:",
    ]
    lines.extend(f"  - {status}: {count:,}" for status, count in status_counts.items())
    lines.append("UNITS distribution:")
    lines.extend(f"  - {unit}: {count:,}" for unit, count in unit_counts.items())

    return "\n".join(lines)


if __name__ == "__main__":
    df = load_stats_nz_data()

    validate_required_columns(df)
    df = standardise_missing_values(df)
    validate_data_types(df)
    validate_duplicate_records(df)
    validate_invalid_values(df)
    df = parse_period(df)

    print("Required column validation: PASSED")
    print("Missing value standardisation: PASSED")
    print("Data type validation: PASSED")
    print("Duplicate record validation: PASSED")
    print("Invalid value validation: PASSED")
    print("Period parsing: PASSED")
    print()
    print(produce_ingestion_summary(df))
