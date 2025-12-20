from datetime import datetime, tzinfo, timezone
from zoneinfo import ZoneInfo
import re

import polars as pl

__all__ = [
    "extract_iso_date",
    "get_current_date_and_time_str",
    "get_current_date_str",
    "get_current_time_str",
    "parse_iso_date",
    "localize_naive_datetimes",
    "convert_local_datetimes_to_utc",
    "make_naive_df_timezone_aware",
]

LOCAL_TZ = ZoneInfo("Europe/Brussels")

def extract_iso_date(text: str, pattern: str = r'\d{4}-\d{2}-\d{2}') -> str | None:
    # define iso date pattern
    iso_date_pattern = re.compile(pattern)
    # Define the regular expression to match the ISO date
    match = re.search(iso_date_pattern, text)
    # Check if match is found and return the matched string
    if match:
        return match.group(0)
    # Return None if no match is found
    return None

def get_current_date_and_time_str(date_format: str,
                                  time_format: str,
                                  tz: tzinfo = LOCAL_TZ) -> tuple[str, str]:
    """Return the current date and time as a tuple of strings formatted as desired."""
    return (get_current_date_str(date_format, tz), get_current_time_str(time_format, tz))

def get_current_date_str(date_format: str,
                         tz: tzinfo = LOCAL_TZ) -> str:
    """Return the current date as a string formatted as desired."""
    now_datetime = datetime.now(tz)
    return now_datetime.strftime(date_format)

def get_current_time_str(time_format: str,
                         tz: tzinfo = LOCAL_TZ) -> str:
    """Return the current time as a string formatted as desired."""
    now_datetime = datetime.now(tz)
    return now_datetime.strftime(time_format)

def parse_iso_date(date_str: str) -> datetime.date:
    """Parses an ISO date string (YYYY-M-D or YYYY-MM-DD) to a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")


def localize_naive_datetimes(
        naive_list: list[datetime | None],
        tz: str = "Europe/Brussels"
) -> list[datetime | None]:
    """
    Convert a list of naive Python datetime.datetime objects (no tzinfo) into timezone-aware datetimes,
    resolving ambiguous (DST fallback) times automatically so the resulting timeline is non-decreasing.

    Args:
        naive_list (list[datetime | None]): List of naive datetime objects or None values.
        tz (str): Timezone to localize the datetimes to. Default is "Europe/Brussels".

    Returns:
        list[datetime | None]: List of timezone-aware datetime objects in the specified timezone.
    """
    zone = ZoneInfo(tz)
    aware_list = [None] * len(naive_list)
    previous_naive_datetime = None

    for i, current_naive_datetime in enumerate(naive_list):
        # handles None elements
        if current_naive_datetime is None:
            aware_list[i] = None
            continue

        # ensure it's a naive datetime
        if current_naive_datetime.tzinfo is not None:
            raise ValueError(f"Expected naive datetime, got timezone-aware: {current_naive_datetime}")

        # handles first element and any other leading None elements
        if current_naive_datetime is not None and previous_naive_datetime is None:
            previous_naive_datetime = current_naive_datetime
            aware_list[i] = current_naive_datetime.replace(tzinfo=zone, fold=0)
            continue

        # time is moving forward, use fold=0 (earliest)
        if current_naive_datetime > previous_naive_datetime:
            previous_naive_datetime = current_naive_datetime
            aware_list[i] = current_naive_datetime.replace(tzinfo=zone, fold=0)

        # time is moving backwards, either due to DST fallback or out-of-order data, either way if we use fold 1 it is fine
        elif current_naive_datetime <= previous_naive_datetime:
            previous_naive_datetime = current_naive_datetime
            aware_list[i] = current_naive_datetime.replace(tzinfo=zone, fold=1)

    return aware_list


def convert_local_datetimes_to_utc(
        aware_list: list[datetime | None]
) -> list[datetime | None]:
    """
    Convert a list of timezone-aware datetime objects to UTC.

    Args:
        aware_list (list[datetime | None]): List of timezone-aware datetime objects or None values.

    Returns:
        list[datetime | None]: List of datetime objects converted to UTC timezone.
    """
    return [dt.astimezone(timezone.utc) if dt is not None else None for dt in aware_list]


def make_naive_df_timezone_aware(
        df: pl.DataFrame,
        col: str = "datetime_naive",
        tz: str = "Europe/Brussels",
        col_utc: str = "datetime_utc",
        col_local: str = "datetime_local"
) -> pl.DataFrame:
    """
    Convert a column of naive Python datetime.datetime objects (no tzinfo) into timezone-aware datetimes in the given timezone,
    resolving ambiguous (DST fallback) times automatically so the resulting timeline is non-decreasing.

    Note: ambiguous="infer" exists in pandas, but does not in python stdlib or polars. Hence this convoluted implementation.

    Args:
        df (pl.DataFrame): Input DataFrame containing the naive datetime column (Python datetime.datetime objects).
        col (str): Name of the column with naive datetimes. Default is "datetime_naive".
        tz (str): Timezone to localize the datetimes to. Default is "Europe/Brussels".
        col_utc (str): Name for the new UTC datetime column. Default is "datetime_utc".
        col_local (str): Name for the new local timezone-aware datetime column. Default is "datetime_local".

    Returns:
        pl.DataFrame: A new DataFrame with two additional columns:
            - `col_utc`: UTC datetimes (`Datetime[ns, tz="UTC"]`)
            - `col_local`: Local timezone-aware datetimes (`Datetime[ns, tz]`)
        The original column is left untouched.
    """

    # check if the col in this df is already of python datetime type, if not abort
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in DataFrame.")
    col_dtype = df.schema[col]
    if col_dtype not in [pl.Datetime]:
        raise ValueError(f"Column '{col}' must be of type pl.Datetime[ns]. Found: {col_dtype}")
    # check if the name provided in col_utc and col_local already exist in df
    if col_utc in df.columns:
        raise ValueError(f"Column '{col_utc}' already exists in DataFrame.")
    if col_local in df.columns:
        raise ValueError(f"Column '{col_local}' already exists in DataFrame.")

    # get naive datetime list from dataframe
    naive_list = df[col].to_list()

    # convert to timezone-aware datetimes in the specified timezone
    aware_list = localize_naive_datetimes(naive_list, tz)

    # convert to UTC
    aware_list_utc = convert_local_datetimes_to_utc(aware_list)

    # build Polars series
    s_local = pl.Series(name=col_local, values=aware_list, )

    s_utc = pl.Series(name=col_utc, values=aware_list_utc, )

    # add both UTC and local datetimes to dataframe
    df_aware = df.with_columns([s_utc, s_local])

    return df_aware
