"""Reusable Plotly and Altair charts for Streamlit pages."""

from __future__ import annotations

import altair as alt
import pandas as pd

try:
    import plotly.express as px
except ImportError:
    px = None


SENTIMENT_COLORS = {
    "positive": "#10B981",
    "negative": "#EF4444",
    "neutral": "#94A3B8",
}


def sentiment_pie(summary: pd.DataFrame):
    """Create sentiment distribution donut chart."""

    if px is None:
        return None

    fig = px.pie(
        summary,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        hole=0.60,
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#1E293B",
        showlegend=True,
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        ),
    )

    fig.update_traces(
        textinfo="percent+label",
        textfont_size=14,
    )

    return fig


def sentiment_bar(summary: pd.DataFrame) -> alt.Chart:
    """Create sentiment distribution bar chart."""

    chart = (
        alt.Chart(summary)
        .mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8,
        )
        .encode(
            x=alt.X(
                "sentiment:N",
                sort=["positive", "neutral", "negative"],
                title=None,
            ),
            y=alt.Y(
                "count:Q",
                title="Records",
            ),
            color=alt.Color(
                "sentiment:N",
                scale=alt.Scale(
                    domain=list(SENTIMENT_COLORS.keys()),
                    range=list(SENTIMENT_COLORS.values()),
                ),
                legend=None,
            ),
            tooltip=[
                "sentiment:N",
                "count:Q",
            ],
        )
        .properties(
            height=320,
        )
    )

    return (
        chart
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#1E293B",
            titleColor="#1E293B",
            gridColor="#E2E8F0",
        )
    )


def timeline_chart(timeline: pd.DataFrame) -> alt.Chart:
    """Create sentiment timeline chart."""

    chart = (
        alt.Chart(timeline)
        .mark_line(
            point=True,
            strokeWidth=3,
        )
        .encode(
            x=alt.X(
                "period:T",
                title="Date",
            ),
            y=alt.Y(
                "count:Q",
                title="Mentions",
            ),
            color=alt.Color(
                "sentiment:N",
                scale=alt.Scale(
                    domain=list(SENTIMENT_COLORS.keys()),
                    range=list(SENTIMENT_COLORS.values()),
                ),
            ),
            tooltip=[
                "period:T",
                "sentiment:N",
                "count:Q",
            ],
        )
        .properties(
            height=360,
        )
    )

    return (
        chart
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#1E293B",
            titleColor="#1E293B",
            gridColor="#E2E8F0",
        )
    )