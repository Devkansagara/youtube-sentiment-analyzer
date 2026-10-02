import streamlit as st
import pandas as pd
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
# SIMPLE DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #172554 0%, transparent 30%),
        radial-gradient(circle at 90% 15%, #3b0764 0%, transparent 30%),
        linear-gradient(135deg, #050816, #0b1228, #111827);
}

.block-container {
    max-width: 1200px;
    padding-top: 30px;
    padding-bottom: 40px;
}

/* Main bordered container */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* Buttons */
.stButton > button {
    border-radius: 14px;
    height: 50px;
    font-weight: 700;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
}

textarea {
    border-radius: 15px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# MAIN HEADER
# =========================================================

with st.container(border=True):

    st.title("🎬 YouTube Sentiment Analyzer")

    st.subheader(
        "AI-powered analysis of YouTube video titles"
    )

    st.write(
        "🧠 Natural Language Processing   •   "
        "🤖 Sentiment Analysis   •   "
        "▶️ YouTube"
    )


# =========================================================
# HOW IT WORKS
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
            "The polarity score determines sentiment."
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
# INPUT
# =========================================================

st.header("🔎 Analyze YouTube Video Titles")

st.write(
    "Enter one YouTube title per line:"
)

titles_text = st.text_area(
    "YouTube Titles",
    height=170,
    placeholder=(
        "Example:\n"
        "This movie is absolutely amazing\n"
        "I hate this boring movie\n"
        "New technology trends in 2026\n"
        "I love this beautiful video"
    )
)


# =========================================================
# BUTTONS
# =========================================================

b1, b2, b3 = st.columns(3)

with b1:

    analyze_button = st.button(
        "🚀 Analyze Sentiment",
        use_container_width=True
    )

with b2:

    clear_button = st.button(
        "🧹 Clear",
        use_container_width=True
    )

with b3:

    history_button = st.button(
        "🕘 View History",
        use_container_width=True
    )


# =========================================================
# CLEAR
# =========================================================

if clear_button:

    st.session_state.history = []

    st.rerun()


# =========================================================
# ANALYSIS FUNCTION
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
# ANALYZE
# =========================================================

if analyze_button:

    if not titles_text.strip():

        st.warning(
            "⚠️ Please enter at least one YouTube title."
        )

    else:

        titles = [
            x.strip()
            for x in titles_text.split("\n")
            if x.strip()
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
        # COUNTS
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
        # OVERVIEW
        # =====================================================

        st.divider()

        st.header("📊 Sentiment Overview")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "😊 Positive Titles",
                positive_count
            )

        with c2:

            st.metric(
                "😞 Negative Titles",
                negative_count
            )

        with c3:

            st.metric(
                "😐 Neutral Titles",
                neutral_count
            )

        with c4:

            st.metric(
                "🎬 Total Titles",
                total_count
            )


        # =====================================================
        # TABLE
        # =====================================================

        st.header("📋 Detailed Analysis")

        display_df = df.copy()

        display_df["Sentiment"] = (
            display_df["Sentiment"].replace(
                {
                    "Positive": "😊 Positive",
                    "Negative": "😞 Negative",
                    "Neutral": "😐 Neutral"
                }
            )
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        # =====================================================
        # DONUT CHART
        # =====================================================

        st.header("🍩 Sentiment Distribution")

        chart_data = pd.DataFrame(
            {
                "Sentiment": [
                    "Positive",
                    "Negative",
                    "Neutral"
                ],
                "Count": [
                    positive_count,
                    negative_count,
                    neutral_count
                ]
            }
        )

        donut_spec = {

            "mark": {
                "type": "arc",
                "innerRadius": 80,
                "stroke": "#0f172a",
                "strokeWidth": 3
            },

            "encoding": {

                "theta": {
                    "field": "Count",
                    "type": "quantitative"
                },

                "color": {
                    "field": "Sentiment",
                    "type": "nominal",
                    "scale": {
                        "domain": [
                            "Positive",
                            "Negative",
                            "Neutral"
                        ],
                        "range": [
                            "#22c55e",
                            "#ef4444",
                            "#f59e0b"
                        ]
                    },

                    "legend": {
                        "orient": "bottom"
                    }
                },

                "tooltip": [
                    {
                        "field": "Sentiment",
                        "type": "nominal"
                    },
                    {
                        "field": "Count",
                        "type": "quantitative"
                    }
                ]
            }
        }

        st.vega_lite_chart(
            chart_data,
            donut_spec,
            use_container_width=True
        )


        # =====================================================
        # PERCENTAGES
        # =====================================================

        st.header("📈 Sentiment Percentages")

        if total_count > 0:

            positive_percentage = round(
                positive_count / total_count * 100
            )

            negative_percentage = round(
                negative_count / total_count * 100
            )

            neutral_percentage = round(
                neutral_count / total_count * 100
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

        if (
            positive_count >= negative_count
            and positive_count >= neutral_count
        ):

            st.success(
                "😊 Most of the analyzed titles have "
                "a positive emotional tone."
            )

        elif (
            negative_count >= positive_count
            and negative_count >= neutral_count
        ):

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
                    f"😊 **Positive**\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )

            elif row["Sentiment"] == "Negative":

                st.error(
                    f"😞 **Negative**\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )

            else:

                st.info(
                    f"😐 **Neutral**\n\n"
                    f"**Title:** {row['Title']}\n\n"
                    f"**Polarity Score:** {row['Score']}\n\n"
                    f"**Subjectivity:** {row['Subjectivity']}"
                )


        # =====================================================
        # DOWNLOAD REPORT
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

        history_df["Sentiment"] = (
            history_df["Sentiment"].replace(
                {
                    "Positive": "😊 Positive",
                    "Negative": "😞 Negative",
                    "Neutral": "😐 Neutral"
                }
            )
        )

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

i1, i2, i3 = st.columns(3)

with i1:

    st.subheader("🐍 Python")

    st.write(
        "Main programming language used "
        "for the project."
    )

with i2:

    st.subheader("🌐 Streamlit")

    st.write(
        "Used to create the interactive "
        "web application."
    )

with i3:

    st.subheader("🧠 TextBlob")

    st.write(
        "Used to calculate sentiment "
        "and polarity."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎬 YouTube Sentiment Analyzer"
)

st.caption(
    "Python • Streamlit • TextBlob • Pandas"
)

st.caption(
    "🧠 Natural Language Processing Project"
)
