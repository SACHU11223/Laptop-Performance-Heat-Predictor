"""Plotly chart builders for the laptop health dashboard."""

from __future__ import annotations

import random

import plotly.graph_objects as go


CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="rgba(248,250,252,0.72)", size=12),
    margin=dict(l=18, r=18, t=48, b=24),
)


def apply_theme(fig: go.Figure, height: int = 300) -> go.Figure:
    fig.update_layout(
        **CHART_THEME,
        height=height,
        legend=dict(
            bgcolor="rgba(255,255,255,0.04)",
            bordercolor="rgba(255,255,255,0.12)",
            borderwidth=1,
            font=dict(size=11, color="rgba(248,250,252,0.64)"),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.1)",
        linecolor="rgba(255,255,255,0.1)",
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.08)",
        zerolinecolor="rgba(255,255,255,0.1)",
        linecolor="rgba(255,255,255,0.1)",
    )
    return fig


def _score_color(score: float) -> str:
    if score >= 85:
        return "#4ade80"
    if score >= 70:
        return "#86efac"
    if score >= 50:
        return "#facc15"
    if score >= 30:
        return "#fb923c"
    return "#fb7185"


def build_gauge_chart(score: float) -> go.Figure:
    score = max(0.0, min(100.0, float(score)))
    color = _score_color(score)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            delta={"reference": 75, "increasing": {"color": "#4ade80"}, "decreasing": {"color": "#fb7185"}},
            number={"font": {"size": 46, "color": color, "family": "Inter, sans-serif"}},
            title={"text": "Health score", "font": {"size": 15, "color": "rgba(248,250,252,0.72)"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "rgba(248,250,252,0.28)"},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "rgba(251,113,133,0.12)"},
                    {"range": [30, 50], "color": "rgba(251,146,60,0.12)"},
                    {"range": [50, 70], "color": "rgba(250,204,21,0.12)"},
                    {"range": [70, 100], "color": "rgba(74,222,128,0.12)"},
                ],
                "threshold": {"line": {"color": "#22d3ee", "width": 3}, "thickness": 0.75, "value": 75},
            },
        )
    )
    return apply_theme(fig, 310)


def build_metric_area_chart(cpu_val: float, ram_val: float, disk_val: float) -> go.Figure:
    random.seed(int(cpu_val * 13 + ram_val * 7 + disk_val * 3))
    x = list(range(30))

    def trace(current: float, noise: float) -> list[float]:
        current = max(0.0, min(100.0, float(current)))
        value = max(0.0, current - noise * 1.5)
        values = []
        for _ in x:
            value = max(0.0, min(100.0, value + random.gauss(0, noise * 0.35)))
            values.append(value)
        values[-1] = current
        return values

    fig = go.Figure()
    series = [
        ("CPU", trace(cpu_val, 7), "#fb7185", "rgba(251,113,133,0.12)"),
        ("RAM", trace(ram_val, 5), "#a78bfa", "rgba(167,139,250,0.12)"),
        ("Disk I/O", trace(disk_val, 7), "#22d3ee", "rgba(34,211,238,0.12)"),
    ]
    for name, values, color, fill in series:
        fig.add_trace(
            go.Scatter(
                x=x,
                y=values,
                name=name,
                mode="lines",
                line=dict(color=color, width=2.6, shape="spline"),
                fill="tozeroy",
                fillcolor=fill,
                hovertemplate=f"{name}: %{{y:.1f}}%<extra></extra>",
            )
        )
    fig.add_hline(y=80, line_dash="dot", line_color="rgba(250,204,21,0.65)", annotation_text="Warning")
    fig.update_layout(title="Resource utilization trend", yaxis=dict(range=[0, 105], ticksuffix="%"), hovermode="x unified")
    return apply_theme(fig, 310)


def build_feature_importance_chart(
    cpu: float, ram: float, disk: float, device_age: float, running_apps: int, crashed_apps: int
) -> go.Figure:
    features = ["CPU", "RAM", "Disk", "Age", "Apps", "Crashes"]
    values = [
        float(cpu),
        float(ram),
        float(disk),
        min(100, float(device_age) * 6.67),
        min(100, int(running_apps) * 1.25),
        min(100, int(crashed_apps) * 5),
    ]
    colors = [_score_color(100 - value) for value in values]
    fig = go.Figure(
        go.Bar(
            x=features,
            y=values,
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.16)", width=1)),
            text=[f"{v:.0f}%" for v in values],
            textposition="outside",
            hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
        )
    )
    fig.add_hline(y=75, line_dash="dot", line_color="rgba(250,204,21,0.65)", annotation_text="Risk line")
    fig.update_layout(title="Metric risk levels", yaxis=dict(range=[0, 112], ticksuffix="%"))
    return apply_theme(fig, 310)


def build_health_timeline_chart(history: list) -> go.Figure:
    fig = go.Figure()
    if not history or len(history) < 2:
        fig.add_annotation(
            text="Run 2+ predictions to see the health timeline",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="rgba(248,250,252,0.42)"),
        )
        fig.update_layout(title="Health score timeline")
        return apply_theme(fig, 270)

    recent = history[-20:]
    scores = [float(item.get("health_score", 0)) for item in recent]
    labels = [str(item.get("timestamp", "")).split(" ")[-1] for item in recent]
    statuses = [item.get("health_status") or item.get("status") or "Unknown" for item in recent]
    colors = [_score_color(score) for score in scores]

    fig.add_trace(
        go.Scatter(
            x=labels,
            y=scores,
            mode="lines+markers",
            name="Health score",
            line=dict(color="#22d3ee", width=2.6, shape="spline"),
            marker=dict(color=colors, size=10, line=dict(color="rgba(255,255,255,0.24)", width=1)),
            text=statuses,
            hovertemplate="%{y:.1f} - %{text}<br>%{x}<extra></extra>",
        )
    )
    fig.add_hline(y=75, line_dash="dot", line_color="rgba(74,222,128,0.65)", annotation_text="Target")
    fig.update_layout(title="Health score timeline", yaxis=dict(range=[0, 105]))
    return apply_theme(fig, 270)


def build_risk_donut_chart(health_score: float) -> go.Figure:
    health = max(0.0, min(100.0, float(health_score)))
    risk = 100 - health
    color = _score_color(health)
    fig = go.Figure(
        go.Pie(
            values=[health, risk],
            labels=["Health", "Risk"],
            hole=0.72,
            marker=dict(colors=[color, "rgba(255,255,255,0.08)"], line=dict(color="rgba(255,255,255,0.08)", width=1)),
            textinfo="none",
            hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
            sort=False,
        )
    )
    fig.add_annotation(
        text=f"<b>{health:.0f}</b><br><span style='font-size:11px'>Health</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=22, color=color),
    )
    fig.update_layout(title="Health vs risk", showlegend=True)
    return apply_theme(fig, 290)


def build_radar_chart(cpu: float, ram: float, disk: float, device_age: float, running_apps: int) -> go.Figure:
    categories = ["CPU", "RAM", "Disk", "Age", "Apps"]
    values = [
        float(cpu),
        float(ram),
        float(disk),
        min(100, float(device_age) * 6.67),
        min(100, int(running_apps) * 1.5),
    ]
    peak = max(values) if values else 0
    color = "#fb7185" if peak >= 80 else "#facc15" if peak >= 60 else "#22d3ee"
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=[75] * len(categories),
            theta=categories,
            fill="toself",
            fillcolor="rgba(250,204,21,0.06)",
            line=dict(color="rgba(250,204,21,0.42)", dash="dot"),
            name="Warning",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            fillcolor="rgba(34,211,238,0.16)",
            line=dict(color=color, width=2.6),
            marker=dict(color=color, size=7),
            name="Current system",
            hovertemplate="%{theta}: %{r:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        title="System profile radar",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
        ),
    )
    return apply_theme(fig, 320)


def build_all_charts(
    cpu: float, ram: float, disk: float, device_age: float, running_apps: int, health_score: float, history: list
):
    return (
        build_gauge_chart(health_score),
        build_metric_area_chart(cpu, ram, disk),
        build_feature_importance_chart(cpu, ram, disk, device_age, running_apps, 0),
        build_risk_donut_chart(health_score),
        build_radar_chart(cpu, ram, disk, device_age, running_apps),
        build_health_timeline_chart(history),
    )
