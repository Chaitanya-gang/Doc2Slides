"""
newd2p - Chart Generator using matplotlib
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from src.llm.provider_factory import get_llm_provider
from src.llm.prompt_templates import CHART_ANALYSIS_PROMPT, SYSTEM_PROMPT
from src.utils.logger import get_logger

logger = get_logger("chart_generator")

CHART_COLORS = [
    '#6366f1', '#f43f5e', '#22d3ee', '#a3e635',
    '#fbbf24', '#a78bfa', '#fb923c', '#34d399',
]

DARK_BG = '#0f172a'
CARD_BG = '#1e293b'
TEXT_COLOR = '#e2e8f0'
GRID_COLOR = '#334155'


def setup_chart_style():
    plt.rcParams.update({
        'figure.facecolor': DARK_BG,
        'axes.facecolor': CARD_BG,
        'axes.edgecolor': GRID_COLOR,
        'axes.labelcolor': TEXT_COLOR,
        'text.color': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'grid.color': GRID_COLOR,
        'grid.alpha': 0.3,
        'font.size': 12,
        'axes.titlesize': 16,
        'axes.labelsize': 13,
    })


def analyze_text_for_charts(text: str) -> list:
    try:
        llm = get_llm_provider()
        prompt = CHART_ANALYSIS_PROMPT.format(content=text)
        response = llm.generate(prompt, system_prompt=SYSTEM_PROMPT)

        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end > start:
            data = json.loads(response[start:end])
            charts = data.get("charts", [])
            # Validate charts
            valid_charts = []
            for chart in charts:
                labels = chart.get("labels", [])
                values = chart.get("values", [])
                if labels and values and len(labels) >= 2 and len(values) >= 2:
                    # Make sure same length
                    min_len = min(len(labels), len(values))
                    chart["labels"] = labels[:min_len]
                    chart["values"] = values[:min_len]
                    valid_charts.append(chart)
            logger.info(f"Found {len(valid_charts)} valid charts")
            return valid_charts
    except Exception as e:
        logger.error(f"Chart analysis failed: {e}")
    return []


def _clean_values(values: list) -> list:
    clean = []
    for v in values:
        try:
            clean.append(float(str(v).replace('%', '').replace(',', '').replace('°C', '').replace('ppm', '').replace('mm', '')))
        except:
            clean.append(0)
    return clean


def create_bar_chart(chart_data: dict, output_path: str) -> str:
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = chart_data.get("labels", [])
    values = _clean_values(chart_data.get("values", []))
    title = chart_data.get("title", "Chart")

    if not labels or not values or len(labels) != len(values):
        plt.close()
        return ""

    colors = CHART_COLORS[:len(labels)]
    bars = ax.bar(labels, values, color=colors, width=0.6, edgecolor='none', zorder=3)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + max(values)*0.02,
                f'{val:g}', ha='center', va='bottom', fontweight='bold',
                color=TEXT_COLOR, fontsize=13)

    ax.set_title(title, fontweight='bold', pad=20, fontsize=18)
    ax.set_xlabel(chart_data.get("x_label", ""), labelpad=10)
    ax.set_ylabel(chart_data.get("y_label", ""), labelpad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    logger.info(f"Bar chart saved: {output_path}")
    return output_path


def create_pie_chart(chart_data: dict, output_path: str) -> str:
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(10, 7))

    labels = chart_data.get("labels", [])
    values = _clean_values(chart_data.get("values", []))
    title = chart_data.get("title", "Chart")

    if not labels or not values or len(labels) != len(values):
        plt.close()
        return ""

    colors = CHART_COLORS[:len(labels)]

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90, pctdistance=0.8,
        wedgeprops=dict(width=0.4, edgecolor=DARK_BG, linewidth=2),
        textprops={'color': TEXT_COLOR, 'fontsize': 12},
    )

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title(title, fontweight='bold', pad=20, fontsize=18, color=TEXT_COLOR)
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    logger.info(f"Pie chart saved: {output_path}")
    return output_path


def create_line_chart(chart_data: dict, output_path: str) -> str:
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = chart_data.get("labels", [])
    values = _clean_values(chart_data.get("values", []))
    title = chart_data.get("title", "Chart")

    if not labels or not values or len(labels) != len(values):
        plt.close()
        return ""

    color = CHART_COLORS[0]
    x_pos = list(range(len(labels)))

    ax.plot(x_pos, values, color=color, linewidth=3,
            marker='o', markersize=10, markerfacecolor='white',
            markeredgecolor=color, markeredgewidth=2, zorder=3)

    ax.fill_between(x_pos, values, alpha=0.15, color=color, zorder=2)

    for i, (x, y) in enumerate(zip(x_pos, values)):
        ax.annotate(f'{y:g}', (x, y), textcoords="offset points",
                    xytext=(0, 15), ha='center', fontweight='bold',
                    color=TEXT_COLOR, fontsize=11)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.set_title(title, fontweight='bold', pad=20, fontsize=18)
    ax.set_xlabel(chart_data.get("x_label", ""), labelpad=10)
    ax.set_ylabel(chart_data.get("y_label", ""), labelpad=10)
    ax.grid(linestyle='--', alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=DARK_BG)
    plt.close()
    logger.info(f"Line chart saved: {output_path}")
    return output_path


def generate_chart(chart_data: dict, output_dir: str, chart_index: int) -> str:
    chart_type = chart_data.get("chart_type", "bar").lower()
    output_path = f"{output_dir}/chart_{chart_index}.png"

    try:
        if chart_type == "pie":
            return create_pie_chart(chart_data, output_path)
        elif chart_type == "line":
            return create_line_chart(chart_data, output_path)
        else:
            return create_bar_chart(chart_data, output_path)
    except Exception as e:
        logger.error(f"Chart generation failed: {e}")
        return ""


def generate_all_charts(text: str, output_dir: str) -> list:
    charts_data = analyze_text_for_charts(text)
    chart_paths = []

    for i, chart_data in enumerate(charts_data):
        path = generate_chart(chart_data, output_dir, i)
        if path:
            chart_paths.append({
                "path": path,
                "title": chart_data.get("title", f"Chart {i+1}"),
                "data": chart_data,
            })

    logger.info(f"Generated {len(chart_paths)} charts")
    return chart_paths
