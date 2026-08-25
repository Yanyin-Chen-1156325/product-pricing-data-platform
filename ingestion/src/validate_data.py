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