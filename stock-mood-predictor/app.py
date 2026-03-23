import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.data_loader import fetch_stock_history, fetch_news_headlines
from src.processor import calculate_sentiment, aggregate_daily_mood
from src.visualizer import plot_trend_line, plot_candlestick_with_signals

# Page Config
st.set_page_config(page_title="Stock Market Mood Predictor", layout="wide")

st.title("Stock Market 'Mood' Predictor")
st.markdown("""
    <style>
    /* Targets the entire app body and all headers */
    html, body, [class*="st-"], h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        font-family: "Times New Roman", Times, serif !important;
    }
    /* Specifically targets sidebar text */
    [data-testid="stSidebar"] {
        font-family: "Times New Roman", Times, serif !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("This AI tool compares daily financial news sentiment against stock price movements.")

# Sidebar - User Inputs
st.sidebar.header("Settings")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
days_back = st.sidebar.slider("Days of History", min_value=7, max_value=60, value=30)

start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

if st.sidebar.button("Analyze Mood"):
    with st.spinner(f'Fetching and analyzing data for {ticker}...'):
        try:
            # 1. Fetch Data
            price_data = fetch_stock_history(ticker, start_date, end_date)
            news_data = fetch_news_headlines(ticker)

            if news_data.empty:
                st.error("No news found for this ticker.")
            else:
                # 2. Process Sentiment
                news_with_sentiment = calculate_sentiment(news_data)
                merged_df = aggregate_daily_mood(news_with_sentiment, price_data)

                # --- Visuals Section ---
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.subheader("Trend Overlay: Price vs. Sentiment")
                    trend_fig = plot_trend_line(merged_df, ticker)
                    st.plotly_chart(trend_fig, use_container_width=True)

                with col2:
                    st.subheader("Latest Headlines & Sentiment")
                    # Display top 5 headlines with their scores
                    display_news = news_with_sentiment[['title', 'sentiment_score']].head(10)
                    st.dataframe(display_news, hide_index=True)

                st.divider()

                st.subheader("Candlestick Analysis with AI Signals")
                candle_fig = plot_candlestick_with_signals(merged_df)
                st.plotly_chart(candle_fig, use_container_width=True)

                # --- Statistics ---
                st.divider()
                avg_mood = merged_df['sentiment_score'].mean()
                mood_label = "Bullish" if avg_mood > 0.05 else "Bearish" if avg_mood < -0.05 else "Neutral"

                st.metric(label=f"Overall {ticker} Mood (Last {days_back} Days)", value=mood_label,
                          delta=f"{avg_mood:.2f} Score")

        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check if the ticker symbol is correct or if you've hit an API rate limit.")

else:
    st.info("Enter a ticker symbol and click 'Analyze Mood' to begin.")
