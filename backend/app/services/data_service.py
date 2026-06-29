import pandas as pd
import numpy as np


def load_dataset(file_path: str) -> dict:
    df = _read_file(file_path)
    return get_summary(file_path, df)


def get_summary(file_path: str, df: pd.DataFrame = None) -> dict:
    if df is None:
        df = _read_file(file_path)

    summary = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percent": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "numeric_columns": df.select_dtypes(include=np.number).columns.tolist(),
        "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
        "preview": df.head(10).fillna("").to_dict(orient="records"),
    }

    return summary


def _read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")