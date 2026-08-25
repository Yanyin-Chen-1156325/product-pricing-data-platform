import pandas as pd


REQUIRED_COLUMNS = [
    "Series_reference",
    "Period",
    "Data_value",
    "STATUS",
    "UNITS",
    "Subject",
    "Group",
    "Series_title_1",
    "Series_title_2",
    "Series_title_3",
]

MISSING_VALUE_MARKERS = {"", "NA", "N/A", "NULL", "NONE"}
ALLOWED_STATUS_VALUES = {"FINAL", "REVISED"}
ALLOWED_UNIT_VALUES = {"Dollars", "Index", "Percent"}


def standardise_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace blank and common text missing-value markers with ``pd.NA``."""
    standardised_df = df.copy()
    text_columns = standardised_df.select_dtypes(include=["object", "string"]).columns

    for column in text_columns:
        text_values = standardised_df[column].astype("string")
        normalised_values = text_values.str.strip().str.upper()
        standardised_df[column] = text_values.mask(
            normalised_values.isin(MISSING_VALUE_MARKERS)
        )

    return standardised_df


def validate_duplicate_records(df: pd.DataFrame) -> None:
    """Reject exact duplicate records and duplicate Stats NZ series-month keys."""
    exact_duplicates = df.duplicated()
    if exact_duplicates.any():
        duplicate_rows = df.index[exact_duplicates].tolist()
        raise ValueError(f"Exact duplicate records found at rows: {duplicate_rows}")

    duplicate_keys = df.duplicated(["Series_reference", "Period"])
    if duplicate_keys.any():
        duplicate_rows = df.index[duplicate_keys].tolist()
        raise ValueError(
            "Duplicate Series_reference + Period records found at rows: "
            f"{duplicate_rows}"
        )


def validate_invalid_values(df: pd.DataFrame) -> None:
    """Validate source-controlled categorical values and value-unit combinations."""
    invalid_status = ~df["STATUS"].isin(ALLOWED_STATUS_VALUES)
    if invalid_status.any():
        invalid_rows = df.index[invalid_status].tolist()
        raise ValueError(f"STATUS contains invalid values at rows: {invalid_rows}")

    invalid_units = ~df["UNITS"].isin(ALLOWED_UNIT_VALUES)
    if invalid_units.any():
        invalid_rows = df.index[invalid_units].tolist()
        raise ValueError(f"UNITS contains invalid values at rows: {invalid_rows}")

    invalid_numeric_values = (
        df["UNITS"].isin({"Dollars", "Index"})
        & df["Data_value"].notna()
        & (pd.to_numeric(df["Data_value"], errors="coerce") < 0)
    )
    if invalid_numeric_values.any():
        invalid_rows = df.index[invalid_numeric_values].tolist()
        raise ValueError(
            "Dollars and Index Data_value values cannot be negative at rows: "
            f"{invalid_rows}"
        )


def validate_data_types(df: pd.DataFrame) -> None:
    """Validate fields that must be parseable for downstream processing.

    ``Data_value`` may be missing in the Stats NZ source, so only non-null
    values are required to be numeric. ``Period`` represents a year and month
    (for example, ``2024.1`` or ``2024.01``), not a decimal year.
    """
    data_values = pd.to_numeric(df["Data_value"], errors="coerce")
    invalid_data_values = df["Data_value"].notna() & data_values.isna()

    if invalid_data_values.any():
        invalid_rows = df.index[invalid_data_values].tolist()
        raise ValueError(
            "Data_value contains non-numeric values at rows: "
            f"{invalid_rows}"
        )

    period_parts = (
        df["Period"]
        .astype("string")
        .str.strip()
        .str.extract(r"^(?P<year>\d{4})\.(?P<month>\d{1,2})$")
    )
    valid_month = pd.to_numeric(period_parts["month"], errors="coerce").between(1, 12)
    invalid_periods = period_parts.isna().any(axis=1) | ~valid_month

    if invalid_periods.any():
        invalid_rows = df.index[invalid_periods].tolist()
        raise ValueError(
            "Period must use a valid YYYY.M or YYYY.MM year-month format at rows: "
            f"{invalid_rows}"
        )


def validate_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


if __name__ == "__main__":
    print("Required columns configured:")
    for column in REQUIRED_COLUMNS:
        print(f"- {column}")
