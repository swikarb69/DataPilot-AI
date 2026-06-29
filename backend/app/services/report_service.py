import os
import io
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

DARK    = colors.HexColor("#0d0f14")
SURFACE = colors.HexColor("#13161e")
ACCENT  = colors.HexColor("#38bdf8")
MUTED   = colors.HexColor("#64748b")
WHITE   = colors.HexColor("#f1f5f9")
GREEN   = colors.HexColor("#4ade80")
ORANGE  = colors.HexColor("#fb923c")
BORDER  = colors.HexColor("#1e2330")
ROW_ALT = colors.HexColor("#1a1f2e")

BG      = "#0d0f14"
SURF    = "#13161e"
ACC     = "#38bdf8"
GRID    = "#1e2330"
TXT     = "#f1f5f9"
MUTED_C = "#64748b"


def build_styles():
    return {
        "title": ParagraphStyle(
            "T",
            fontName="Helvetica-Bold",
            fontSize=34,
            leading=40,
            textColor=WHITE,
            spaceBefore=0,
            spaceAfter=18,
            alignment=0,
        ),
        "subtitle": ParagraphStyle(
            "ST",
            fontName="Helvetica",
            fontSize=15,
            leading=22,
            textColor=MUTED,
            spaceBefore=0,
            spaceAfter=20,
            alignment=0,
        ),
        "section":       ParagraphStyle("S",  fontName="Helvetica-Bold", fontSize=13, textColor=ACCENT, spaceBefore=18, spaceAfter=8),
        "body":          ParagraphStyle("B",  fontName="Helvetica",      fontSize=10, textColor=WHITE, spaceAfter=6, leading=16),
        "muted":         ParagraphStyle("M",  fontName="Helvetica",      fontSize=8,  textColor=MUTED, spaceAfter=3),
        "insight_title": ParagraphStyle("IT", fontName="Helvetica-Bold", fontSize=10, textColor=ACCENT, spaceAfter=2),
        "insight_body":  ParagraphStyle("IB", fontName="Helvetica",      fontSize=9,  textColor=WHITE, spaceAfter=4, leading=14),
        "rec":           ParagraphStyle("R",  fontName="Helvetica",      fontSize=9,  textColor=WHITE, spaceAfter=5, leading=14, leftIndent=10),
        "chart_title":   ParagraphStyle("CT", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, spaceAfter=4, alignment=TA_CENTER),
    }


def _mpl_defaults(ax, title=""):
    ax.set_facecolor(SURF)
    ax.figure.patch.set_facecolor(SURF)
    ax.tick_params(colors=TXT, labelsize=8)
    ax.xaxis.label.set_color(TXT)
    ax.yaxis.label.set_color(TXT)
    ax.title.set_color(TXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(color=GRID, linewidth=0.5)
    if title:
        ax.set_title(title, color=TXT, fontsize=10, pad=8)


def _buf(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=SURF, edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf


def _generate_charts(df):
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    charts = []

    # Histograms
    for col in numeric_cols[:3]:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(df[col].dropna(), bins=20, color=ACC, edgecolor=GRID, linewidth=0.5)
        _mpl_defaults(ax, f"Distribution of {col}")
        ax.set_xlabel(col, color=TXT, fontsize=8)
        ax.set_ylabel("Count", color=TXT, fontsize=8)
        charts.append((f"Distribution of {col}", _buf(fig)))

    # Correlation heatmap
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(5, 4))
        im = ax.imshow(corr.values, cmap="Blues", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8, color=TXT)
        ax.set_yticklabels(corr.columns, fontsize=8, color=TXT)
        for i in range(len(corr)):
            for j in range(len(corr.columns)):
                ax.text(j, i, f"{corr.values[i, j]:.2f}",
                        ha="center", va="center", fontsize=8, color=TXT)
        fig.colorbar(im, ax=ax)
        _mpl_defaults(ax, "Correlation Heatmap")
        charts.append(("Correlation Heatmap", _buf(fig)))

    # Bar charts for categorical
    for col in categorical_cols[:2]:
        counts = df[col].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(counts.index, counts.values, color=ACC, edgecolor=GRID, linewidth=0.5)
        ax.set_xticklabels(counts.index, rotation=45, ha="right", fontsize=7, color=TXT)
        _mpl_defaults(ax, f"Value Counts: {col}")
        ax.set_ylabel("Count", color=TXT, fontsize=8)
        charts.append((f"Value Counts: {col}", _buf(fig)))

    # Scatter
    if len(numeric_cols) >= 2:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]],
                   color=ACC, alpha=0.7, edgecolors=GRID, linewidth=0.3, s=40)
        _mpl_defaults(ax, f"{numeric_cols[0]} vs {numeric_cols[1]}")
        ax.set_xlabel(numeric_cols[0], color=TXT, fontsize=8)
        ax.set_ylabel(numeric_cols[1], color=TXT, fontsize=8)
        charts.append((f"{numeric_cols[0]} vs {numeric_cols[1]}", _buf(fig)))

    return charts


def _table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  ACCENT),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  DARK),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("BACKGROUND",   (0, 1), (-1, -1), SURFACE),
        ("TEXTCOLOR",    (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS",(0,1), (-1, -1), [SURFACE, ROW_ALT]),
        ("GRID",         (0, 0), (-1, -1), 0.4, BORDER),
        ("PADDING",      (0, 0), (-1, -1), 7),
        ("FONTNAME",     (0, 1), (0, -1),  "Helvetica-Bold"),
        ("TEXTCOLOR",    (0, 1), (0, -1),  ACCENT),
    ]))
    return t


def generate_report(file_path: str, insights: dict) -> str:
    df = _read_file(file_path)
    filename = os.path.basename(file_path)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"report_{filename.replace('.csv','').replace('.xlsx','')}_{ts}.pdf"
    report_path = os.path.join(REPORTS_DIR, report_name)

    doc = SimpleDocTemplate(report_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = build_styles()
    story = []

    def dark_bg(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DARK)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.restoreState()

    # Cover
    story.append(Spacer(1, 2.0*cm))
    story.append(Paragraph("DataPilot AI", S["title"]))
    story.append(Paragraph("Automated Data Analysis Report", S["subtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=ACCENT))
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(f"<b>Dataset:</b>  {filename}", S["muted"]))
    story.append(Paragraph(f"<b>Generated:</b>  {datetime.now().strftime('%B %d, %Y at %H:%M')}", S["muted"]))
    story.append(Spacer(1, 0.5*cm))

    # Executive Summary
    story.append(Paragraph("Executive Summary", S["section"]))
    story.append(Paragraph(insights.get("summary", "No summary available."), S["body"]))

    # Dataset Overview
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    total_missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    story.append(Paragraph("Dataset Overview", S["section"]))
    overview = [
        ["Metric", "Value"],
        ["Total Rows", f"{len(df):,}"],
        ["Total Columns", str(len(df.columns))],
        ["Numeric Columns", str(len(numeric_cols))],
        ["Categorical Columns", str(len(categorical_cols))],
        ["Missing Values", str(total_missing)],
        ["Duplicate Rows", str(duplicates)],
        ["Memory Usage", f"{round(df.memory_usage(deep=True).sum()/1024, 2)} KB"],
    ]
    story.append(_table(overview, [9*cm, 8*cm]))
    story.append(Spacer(1, 0.4*cm))

    # Column Details
    story.append(Paragraph("Column Details", S["section"]))
    col_data = [["Column", "Type", "Missing", "Missing %"]]
    for col in df.columns:
        m = int(df[col].isnull().sum())
        col_data.append([col, str(df[col].dtype), str(m), f"{round(m/len(df)*100,1)}%"])
    story.append(_table(col_data, [6*cm, 4.5*cm, 2.5*cm, 4*cm]))
    story.append(Spacer(1, 0.4*cm))

    # Statistical Summary
    if numeric_cols:
        story.append(Paragraph("Statistical Summary", S["section"]))
        desc = df[numeric_cols].describe().round(2)
        metrics = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
        stat_data = [["Metric"] + numeric_cols]
        for m in metrics:
            if m in desc.index:
                stat_data.append([m] + [str(desc.loc[m, c]) for c in numeric_cols])
        col_w = [3*cm] + [14*cm / len(numeric_cols)] * len(numeric_cols)
        story.append(_table(stat_data, col_w))

    story.append(PageBreak())

    # Charts
    story.append(Paragraph("Data Visualizations", S["section"]))
    story.append(Spacer(1, 0.2*cm))

    try:
        charts = _generate_charts(df)
        page_width = A4[0] - 4*cm
        chart_w = (page_width - 0.5*cm) / 2

        pairs = [charts[i:i+2] for i in range(0, len(charts), 2)]
        for pair in pairs:
            row_items = []
            for title, img_buf in pair:
                img = Image(img_buf, width=chart_w, height=chart_w * 0.62)
                cell = [Paragraph(title, S["chart_title"]), img]
                row_items.append(cell)

            if len(row_items) == 2:
                t = Table([[row_items[0], row_items[1]]],
                          colWidths=[chart_w + 0.2*cm, chart_w + 0.2*cm])
            else:
                t = Table([[row_items[0]]], colWidths=[page_width])

            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("GRID",       (0, 0), (-1, -1), 0.4, BORDER),
                ("PADDING",    (0, 0), (-1, -1), 6),
                ("VALIGN",     (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.3*cm))
    except Exception as e:
        story.append(Paragraph(f"Note: Charts unavailable — {str(e)}", S["muted"]))

    story.append(PageBreak())

    # AI Insights
    story.append(Paragraph("AI Insights", S["section"]))
    type_colors = {"positive": GREEN, "warning": ORANGE, "neutral": ACCENT}

    for i, insight in enumerate(insights.get("insights", []), 1):
        dot = type_colors.get(insight.get("type", "neutral"), ACCENT)
        rows = [
            [Paragraph(f"<b>{i}. {insight['title']}</b>", S["insight_title"])],
            [Paragraph(insight["description"], S["insight_body"])],
        ]
        t = Table(rows, colWidths=[16*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), SURFACE),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
            ("TOPPADDING",    (0, 0), (-1, 0),  10),
            ("BOTTOMPADDING", (0,-1), (-1, -1), 10),
            ("LINEAFTER",     (0, 0), (0, -1),  3, dot),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.2*cm))

    # Recommendations
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Recommendations", S["section"]))
    for i, rec in enumerate(insights.get("recommendations", []), 1):
        story.append(Paragraph(f"{i}.  {rec}", S["rec"]))

    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        f"Generated by DataPilot AI  ·  {datetime.now().strftime('%B %d, %Y')}",
        S["muted"]
    ))

    doc.build(story, onFirstPage=dark_bg, onLaterPages=dark_bg)
    return report_path


def _read_file(file_path: str) -> pd.DataFrame:
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format.")