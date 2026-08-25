import os

import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

from config import STATS_NZ_SOURCE_FILE
from load_stats_nz import load_stats_nz_data, parse_period
from validate_data import (
    standardise_missing_values,
    validate_data_types,
    validate_duplicate_records,
    validate_invalid_values,
    validate_required_columns,
)

load_dotenv()


def prepare_raw_data() -> pd.DataFrame:
    df = load_stats_nz_data()

    validate_required_columns(df)
    df = standardise_missing_values(df)
    validate_data_types(df)
    validate_duplicate_records(df)
    validate_invalid_values(df)
    df = parse_period(df)

    raw_df = df.drop(columns=["Period_date"]).rename(
        columns={
            "Series_reference": "SERIES_REFERENCE",
            "Period": "PERIOD",
            "Data_value": "DATA_VALUE",
            "STATUS": "STATUS",
            "UNITS": "UNITS",
            "Subject": "SUBJECT",
            "Group": "GROUP_NAME",
            "Series_title_1": "SERIES_TITLE_1",
            "Series_title_2": "SERIES_TITLE_2",
            "Series_title_3": "SERIES_TITLE_3",
        }
    )

    raw_df["SOURCE_FILE"] = STATS_NZ_SOURCE_FILE.name

    return raw_df


def load_to_snowflake(df: pd.DataFrame) -> int:
    connection = snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )

    try:
        success, _, rows_loaded, _ = write_pandas(
            connection,
            df,
            "STATS_NZ_SELECTED_PRICE_INDEXES",
            database=os.environ["SNOWFLAKE_DATABASE"],
            schema=os.environ["SNOWFLAKE_SCHEMA"],
            quote_identifiers=False,
            auto_create_table=False,
        )

        if not success:
            raise RuntimeError("Snowflake load failed.")

        return rows_loaded
    finally:
        connection.close()


if __name__ == "__main__":
    raw_df = prepare_raw_data()
    rows_loaded = load_to_snowflake(raw_df)
    print(f"Snowflake RAW load: PASSED ({rows_loaded:,} rows loaded)")