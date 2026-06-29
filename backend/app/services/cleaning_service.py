import pandas as pd
import numpy as np
from typing import Optional
import os


def analyze_issues(file_path: str) -> dict:
    df = _read_file(file_path)

    issues = []

    # Missing values
    for col in df.columns:
        missing = int(df[col].isnull().sum())
        if missing > 0:
            dtype = str(df[col].dtype)
            is_numeric = pd.api.types.is_numeric_dtype(df[col])
            issue = {
                "column": col,
                "type": "missing_values",
                "count": missing,
                "percent": round(missing / len(df) * 100, 2),
                "dtype": dtype,
                "suggestions": _get_suggestions(df[col], is_numeric),
            }
            issues.append(issue)

    # Duplicates
    dup_count = int(df.duplicated().sum())

    # Outliers (numeric columns only)
    outlier_info = []
    for col in df.select_dtypes(include=np.number).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = df[(df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)]
        if len(outliers) > 0:
            outlier_info.append({
                "column": col,
                "count": len(outliers),
                "percent": round(len(outliers) / len(df) * 100, 2),
            })

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "missing_issues": issues,
        "duplicate_count": dup_count,
        "outlier_info": outlier_info,
    }


def apply_cleaning(file_path: str, instructions: dict) -> dict:
    df = _read_file(file_path)
    original_rows = len(df)
    changes = []

    # Handle duplicates
    if instructions.get("remove_duplicates"):
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        if removed > 0:
            changes.append(f"Removed {removed} duplicate rows.")

    # Handle missing values per column
    for fix in instructions.get("missing_fixes", []):
        col = fix["column"]
        strategy = fix["strategy"]

        if col not in df.columns:
            continue

        missing_before = df[col].isnull().sum()

        if strategy == "mean" and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
        elif strategy == "median" and pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        elif strategy == "mode":
            df[col] = df[col].fillna(df[col].mode()[0])
        elif strategy == "drop":
            df = df.dropna(subset=[col])
        elif strategy == "constant":
            df[col] = df[col].fillna(fix.get("value", "Unknown"))

        changes.append(f"'{col}': filled {missing_before} missing values using {strategy}.")

    # Save cleaned file
    upload_dir = os.path.dirname(file_path)
    base_name = "cleaned_" + os.path.basename(file_path)
    cleaned_path = os.path.join(upload_dir, base_name)
    # filename_only = os.path.basename(cleaned_path)
    df.to_csv(cleaned_path, index=False)

    return {
        "original_rows": original_rows,
        "cleaned_rows": len(df),
        "rows_removed": original_rows - len(df),
        "changes": changes,
        "cleaned_filename": os.path.basename(cleaned_path),
        "preview": df.head(10).fillna("").to_dict(orient="records"),
        "column_names": df.columns.tolist(),
    }


def _get_suggestions(series: pd.Series, is_numeric: bool) -> list:
    suggestions = []
    if is_numeric:
        suggestions = ["mean", "median", "mode", "drop", "constant"]
    else:
        suggestions = ["mode", "drop", "constant"]
    return suggestions


def _read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")