"""
Feature blueprint for Illinois Lucky Day Lotto (5 of 45, midday/evening).

Each row = one draw.
This file defines:
- Raw input schema
- Engineered feature groups
- Target schema
- Skeleton functions to compute features
"""

from dataclasses import dataclass
from typing import List
import pandas as pd
import numpy as np


# ---------- 1. Raw schema ----------

RAW_COLUMNS = [
    "draw_id",
    "draw_date",   # datetime
    "draw_time",   # "MIDDAY" / "EVENING" or datetime.time
    "n1", "n2", "n3", "n4", "n5",
]


# ---------- 2. Feature groups ----------

TEMPORAL_FEATURES = [
    "year",
    "month",
    "day",
    "day_of_week",
    "month_sin", "month_cos",
    "dow_sin", "dow_cos",
    "is_midday",
    "is_evening",
    "draw_index",
    "days_since_start",
]

POSITIONAL_FEATURES = [
    "s1", "s2", "s3", "s4", "s5",
    "s1_norm", "s2_norm", "s3_norm", "s4_norm", "s5_norm",
]

FREQUENCY_FEATURES = (
    [f"freq_global_{i}" for i in range(1, 46)] +
    [f"freq_25_{i}" for i in range(1, 46)] +
    [f"skip_{i}" for i in range(1, 46)] +
    [f"streak_{i}" for i in range(1, 46)]
)

NUMERIC_REL_FEATURES = [
    "sum_numbers",
    "mean_numbers",
    "var_numbers",
    "gap_12", "gap_23", "gap_34", "gap_45",
    "range_numbers",
    "count_odd", "count_even",
    "count_low", "count_high",
    "max_gap",
    "repeat_count_prev",
]

META_FEATURES = [
    "entropy_like",
    "sum_delta_prev",
]

TARGET_COLUMNS = [f"y_{i}" for i in range(1, 46)]


# ---------- 3. Blueprint container ----------

@dataclass
class FeatureBlueprint:
    raw_columns: List[str]
    temporal: List[str]
    positional: List[str]
    frequency: List[str]
    numeric_rel: List[str]
    meta: List[str]
    targets: List[str]

    @property
    def all_features(self) -> List[str]:
        return (
            self.temporal
            + self.positional
            + self.frequency
            + self.numeric_rel
            + self.meta
        )


BLUEPRINT = FeatureBlueprint(
    raw_columns=RAW_COLUMNS,
    temporal=TEMPORAL_FEATURES,
    positional=POSITIONAL_FEATURES,
    frequency=FREQUENCY_FEATURES,
    numeric_rel=NUMERIC_REL_FEATURES,
    meta=META_FEATURES,
    targets=TARGET_COLUMNS,
)


# ---------- 4. Skeleton feature functions ----------

def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add year, month, dow, cyclical encodings, draw_index, etc."""
    df = df.copy()

    df["draw_date"] = pd.to_datetime(df["draw_date"])
    df["year"] = df["draw_date"].dt.year
    df["month"] = df["draw_date"].dt.month
    df["day"] = df["draw_date"].dt.day
    df["day_of_week"] = df["draw_date"].dt.dayofweek

    # Cyclical encodings
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    # Midday / evening flags (adjust if your raw format differs)
    df["is_midday"] = (df["draw_time"].astype(str).str.upper() == "MIDDAY").astype(int)
    df["is_evening"] = (df["draw_time"].astype(str).str.upper() == "EVENING").astype(int)

    # Draw index and days since start
    df = df.sort_values("draw_date").reset_index(drop=True)
    df["draw_index"] = np.arange(1, len(df) + 1)
    df["days_since_start"] = (df["draw_date"] - df["draw_date"].min()).dt.days

    return df


def add_positional_features(df: pd.DataFrame) -> pd.DataFrame:
    """Sort n1..n5 into s1..s5 and add normalized versions."""
    df = df.copy()

    nums = df[["n1", "n2", "n3", "n4", "n5"]].values
    nums_sorted = np.sort(nums, axis=1)
    for i in range(5):
        df[f"s{i+1}"] = nums_sorted[:, i]

    # Normalize (1–45)
    df[[f"s{i}_norm" for i in range(1, 6)]] = (
        df[[f"s{i}" for i in range(1, 6)]] - 1
    ) / 44.0

    return df


def add_numeric_relationship_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add sum, gaps, parity, low/high counts, etc."""
    df = df.copy()

    s_cols = [f"s{i}" for i in range(1, 6)]
    df["sum_numbers"] = df[s_cols].sum(axis=1)
    df["mean_numbers"] = df[s_cols].mean(axis=1)
    df["var_numbers"] = df[s_cols].var(axis=1)

    df["gap_12"] = df["s2"] - df["s1"]
    df["gap_23"] = df["s3"] - df["s2"]
    df["gap_34"] = df["s4"] - df["s3"]
    df["gap_45"] = df["s5"] - df["s4"]

    df["range_numbers"] = df["s5"] - df["s1"]

    df["count_odd"] = df[s_cols].apply(lambda row: (row % 2 != 0).sum(), axis=1)
    df["count_even"] = 5 - df["count_odd"]

    df["count_low"] = df[s_cols].apply(lambda row: (row <= 22).sum(), axis=1)
    df["count_high"] = 5 - df["count_low"]

    df["max_gap"] = df[["gap_12", "gap_23", "gap_34", "gap_45"]].max(axis=1)

    # Repeat count from previous draw
    df["repeat_count_prev"] = 0
    for idx in range(1, len(df)):
        prev_set = set(df.loc[idx - 1, s_cols])
        curr_set = set(df.loc[idx, s_cols])
        df.loc[idx, "repeat_count_prev"] = len(prev_set & curr_set)

    # Placeholder for entropy-like feature
    df["entropy_like"] = np.nan  # TODO: define if you want

    # Placeholder for sum delta vs previous
    df["sum_delta_prev"] = df["sum_numbers"].diff().fillna(0)

    return df


def add_frequency_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add frequency, rolling frequency, skip, streak features.
    This is a bit heavier; start simple and extend.
    """
    df = df.copy()

    # Initialize columns
    for i in range(1, 46):
        df[f"freq_global_{i}"] = 0
        df[f"freq_25_{i}"] = 0
        df[f"skip_{i}"] = 0
        df[f"streak_{i}"] = 0

    # We'll maintain running stats as we iterate chronologically
    df = df.sort_values("draw_date").reset_index(drop=True)

    global_counts = {i: 0 for i in range(1, 46)}
    last_seen = {i: None for i in range(1, 46)}
    streaks = {i: 0 for i in range(1, 46)}

    window_size = 25
    history_numbers = []  # list of sets of numbers for last window_size draws

    for idx, row in df.iterrows():
        current_nums = set(int(x) for x in row[["n1", "n2", "n3", "n4", "n5"]])

        # Update global counts and streaks
        for i in range(1, 46):
            appeared = i in current_nums

            # freq_global
            df.at[idx, f"freq_global_{i}"] = global_counts[i]

            # rolling freq_25
            recent_count = sum(i in s for s in history_numbers[-window_size:])
            df.at[idx, f"freq_25_{i}"] = recent_count

            # skip
            if last_seen[i] is None:
                df.at[idx, f"skip_{i}"] = idx  # or np.nan for "never seen"
            else:
                df.at[idx, f"skip_{i}"] = idx - last_seen[i]

            # streak
            df.at[idx, f"streak_{i}"] = streaks[i]

            # Update state AFTER writing features
            if appeared:
                global_counts[i] += 1
                last_seen[i] = idx
                streaks[i] += 1
            else:
                streaks[i] = 0

        # Update rolling window
        history_numbers.append(current_nums)

    return df


def add_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Create y_1..y_45 multi-label targets."""
    df = df.copy()
    nums_cols = ["n1", "n2", "n3", "n4", "n5"]

    for i in range(1, 46):
        df[f"y_{i}"] = df[nums_cols].apply(lambda row: int(i in set(row)), axis=1)

    return df


def build_feature_matrix(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    High-level pipeline:
    - assumes df_raw has RAW_COLUMNS
    - returns df with all features + targets
    """
    df = df_raw.copy()

    df = add_temporal_features(df)
    df = add_positional_features(df)
    df = add_numeric_relationship_features(df)
    df = add_frequency_features(df)
    df = add_targets(df)

    return df