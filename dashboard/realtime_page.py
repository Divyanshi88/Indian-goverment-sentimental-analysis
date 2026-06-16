"""Streamlit dashboard for real-time Reddit sentiment analysis."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None

from src.models.realtime_analyzer import RealtimeRedditAnalyzer
from src.analytics.aggregations import sentiment_timeline

SENTIMENT_COLORS = {
    "positive": "#16a34a",
    "negative": "#dc2626",
    "neutral": "#334155",
}

st.set_page_config(
    page_title="Real-Time Reddit Sentiment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Real-Time Reddit Sentiment Analysis")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    subreddit = st.text_input(
        "Subreddit",
        value="india",
        help="Enter subreddit name without 'r/'",
    )
    
    analysis_mode = st.radio(
        "Analysis Mode",
        ["Recent Posts", "Recent Comments", "Both"],
        help="Choose what to analyze",
    )
    
    post_limit = st.slider("Post Limit", min_value=5, max_value=100, value=20)
    comment_limit = st.slider("Comment Limit", min_value=5, max_value=100, value=50)
    
    model_choice = st.selectbox(
        "ML Model",
        ["logistic_regression", "naive_bayes"],
        help="Choose the sentiment classification model",
    )
    
    run_analysis = st.button(
        "🚀 Run Real-Time Analysis",
        type="primary",
        use_container_width=True,
    )


# Main analysis section
if run_analysis:
    with st.spinner("🔄 Connecting to Reddit and analyzing sentiment..."):
        try:
            # Initialize analyzer
            analyzer = RealtimeRedditAnalyzer(model_name=model_choice)
            
            # Connect to Reddit
            if not analyzer.connect_reddit():
                st.error(
                    "❌ Failed to connect to Reddit API.\n\n"
                    "Please set these environment variables:\n"
                    "- REDDIT_CLIENT_ID\n"
                    "- REDDIT_CLIENT_SECRET\n"
                    "- REDDIT_USER_AGENT"
                )
            else:
                st.success("✅ Connected to Reddit API")
                
                # Collect data based on mode
                posts_df = pd.DataFrame()
                comments_df = pd.DataFrame()
                
                if analysis_mode in ["Recent Posts", "Both"]:
                    st.info(f"📥 Fetching recent posts from r/{subreddit}...")
                    posts_df = analyzer.analyze_recent_posts(
                        subreddit_name=subreddit,
                        limit=post_limit,
                    )
                    st.success(f"✅ Analyzed {len(posts_df)} posts")
                
                if analysis_mode in ["Recent Comments", "Both"]:
                    st.info(f"📥 Fetching recent comments from r/{subreddit}...")
                    comments_df = analyzer.analyze_recent_comments(
                        subreddit_name=subreddit,
                        limit=comment_limit,
                    )
                    st.success(f"✅ Analyzed {len(comments_df)} comments")
                
                # Combine dataframes
                if not posts_df.empty and not comments_df.empty:
                    combined_df = pd.concat(
                        [posts_df, comments_df],
                        ignore_index=True,
                    )
                    content_type = "Posts & Comments"
                elif not posts_df.empty:
                    combined_df = posts_df
                    content_type = "Posts"
                elif not comments_df.empty:
                    combined_df = comments_df
                    content_type = "Comments"
                else:
                    combined_df = pd.DataFrame()
                    content_type = "Data"
                
                # Display results
                if not combined_df.empty:
                    st.markdown("---")
                    st.header(f"📈 Sentiment Analysis Results: {content_type}")
                    
                    # Summary metrics
                    col1, col2, col3 = st.columns(3)
                    
                    summary = analyzer.get_sentiment_summary(combined_df)
                    
                    with col1:
                        st.metric(
                            "Total Analyzed",
                            len(combined_df),
                        )
                    
                    with col2:
                        if "positive" in summary["sentiment"].values:
                            positive_count = summary[summary["sentiment"] == "positive"]["count"].values[0]
                            st.metric("🟢 Positive", positive_count)
                        else:
                            st.metric("🟢 Positive", 0)
                    
                    with col3:
                        if "negative" in summary["sentiment"].values:
                            negative_count = summary[summary["sentiment"] == "negative"]["count"].values[0]
                            st.metric("🔴 Negative", negative_count)
                        else:
                            st.metric("🔴 Negative", 0)
                    
                    # Sentiment distribution chart
                    st.markdown("### Sentiment Distribution")
                    
                    if px and go:
                        fig = px.pie(
                            summary,
                            names="sentiment",
                            values="count",
                            color="sentiment",
                            color_discrete_map=SENTIMENT_COLORS,
                            hover_data={"count": True, "percentage": True},
                        )
                        fig.update_traces(
                            textinfo="percent+label",
                            textfont_size=12,
                            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{customdata[1]:.1f}%<extra></extra>",
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.dataframe(summary, use_container_width=True)
                    
                    # Sentiment summary table
                    st.markdown("### Sentiment Summary")
                    summary_display = summary.copy()
                    summary_display["percentage"] = summary_display["percentage"].apply(lambda x: f"{x:.2f}%")
                    st.dataframe(
                        summary_display,
                        use_container_width=True,
                        hide_index=True,
                    )
                    
                    # Sample data display
                    st.markdown("### Recent Posts/Comments")
                    
                    display_cols = [
                        "sentiment",
                        "text",
                        "sentiment_probability",
                        "score",
                        "author",
                    ]
                    available_cols = [col for col in display_cols if col in combined_df.columns]
                    
                    display_df = combined_df[available_cols].head(10).copy()
                    display_df.columns = [col.replace("_", " ").title() for col in display_cols]
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True,
                    )
                    
                    # Download options
                    st.markdown("### Download Results")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = combined_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name=f"{subreddit}_sentiment_analysis.csv",
                            mime="text/csv",
                        )
                    
                    with col2:
                        json = combined_df.to_json(orient="records")
                        st.download_button(
                            label="📥 Download as JSON",
                            data=json,
                            file_name=f"{subreddit}_sentiment_analysis.json",
                            mime="application/json",
                        )
                else:
                    st.warning("No data available for analysis")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check your Reddit API credentials and try again.")

else:
    st.info("👈 Configure settings in the sidebar and click 'Run Real-Time Analysis' to start")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666;">
    <p>Real-Time Reddit Sentiment Dashboard | Using Logistic Regression & Naive Bayes Models</p>
    </div>
    """,
    unsafe_allow_html=True,
)
