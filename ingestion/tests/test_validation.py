from pathlib import Path
import sys

import pandas as pd
import pytest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from load_stats_nz import parse_period, produce_ingestion_summary
from validate_data import (
    standardise_missing_values,
    validate_data_types,
    validate_duplicate_records,
    validate_invalid_values,
    validate_required_columns,
)

def test_validate_required_columns_accepts_complete_schema() -> None:
    df = pd.DataFrame(columns=[
        "Series_reference", "Period", "Data_value", "STATUS", "UNITS",
        "Subject", "Group", "Series_title_1", "Series_title_2",
        "Series_title_3",
    ])

    validate_required_columns(df)


def test_validate_required_columns_rejects_missing_column() -> None:
    df = pd.DataFrame(columns=["Series_reference", "Period"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(df)

def test_validate_data_types_accepts_valid_values_and_missing_data_value() -> None:
    df = pd.DataFrame(
        {
            "Data_value": [12.5, "8.25", None],
            "Period": ["2024.01", "2024.1", "2024.12"],
        }
    )

    validate_data_types(df)


def test_validate_data_types_rejects_non_numeric_data_value() -> None:
    df = pd.DataFrame(
        {
            "Data_value": ["not-a-number"],
            "Period": ["2024.01"],
        }
    )

    with pytest.raises(ValueError, match="Data_value contains non-numeric values"):
        validate_data_types(df)


@pytest.mark.parametrize("period", ["2024.00", "2024.13", "2024.1.5", "January 2024"])
def test_validate_data_types_rejects_invalid_period(period: str) -> None:
    df = pd.DataFrame({"Data_value": [12.5], "Period": [period]})

    with pytest.raises(ValueError, match="Period must use a valid"):
        validate_data_types(df)


def test_parse_period_adds_month_start_date_and_preserves_source_period() -> None:
    df = pd.DataFrame({"Period": ["2024.01", "2024.1", "2024.12"]})

    parsed_df = parse_period(df)

    assert parsed_df["Period"].tolist() == ["2024.01", "2024.1", "2024.12"]
    assert parsed_df["Period_date"].tolist() == [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-12-01"),
    ]


def test_produce_ingestion_summary_includes_key_metrics() -> None:
    df = pd.DataFrame(
        {
            "Series_reference": ["SERIES_A", "SERIES_A", "SERIES_B"],
            "Period_date": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-02-01"]),
            "Data_value": [1.0, None, 2.0],
            "STATUS": ["FINAL", "REVISED", "FINAL"],
            "UNITS": ["Dollars", "Dollars", "Index"],
        }
    )

    summary = produce_ingestion_summary(df)

    assert "Rows processed: 3" in summary
    assert "Unique series: 2" in summary
    assert "Period range: 2024-01-01 to 2024-02-01" in summary
    assert "Missing Data_value: 1" in summary
    assert "  - FINAL: 2" in summary
    assert "  - Dollars: 2" in summary


def test_standardise_missing_values_replaces_blank_text_markers() -> None:
    df = pd.DataFrame({"title": ["NA", "  ", "Product"], "value": [None, 1, 2]})

    standardised_df = standardise_missing_values(df)

    assert standardised_df["title"].isna().tolist() == [True, True, False]
    assert standardised_df["title"].iloc[2] == "Product"
    assert standardised_df["value"].isna().tolist() == [True, False, False]


def test_validate_duplicate_records_rejects_exact_duplicate() -> None:
    df = pd.DataFrame(
        {
            "Series_reference": ["CPIM.SE901", "CPIM.SE901"],
            "Period": ["2024.01", "2024.01"],
            "Data_value": [100.0, 100.0],
        }
    )

    with pytest.raises(ValueError, match="Exact duplicate records"):
        validate_duplicate_records(df)


def test_validate_duplicate_records_rejects_duplicate_natural_key() -> None:
    df = pd.DataFrame(
        {
            "Series_reference": ["CPIM.SE901", "CPIM.SE901"],
            "Period": ["2024.01", "2024.01"],
            "Data_value": [100.0, 101.0],
        }
    )

    with pytest.raises(ValueError, match="Duplicate Series_reference"):
        validate_duplicate_records(df)


@pytest.mark.parametrize(
    ("column", "value", "error_message"),
    [
        ("STATUS", "PRELIMINARY", "STATUS contains invalid values"),
        ("UNITS", "Euros", "UNITS contains invalid values"),
    ],
)
def test_validate_invalid_values_rejects_unknown_categorical_values(
    column: str, value: str, error_message: str
) -> None:
    df = pd.DataFrame(
        {
            "STATUS": ["FINAL"],
            "UNITS": ["Dollars"],
            "Data_value": [12.5],
        }
    )
    df.loc[0, column] = value

    with pytest.raises(ValueError, match=error_message):
        validate_invalid_values(df)


def test_validate_invalid_values_rejects_negative_dollar_value() -> None:
    df = pd.DataFrame(
        {
            "STATUS": ["FINAL"],
            "UNITS": ["Dollars"],
            "Data_value": [-1.0],
        }
    )

    with pytest.raises(ValueError, match="cannot be negative"):
        validate_invalid_values(df)
