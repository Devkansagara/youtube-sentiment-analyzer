import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from textblob import TextBlob

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="YouTube Sentiment Analyzer",
    page_icon="🎬",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =========================================================
# HEADER
# =========================================================

st.title("🎬 YouTube Sentiment Analyzer")

st.subheader(
    "AI-powered analysis of YouTube video titles"
)

st.caption(
    "🧠 Natural Language Processing  •  "
    "🤖 Sentiment Analysis  •  "
    "▶️ YouTube"
)

st.divider()


# =========================================================
# PROJECT INTRO
# =========================================================

st.header("⚡ How It Works")

step1, step2, step3 = st.columns(3)

with step1:
    with st.container(border=True):
        st.subheader("1️⃣ Input")
        st.write(
            "Enter one or more YouTube video titles."
        )
        st.caption(
            "Enter each title on a separate line."
        )

with step2:
    with st.container(border=True):
        st.subheader("2️⃣ NLP Analysis")
        st.write(
            "TextBlob analyzes the emotional polarity "
            "of each title."
        )
        st.caption(
            "The score helps determine the sentiment."
        )

with step3:
    with st.container(border=True):
        st.subheader("3️⃣ Result")
        st.write(
            "The system displays Positive, Negative "
            "or Neutral sentiment."
        )
        st.caption(
            "Results are shown with scores and charts."
        )

st.divider()


# =========================================================
# INPUT SECTION
# =========================================================

st.header("🔎 Analyze YouTube Video Titles")

st.write(
    "Enter one title per line:"
)

titles_text = st.text_area(
    "YouTube Titles",
    height=180,
    placeholder=(
        "Example:\n"
        "This movie is absolutely amazing\n"
        "I hate this boring movie\n"
        "New technology trends in 2026\n"
        "I love this beautiful video"
    ),
    label_visibility="collapsed"
)


# =========================================================
# BUTTONS
# =========================================================

button1, button2, button3 = st.columns(3)

with button1:
    analyze_button = st.button(
        "🚀 Analyze Sentiment",
        use_container_width=True
    )

with button2:
    clear_button = st.button(
        "🧹 Clear",
        use_container_width=True
    )

with button3:
    history_button = st.button(
        "🕘 View History",
        use_container_width=True
    )


# =========================================================
# CLEAR BUTTON
# =========================================================

if clear_button:
    st.session_state.history = []
    st.rerun()


# =========================================================
# SENTIMENT FUNCTION
# =========================================================

def analyze_title(title):

    blob = TextBlob(title)

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "Positive"
        emoji = "😊"

    elif polarity < 0:
        sentiment = "Negative"
        emoji = "😞"

    else:
        sentiment = "Neutral"
        emoji = "😐"

    return sentiment, polarity, subjectivity, emoji


# =========================================================
# ANALYZE BUTTON
# =========================================================

if analyze_button:

    if not titles_text.strip():

        st.warning(
            "⚠️ Please enter at least one YouTube title."
        )

    else:

        titles = [
            title.strip()
            for title in titles_text.split("\n")
            if title.strip()
        ]

        results = []

        for title in titles:

            sentiment, polarity, subjectivity, emoji = (
                analyze_title(title)
            )

            result = {
                "Title": title,
                "Sentiment": sentiment,
                "Score": round(polarity, 2),
                "Subjectivity": round(subjectivity, 2)
            }

            results.append(result)

            st.session_state.history.append(result)


        df = pd.DataFrame(results)


        # =====================================================
        # SENTIMENT COUNTS
        # =====================================================

        positive_count = int(
            (df["Sentiment"] == "Positive").sum()
        )

        negative_count = int(
            (df["Sentiment"] == "Negative").sum()
        )

        neutral_count = int(
            (df["Sentiment"] == "Neutral").sum()
        )

        total_count = len(df)


        # =====================================================
        # RESULTS
        # =====================================================

        st.divider()

        st.header("📊 Sentiment Overview")


        # =====================================================
        # TOP METRIC CARDS
        # =====================================================

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                label="😊 Positive Titles",
                value=positive_count
            )

        with m2:
            st.metric(
                label="😞 Negative Titles",
                value=negative_count
            )

        with m3:
            st.metric(
                label="😐 Neutral Titles",
                value=neutral_count
            )

        with m4:
            st.metric(
                label="🎬 Total Titles",
                value=total_count
            )


        # =====================================================
        # RESULT TABLE
        # =====================================================

        st.header("📋 Detailed Analysis")

        display_df = df.copy()

        display_df["Sentiment"] = display_df[
            "Sentiment"
        ].replace({
            "Positive": "😊 Positive",
            "Negative": "😞 Negative",
            "Neutral": "😐 Neutral"
        })

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        # =====================================================
        # CHART SECTION
        # =====================================================

        st.header("🍩 Sentiment Distribution")

        chart_left, chart_right = st.columns(2)


        # =====================================================
        # DONUT CHART
        # =====================================================

        with chart_left:

            labels = [
                "Positive",
                "Negative",
                "Neutral"
            ]

            values = [
                positive_count,
                negative_count,
                neutral_count
            ]

            donut = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.60,
                        textinfo="label+percent",
                        textposition="outside",
                        marker=dict(
                            colors=[
                                "#22c55e",
                                "#ef4444",
                                "#f59e0b"
                            ]
                        )
                    )
                ]
            )

            donut.update_layout(
                title={
                    "text": "Overall Sentiment",
                    "x": 0.5
                },
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                showlegend=True
            )

            st.plotly_chart(
                donut,
                use_container_width=True
            )


        # =====================================================
        # BAR CHART
        # =====================================================

        with chart_right:

            bar = go.Figure()

            bar.add_trace(
                go.Bar(
                    x=[
                        "Positive",
                        "Negative",
                        "Neutral"
                    ],
                    y=[
                        positive_count,
                        negative_count,
                        neutral_count
                    ],
                    text=[
                        positive_count,
                        negative_count,
                        neutral_count
                    ],
                    textposition="auto",
                    marker_color=[
                        "#22c55e",
                        "#ef4444",
                        "#f59e0b"
                    ]
                )
            )

            bar.update_layout(
                title={
                    "text": "Number of Titles",
                    "x": 0.5
                },
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.03)",
                font=dict(color="white"),
                xaxis_title="Sentiment",
                yaxis_title="Number of Titles"
            )

            st.plotly_chart(
                bar,
                use_container_width=True
            )


        # =====================================================
        # PERCENTAGE SUMMARY
        # =====================================================

        st.header("📈 Sentiment Percentages")

        if total_count > 0:

            positive_percentage = round(
                (positive_count / total_count) * 100
            )

            negative_percentage = round(
                (negative_count / total_count) * 100
            )

            neutral_percentage = round(
                (neutral_count / total_count) * 100
            )

        else:

            positive_percentage = 0
            negative_percentage = 0
            neutral_percentage = 0


        p1, p2, p3 = st.columns(3)

        with p1:
            st.write("😊 Positive")
            st.progress(
                positive_percentage / 100
            )
            st.caption(
                f"{positive_percentage}%"
            )

        with p2:
            st.write("😞 Negative")
            st.progress(
                negative_percentage / 100
            )
            st.caption(
                f"{negative_percentage}%"
            )

        with p3:
            st.write("😐 Neutral")
            st.progress(
                neutral_percentage / 100
            )
            st.caption(
                f"{neutral_percentage}%"
            )


        # =====================================================
        # QUICK INSIGHT
        # =====================================================

        st.header("💡 Quick Insight")

        if positive_count >= negative_count and positive_count >= neutral_count:

            st.success(
                "😊 Most of the analyzed titles have "
                "a positive emotional tone."
            )

        elif negative_count >= positive_count and negative_count >= neutral_count:

            st.error(
                "😞 Most of the analyzed titles have "
                "a negative emotional tone."
            )

        else:

            st.info(
                "😐 Most of the analyzed titles have "
                "a neutral emotional tone."
            )


        # =====================================================
        # INDIVIDUAL RESULTS
        # =====================================================

        st.header("🎯 Individual Results")

        for _, row in df.iterrows():

            if row["Sentiment"] == "Positive":

                st.success(
                    f"😊 Positive\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )

            elif row["Sentiment"] == "Negative":

                st.error(
                    f"😞 Negative\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )

            else:

                st.info(
                    f"😐 Neutral\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )


        # =====================================================
        # DOWNLOAD
        # =====================================================

        st.header("⬇️ Download Report")

        csv_data = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name="youtube_sentiment_results.csv",
            mime="text/csv",
            use_container_width=True
        )


# =========================================================
# HISTORY
# =========================================================

if history_button:

    st.divider()

    st.header("🕘 Analysis History")

    if not st.session_state.history:

        st.info(
            "No analysis history available yet."
        )

    else:

        history_df = pd.DataFrame(
            st.session_state.history
        )

        history_df["Sentiment"] = history_df[
            "Sentiment"
        ].replace({
            "Positive": "😊 Positive",
            "Negative": "😞 Negative",
            "Neutral": "😐 Neutral"
        })

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.divider()

st.header("🧠 Project Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.subheader("🐍 Python")
    st.write(
        "Used as the main programming language."
    )

with info2:
    st.subheader("🌐 Streamlit")
    st.write(
        "Used to build the web application interface."
    )

with info3:
    st.subheader("🧠 TextBlob")
    st.write(
        "Used for sentiment and polarity analysis."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎬 YouTube Sentiment Analyzer"
)

st.caption(
    "Python • Streamlit • TextBlob • Pandas • Plotly"
)

st.caption(
    "🧠 Natural Language Processing Project"
)