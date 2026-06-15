"""Streamlit dashboard entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import altair as alt
alt.themes.enable("default")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import altair as alt

try:
    import plotly.express as px
except ImportError:  # pragma: no cover - optional dashboard enhancement
    px = None

try:
    from wordcloud import WordCloud
except ImportError:  # pragma: no cover - optional dashboard enhancement
    WordCloud = None

from main import run_sample_pipeline
from src.analytics.aggregations import sentiment_summary, sentiment_timeline
from src.feature_engineering.topics import extract_tfidf_keywords, lda_topics

SENTIMENT_COLORS = {
    "positive": "#1f9d73",
    "negative": "#c93c37",
    "neutral": "#64748b",
}

st.set_page_config(
    page_title="Indian Government Sentiment Dashboard",
    page_icon="IN",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_content() -> pd.DataFrame:
    """Load processed content, generating sample data on first run."""
    processed_path = PROJECT_ROOT / "data" / "processed" / "sentiment_content.csv"
    if not processed_path.exists():
        run_sample_pipeline()
    frame = pd.read_csv(processed_path)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], errors="coerce", utc=True)
    frame["date"] = frame["created_utc"].dt.date
    return frame.dropna(subset=["created_utc"])


def asset_path(filename: str) -> Path:
    """Return an absolute path for a dashboard asset."""
    return PROJECT_ROOT / "dashboard" / "assets" / filename


def sentiment_pie(summary: pd.DataFrame):
    """Create sentiment distribution pie chart when Plotly is installed."""
    if px is None:
        return None
    return px.pie(
        summary,
        names="sentiment",
        values="count",
        color="sentiment",
        color_discrete_map=SENTIMENT_COLORS,
        hole=0.52,
    )


def sentiment_bar(summary: pd.DataFrame) -> alt.Chart:
    """Create sentiment distribution bar chart."""
    return (
        alt.Chart(summary)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("sentiment:N", title=None, sort=["positive", "neutral", "negative"]),
            y=alt.Y("count:Q", title="Records"),
            color=alt.Color(
                "sentiment:N",
                scale=alt.Scale(
                    domain=list(SENTIMENT_COLORS),
                    range=list(SENTIMENT_COLORS.values()),
                ),
            ),
            tooltip=["sentiment", "count", alt.Tooltip("percentage:Q", format=".1f")],
        )
        .properties(height=280)
    )


def timeline_chart(timeline: pd.DataFrame) -> alt.Chart:
    """Create sentiment timeline chart."""
    return (
        alt.Chart(timeline)
        .mark_line(point=True)
        .encode(
            x=alt.X("period:T", title="Date"),
            y=alt.Y("count:Q", title="Mentions"),
            color=alt.Color(
                "sentiment:N",
                scale=alt.Scale(
                    domain=list(SENTIMENT_COLORS),
                    range=list(SENTIMENT_COLORS.values()),
                ),
            ),
            tooltip=["period:T", "sentiment:N", "count:Q"],
        )
        .properties(height=360)
    )


def inject_css() -> None:
    css_path = asset_path("styles.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="metric-card"><span>{label}</span><strong>{value}</strong></div>',
        unsafe_allow_html=True,
    )


def filter_content(frame: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    subreddits = st.sidebar.multiselect(
        "Subreddit",
        sorted(frame["subreddit"].dropna().unique()),
        default=sorted(frame["subreddit"].dropna().unique()),
    )
    sentiments = st.sidebar.multiselect(
        "Sentiment",
        ["positive", "neutral", "negative"],
        default=["positive", "neutral", "negative"],
    )
    date_min = frame["date"].min()
    date_max = frame["date"].max()
    date_range = st.sidebar.date_input("Date range", value=(date_min, date_max))
    query = st.sidebar.text_input("Keyword search")

    filtered = frame[
        frame["subreddit"].isin(subreddits) & frame["sentiment"].isin(sentiments)
    ].copy()
    if len(date_range) == 2:
        filtered = filtered[(filtered["date"] >= date_range[0]) & (filtered["date"] <= date_range[1])]
    if query:
        mask = filtered["text"].fillna("").str.contains(query, case=False, regex=False)
        filtered = filtered[mask]
    return filtered


def overview_page(frame: pd.DataFrame) -> None:
    st.title("Indian Government Sentiment Analysis")
    st.markdown(
        '<p class="section-note">A recruiter-ready NLP dashboard for monitoring public discussion across India-focused Reddit communities.</p>',
        unsafe_allow_html=True,
    )
    summary = sentiment_summary(frame)
    total_posts = int((frame["content_type"] == "post").sum())
    total_comments = int((frame["content_type"] == "comment").sum())
    percentages = summary.set_index("sentiment")["percentage"].to_dict()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_card("Posts analyzed", f"{total_posts:,}")
    with col2:
        metric_card("Comments analyzed", f"{total_comments:,}")
    with col3:
        metric_card("Positive", f"{percentages.get('positive', 0):.1f}%")
    with col4:
        metric_card("Neutral", f"{percentages.get('neutral', 0):.1f}%")
    with col5:
        metric_card("Negative", f"{percentages.get('negative', 0):.1f}%")

    st.divider()
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Sentiment Mix")
        pie = sentiment_pie(summary)
        if pie is None:
            st.altair_chart(sentiment_bar(summary), use_container_width=True)
        else:
            st.plotly_chart(pie, use_container_width=True)
    with right:
        st.subheader("Daily Conversation Trend")
        st.altair_chart(timeline_chart(sentiment_timeline(frame, "D")), use_container_width=True)


def distribution_page(frame: pd.DataFrame) -> None:
    st.title("Sentiment Distribution")
    summary = sentiment_summary(frame)
    col1, col2 = st.columns(2)
    with col1:
        pie = sentiment_pie(summary)
        if pie is None:
            st.altair_chart(sentiment_bar(summary), use_container_width=True)
        else:
            st.plotly_chart(pie, use_container_width=True)
    with col2:
        st.altair_chart(sentiment_bar(summary), use_container_width=True)


def timeline_page(frame: pd.DataFrame) -> None:
    st.title("Sentiment Timeline")
    frequency_label = st.radio(
        "Granularity",
        ["Daily", "Weekly", "Monthly"],
        horizontal=True,
        index=0,
    )
    frequency = {"Daily": "D", "Weekly": "W", "Monthly": "M"}[frequency_label]
    st.altair_chart(timeline_chart(sentiment_timeline(frame, frequency)), use_container_width=True)


def word_cloud_page(frame: pd.DataFrame) -> None:
    st.title("Word Cloud Analysis")
    col1, col2 = st.columns(2)
    for column, sentiment in [(col1, "positive"), (col2, "negative")]:
        text = " ".join(frame.loc[frame["sentiment"] == sentiment, "clean_text"].fillna(""))
        with column:
            st.subheader(f"{sentiment.title()} discussion")
            if text.strip():
                if WordCloud is None:
                    words = pd.Series(text.split()).value_counts().head(20).reset_index()
                    words.columns = ["word", "count"]
                    st.bar_chart(words, x="word", y="count")
                else:
                    image = WordCloud(
                        width=900,
                        height=520,
                        background_color="white",
                        colormap="Greens" if sentiment == "positive" else "Reds",
                    ).generate(text)
                    st.image(image.to_array(), use_container_width=True)
            else:
                st.info(f"No {sentiment} records in the current filter.")


def topics_page(frame: pd.DataFrame) -> None:
    st.title("Trending Topics")
    keywords = extract_tfidf_keywords(frame, top_n=20)
    topics = lda_topics(frame)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Top Keywords")
        st.dataframe(keywords, use_container_width=True, hide_index=True)
    with col2:
        st.subheader("Topic Clusters")
        st.dataframe(topics, use_container_width=True, hide_index=True)


def explorer_page(frame: pd.DataFrame) -> None:
    st.title("Reddit Post Explorer")
    columns = [
        "created_utc",
        "content_type",
        "subreddit",
        "sentiment",
        "sentiment_probability",
        "score",
        "text",
        "permalink",
    ]
    st.dataframe(
        frame[[column for column in columns if column in frame.columns]].sort_values(
            "created_utc", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )


def main() -> None:
    inject_css()
    frame = filter_content(load_content())
    page = st.sidebar.radio(
        "Navigation",
        [
            "Overview",
            "Sentiment Distribution",
            "Sentiment Timeline",
            "Word Cloud Analysis",
            "Trending Topics",
            "Reddit Post Explorer",
        ],
    )
    if frame.empty:
        st.warning("No records match the selected filters.")
        return
    if page == "Overview":
        overview_page(frame)
    elif page == "Sentiment Distribution":
        distribution_page(frame)
    elif page == "Sentiment Timeline":
        timeline_page(frame)
    elif page == "Word Cloud Analysis":
        word_cloud_page(frame)
    elif page == "Trending Topics":
        topics_page(frame)
    else:
        explorer_page(frame)


if __name__ == "__main__":
    main()
