import pandas as pd

def load_and_prepare_data(csv_path: str) -> pd.DataFrame:
    """Return a DataFrame with extra date-part columns added."""
    df = pd.read_csv(csv_path)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["quarter"] = df["date"].dt.quarter
        df["month"] = df["date"].dt.month
        df["year"] = df["date"].dt.year

    return df


def make_schema_text(df: pd.DataFrame) -> str:
    """Return a human-readable column -> dtype listing to pass into LLM prompts."""
    return "\n".join(f"- {c}: {dt}" for c, dt in df.dtypes.items())
