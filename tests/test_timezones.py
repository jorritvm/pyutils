import pytest
import polars as pl
from datetime import datetime, timezone
from pyutils.time import make_naive_df_timezone_aware

# 1. Simple consecutive dates
def test_simple_consecutive_dates():
    naive_datetimes = [
        datetime(2023, 1, 1, 12, 0),
        datetime(2023, 1, 2, 12, 0),
        datetime(2023, 1, 3, 12, 0),
    ]
    df = pl.DataFrame({"datetime_naive": naive_datetimes})
    df_aware = make_naive_df_timezone_aware(df)
    assert "datetime_utc" in df_aware.columns
    assert "datetime_local" in df_aware.columns
    # Check monotonicity
    utc_vals = [dt for dt in df_aware["datetime_utc"] if dt is not None]
    assert all(earlier <= later for earlier, later in zip(utc_vals, utc_vals[1:]))

# 2. Edge case: empty dataframe
def test_empty_dataframe():
    df = pl.DataFrame({"datetime_naive": pl.Series([], dtype=pl.Datetime)})
    df_aware = make_naive_df_timezone_aware(df)
    assert df_aware.shape[0] == 0
    assert "datetime_utc" in df_aware.columns
    assert "datetime_local" in df_aware.columns

# 3. Edge case: only None
def test_only_none():
    df = pl.DataFrame({"datetime_naive": pl.Series([None, None], dtype=pl.Datetime)})
    df_aware = make_naive_df_timezone_aware(df)
    assert df_aware["datetime_utc"].to_list() == [None, None]
    assert df_aware["datetime_local"].to_list() == [None, None]

# 4. Edge case: leading None
def test_leading_none():
    naive_datetimes = [None, datetime(2023, 1, 1, 12, 0), datetime(2023, 1, 2, 12, 0)]
    df = pl.DataFrame({"datetime_naive": naive_datetimes})
    df_aware = make_naive_df_timezone_aware(df)
    assert df_aware["datetime_utc"][0] is None
    assert df_aware["datetime_local"][0] is None
    assert df_aware["datetime_utc"][1] is not None
    assert df_aware["datetime_local"][1] is not None

# 5. Edge case: intermittent None
def test_intermittent_none():
    naive_datetimes = [datetime(2023, 1, 1, 12, 0), None, datetime(2023, 1, 3, 12, 0)]
    df = pl.DataFrame({"datetime_naive": naive_datetimes})
    df_aware = make_naive_df_timezone_aware(df)
    assert df_aware["datetime_utc"][1] is None
    assert df_aware["datetime_local"][1] is None

# 6. Edge case: datetime that is already tz aware
def test_tz_aware_datetime_raises():
    aware_dt = datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)
    df = pl.DataFrame({"datetime_naive": [aware_dt]})
    with pytest.raises(ValueError):
        make_naive_df_timezone_aware(df)

# 7. Edge case: columns that already exist
def test_columns_already_exist():
    naive_datetimes = [datetime(2023, 1, 1, 12, 0)]
    df = pl.DataFrame({
        "datetime_naive": naive_datetimes,
        "datetime_utc": [None],
        "datetime_local": [None],
    })
    with pytest.raises(ValueError):
        make_naive_df_timezone_aware(df)

# 8. Out of order data
def test_out_of_order_data():
    naive_datetimes = [
        datetime(2023, 1, 3, 12, 0),
        datetime(2023, 1, 1, 12, 0),
        datetime(2023, 1, 2, 12, 0),
    ]
    df = pl.DataFrame({"datetime_naive": naive_datetimes})
    df_aware = make_naive_df_timezone_aware(df)
    utc_vals = [dt for dt in df_aware["datetime_utc"] if dt is not None]
    print(utc_vals)
    assert not all(earlier <= later for earlier, later in zip(utc_vals, utc_vals[1:]))

# 9. Ambiguous dates (CEST -> CET transition)
def test_ambiguous_dates_dst_fallback():
    # 2023-10-29 02:30 occurs twice in Europe/Brussels
    naive_datetimes = [
        datetime(2023, 10, 29, 0, 30),
        datetime(2023, 10, 29, 1, 30),
        datetime(2023, 10, 29, 2, 30),
        datetime(2023, 10, 29, 2, 30),
        datetime(2023, 10, 29, 3, 30),
    ]
    df = pl.DataFrame({"datetime_naive": naive_datetimes})
    df_aware = make_naive_df_timezone_aware(df, tz="Europe/Brussels")
    utc_vals = [dt for dt in df_aware["datetime_utc"] if dt is not None]
    # The two ambiguous 2:30 times should have different UTC values, and the second should be later
    assert utc_vals[2] < utc_vals[3]
    # All UTC values should be monotonic
    assert all(earlier <= later for earlier, later in zip(utc_vals, utc_vals[1:]))

