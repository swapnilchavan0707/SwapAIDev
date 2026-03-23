import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.engine import SentimentEngine

# ================= PAGE CONFIG =================
st.set_page_config(page_title="VibeStream AI", layout="wide")

# ================= LOAD CSS =================
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

engine = SentimentEngine()

# ================= NAVBAR =================
st.markdown("""
<div class="navbar">
    <div class="nav-left">VibeStream AI</div>
</div>
""", unsafe_allow_html=True)

# ================= HERO SECTION =================
st.markdown("""
<div class="hero">
    <h1>Understand Emotions with AI</h1>
    <p>Advanced Emotional Arc & Trend Analysis System</p>
</div>
""", unsafe_allow_html=True)

# ================= INPUT =================
st.markdown('<div class="card">', unsafe_allow_html=True)

user_input = st.text_area(
    "Enter Text",
    height=200,
    placeholder="Paste your text here for analysis..."
)

run_btn = st.button("Run Analysis")

st.markdown('</div>', unsafe_allow_html=True)

# ================= ANALYSIS =================
if run_btn:
    if user_input.strip():

        trend_data = engine.analyze_trend(user_input)
        summary = engine.get_summary(trend_data)
        df = pd.DataFrame(trend_data)

        # ===== METRICS =====
        st.markdown('<div class="card">', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Overall Tone", summary['label'])
        m2.metric("Avg Sentiment", summary['average_score'])
        m3.metric("Peak Positive", f"{summary['peak_positive']:.2f}")
        m4.metric("Sentences", summary['count'])

        st.markdown('</div>', unsafe_allow_html=True)

        # ===== CHARTS =====
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = px.area(df, x="Point", y="Sentiment Score", hover_data=["Sentence"])
            fig.update_layout(font=dict(family="Times New Roman"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            pos = len(df[df['Sentiment Score'] > 0.05])
            neg = len(df[df['Sentiment Score'] < -0.05])
            neu = len(df) - (pos + neg)

            pie = px.pie(
                values=[pos, neg, neu],
                names=["Positive", "Negative", "Neutral"]
            )
            pie.update_layout(font=dict(family="Times New Roman"))
            st.plotly_chart(pie, use_container_width=True)

        # ===== TABLE =====
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.dataframe(df)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("Please enter valid text")

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    © 2024 VibeStream AI | Analytics Engine
</div>
""", unsafe_allow_html=True)