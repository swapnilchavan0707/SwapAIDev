import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()


def calculate_sentiment(df):
    """
    Safely calculates sentiment scores for headlines.
    Handles cases where 'title' or 'headline' might be the column name.
    """
    if df.empty:
        return df

    # Find the column that contains the text (usually 'title' or 'headline')
    text_col = 'title' if 'title' in df.columns else 'headline' if 'headline' in df.columns else None

    if not text_col:
        # Fallback: use the first string column found
        text_col = df.select_dtypes(include=['object']).columns[0]

    # Apply VADER sentiment
    df['sentiment_score'] = df[text_col].apply(
        lambda x: analyzer.polarity_scores(str(x))['compound']
    )
    return df


def aggregate_daily_mood(news_df, price_df):
    """
    Merges news sentiment with price data by Date.
    Handles varying date column names from yfinance.
    """
    if news_df.empty or price_df.empty:
        return pd.DataFrame()

    # 1. Identify the Date column in News (could be 'providerPublishTime' or 'date')
    if 'providerPublishTime' in news_df.columns:
        news_df['date'] = pd.to_datetime(news_df['providerPublishTime'], unit='s').dt.date
    elif 'date' in news_df.columns:
        news_df['date'] = pd.to_datetime(news_df['date']).dt.date
    else:
        # Last resort: use the index if it's a DatetimeIndex
        news_df['date'] = pd.to_datetime(news_df.index).date

    # 2. Identify the Date column in Price (usually 'Date' or index)
    if 'Date' in price_df.columns:
        price_df['date'] = pd.to_datetime(price_df['Date']).dt.date
    else:
        price_df['date'] = pd.to_datetime(price_df.index).date

    # 3. Group news by date to get the "Daily Mood"
    daily_sentiment = news_df.groupby('date')['sentiment_score'].mean().reset_index()

    # 4. Merge News and Prices
    # We use 'left' join on price_df to keep all trading days even if no news exists
    merged_df = pd.merge(price_df, daily_sentiment, on='date', how='left')

    # Fill days with no news as 'Neutral' (0.0 sentiment)
    merged_df['sentiment_score'] = merged_df['sentiment_score'].fillna(0)

    return merged_df


def get_keyword_correlation(df, news_df):
    """
    Creates a correlation matrix between specific 'Mood' keywords and price returns.
    """
    keywords = ['earnings', 'growth', 'crash', 'warns', 'rally', 'downgrade', 'surge', 'dip']

    # Calculate daily price return percentage
    df['Price_Return'] = df['Close'].pct_change()

    # Build binary keyword columns
    for word in keywords:
        df[word] = df['date'].apply(lambda d: 1 if news_df[
                                                       (pd.to_datetime(news_df['date']).dt.date == d) &
                                                       (news_df['title'].str.lower().str.contains(word, na=False))
                                                       ].shape[0] > 0 else 0)

    # Filter columns that actually have data (avoid all-zero columns crashing the corr)
    active_cols = [w for w in keywords if df[w].any()] + ['Price_Return']
    return df[active_cols].corr().fillna(0)