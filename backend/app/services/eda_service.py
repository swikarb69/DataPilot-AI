import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import json


def generate_eda(file_path: str) -> dict:
    df = _read_file(file_path)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    charts = []

    # 1. Distribution histograms for numeric columns
    for col in numeric_cols[:6]:
        fig = px.histogram(
            df, x=col, nbins=30,
            title=f"Distribution of {col}",
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(**_dark_layout())
        charts.append({
            "id": f"hist_{col}",
            "title": f"Distribution of {col}",
            "type": "histogram",
            "column": col,
            "data": json.loads(fig.to_json()),
        })

    # 2. Boxplots for numeric columns
    for col in numeric_cols[:6]:
        fig = px.box(
            df, y=col,
            title=f"Boxplot of {col}",
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(**_dark_layout())
        charts.append({
            "id": f"box_{col}",
            "title": f"Boxplot of {col}",
            "type": "boxplot",
            "column": col,
            "data": json.loads(fig.to_json()),
        })

    # 3. Correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.columns.tolist(),
            colorscale="Blues",
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
            showscale=True,
        ))
        fig.update_layout(title="Correlation Heatmap", **_dark_layout())
        charts.append({
            "id": "correlation_heatmap",
            "title": "Correlation Heatmap",
            "type": "heatmap",
            "data": json.loads(fig.to_json()),
        })

    # 4. Bar charts for categorical columns
    for col in categorical_cols[:4]:
        counts = df[col].value_counts().head(15).reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(
            counts, x=col, y="count",
            title=f"Value Counts: {col}",
            color_discrete_sequence=["#38bdf8"],
        )
        fig.update_layout(**_dark_layout())
        charts.append({
            "id": f"bar_{col}",
            "title": f"Value Counts: {col}",
            "type": "bar",
            "column": col,
            "data": json.loads(fig.to_json()),
        })

    # 5. Missing values heatmap
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing) > 0:
        fig = px.bar(
            x=missing.index.tolist(),
            y=missing.values.tolist(),
            title="Missing Values per Column",
            labels={"x": "Column", "y": "Missing Count"},
            color_discrete_sequence=["#f87171"],
        )
        fig.update_layout(**_dark_layout())
        charts.append({
            "id": "missing_heatmap",
            "title": "Missing Values per Column",
            "type": "missing",
            "data": json.loads(fig.to_json()),
        })

    # 6. Scatter plot (top 2 numeric cols)
    if len(numeric_cols) >= 2:
        fig = px.scatter(
            df, x=numeric_cols[0], y=numeric_cols[1],
            title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
            color_discrete_sequence=["#38bdf8"],
            opacity=0.7,
        )
        fig.update_layout(**_dark_layout())
        charts.append({
            "id": f"scatter_{numeric_cols[0]}_{numeric_cols[1]}",
            "title": f"{numeric_cols[0]} vs {numeric_cols[1]}",
            "type": "scatter",
            "data": json.loads(fig.to_json()),
        })

    # Statistical summary
    stats = {}
    if len(numeric_cols) > 0:
        desc = df[numeric_cols].describe().round(2)
        stats = desc.to_dict()

    return {
        "charts": charts,
        "stats": stats,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "total_charts": len(charts),
    }


def _dark_layout():
    return {
        "paper_bgcolor": "#13161e",
        "plot_bgcolor": "#13161e",
        "font": {"color": "#f1f5f9", "family": "Inter"},
        "xaxis": {"gridcolor": "#1e2330", "zerolinecolor": "#1e2330"},
        "yaxis": {"gridcolor": "#1e2330", "zerolinecolor": "#1e2330"},
        "margin": {"t": 50, "l": 40, "r": 20, "b": 40},
    }


def _read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")