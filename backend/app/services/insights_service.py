import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


def generate_insights(file_path: str) -> dict:
    df = _read_file(file_path)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
    }

    if numeric_cols:
        desc = df[numeric_cols].describe().round(2)
        profile["numeric_stats"] = desc.to_dict()

    cat_counts = {}
    for col in categorical_cols[:4]:
        cat_counts[col] = df[col].value_counts().head(5).to_dict()
    profile["categorical_counts"] = cat_counts

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().round(2)
        profile["correlations"] = corr.to_dict()

    if GEMINI_AVAILABLE:
        try:
            return _call_gemini(profile)
        except Exception:
            pass

    return _generate_statistical_insights(df, profile, numeric_cols, categorical_cols)


def _call_gemini(profile: dict) -> dict:
    prompt = f"""..."""  # keep your existing prompt
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def _generate_statistical_insights(df, profile, numeric_cols, categorical_cols) -> dict:
    insights = []
    recommendations = []

    total_missing = sum(profile["missing_values"].values())
    missing_pct = round(total_missing / (profile["rows"] * profile["columns"]) * 100, 1)

    if missing_pct == 0:
        insights.append({
            "title": "Complete Dataset",
            "description": f"The dataset contains {profile['rows']} rows and {profile['columns']} columns with no missing values — excellent data quality.",
            "type": "positive"
        })
    else:
        insights.append({
            "title": "Missing Data Detected",
            "description": f"{total_missing} missing values found across {profile['columns']} columns ({missing_pct}% of all data points).",
            "type": "warning"
        })
        recommendations.append("Address missing values using appropriate imputation strategies before modeling.")

    if numeric_cols:
        stats = profile.get("numeric_stats", {})
        for col in numeric_cols[:2]:
            if col in stats and "mean" in stats[col] and "std" in stats[col]:
                mean = stats[col]["mean"]
                std = stats[col]["std"]
                cv = round((std / mean) * 100, 1) if mean != 0 else 0
                insights.append({
                    "title": f"{col.title()} Distribution",
                    "description": f"'{col}' has a mean of {mean} with standard deviation {std} (coefficient of variation: {cv}%).",
                    "type": "neutral"
                })

    if len(numeric_cols) >= 2 and "correlations" in profile:
        corr = profile["correlations"]
        strongest = None
        strongest_val = 0
        for c1 in numeric_cols:
            for c2 in numeric_cols:
                if c1 != c2 and c1 in corr and c2 in corr[c1]:
                    val = abs(corr[c1][c2])
                    if val > strongest_val:
                        strongest_val = val
                        strongest = (c1, c2, corr[c1][c2])
        if strongest:
            direction = "positive" if strongest[2] > 0 else "negative"
            strength = "strong" if strongest_val > 0.7 else "moderate" if strongest_val > 0.4 else "weak"
            insights.append({
                "title": "Correlation Found",
                "description": f"'{strongest[0]}' and '{strongest[1]}' show a {strength} {direction} correlation (r={round(strongest[2], 2)}).",
                "type": "positive" if strongest_val > 0.5 else "neutral"
            })
            recommendations.append(f"Investigate the relationship between '{strongest[0]}' and '{strongest[1]}' for predictive modeling.")

    if categorical_cols:
        col = categorical_cols[0]
        counts = profile.get("categorical_counts", {}).get(col, {})
        if counts:
            top_val = list(counts.keys())[0]
            top_count = list(counts.values())[0]
            top_pct = round(top_count / profile["rows"] * 100, 1)
            insights.append({
                "title": f"Dominant Category in {col.title()}",
                "description": f"'{top_val}' is the most frequent value in '{col}' appearing {top_count} times ({top_pct}% of records).",
                "type": "neutral"
            })

    if profile["duplicates"] > 0:
        insights.append({
            "title": "Duplicate Rows Present",
            "description": f"{profile['duplicates']} duplicate rows detected — these may skew analysis results if not removed.",
            "type": "warning"
        })
        recommendations.append("Remove duplicate rows before training any machine learning models.")
    else:
        insights.append({
            "title": "No Duplicates Found",
            "description": f"All {profile['rows']} rows are unique — no duplicate records detected in this dataset.",
            "type": "positive"
        })

    while len(insights) < 6:
        insights.append({
            "title": "Dataset Overview",
            "description": f"The dataset contains {profile['rows']} rows and {len(numeric_cols)} numeric + {len(categorical_cols)} categorical features.",
            "type": "neutral"
        })

    if not recommendations:
        recommendations = [
            f"Explore relationships between numeric features using correlation analysis.",
            "Consider feature engineering to create new predictive variables.",
            "Visualize distributions to identify any data anomalies before modeling."
        ]

    summary = (
        f"This dataset contains {profile['rows']} records across {profile['columns']} columns "
        f"({len(numeric_cols)} numeric, {len(categorical_cols)} categorical). "
        f"{'Data quality is excellent with no missing values.' if total_missing == 0 else f'There are {total_missing} missing values requiring attention.'} "
        f"{'No duplicate rows were found.' if profile['duplicates'] == 0 else str(profile['duplicates']) + ' duplicate rows detected.'}"
    )

    return {
        "summary": summary,
        "insights": insights[:6],
        "recommendations": recommendations[:3],
        "powered_by": "statistical_analysis"
    }


def _read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")