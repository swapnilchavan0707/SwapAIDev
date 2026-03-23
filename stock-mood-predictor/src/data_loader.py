import yfinance as yf
import pandas as pd
import datetime


def fetch_stock_history(ticker, start_date, end_date):
    """
    Downloads historical OHLCV data.
    Handles MultiIndex headers in newer yfinance versions.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return pd.DataFrame()

        # Reset index to make 'Date' a column
        data.reset_index(inplace=True)

        # FIX: Flatten MultiIndex columns (e.g., ('Close', 'AAPL') -> 'Close')
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        return data
    except Exception as e:
        print(f"Price Fetch Error: {e}")
        return pd.DataFrame()


def fetch_news_headlines(ticker):
    """
    New logic to handle yfinance's nested 'content' structure.
    Prevents "['title'] not in index" errors.
    """
    try:
        tk = yf.Ticker(ticker)
        raw_news = tk.news

        if not raw_news:
            return pd.DataFrame()

        processed_news = []
        for item in raw_news:
            # 1. Determine if data is nested in 'content' (new API) or flat (old API)
            data = item.get('content', item)

            # 2. Extract fields with multiple fallback keys for safety
            headline = data.get('title', 'No Title Found')
            source = data.get('publisher', 'Unknown Source')
            url = data.get('clickThroughUrl', data.get('link', '#'))

            # 3. Handle varying date keys (pubDate, providerPublishTime, etc.)
            # New API uses 'pubDate', older used 'providerPublishTime'
            raw_date = data.get('pubDate', data.get('providerPublishTime', 0))

            # Convert ISO string or Timestamp to Unix for consistency
            try:
                if isinstance(raw_date, str):
                    dt_obj = pd.to_datetime(raw_date)
                    timestamp = int(dt_obj.timestamp())
                else:
                    timestamp = int(raw_date)
            except:
                timestamp = 0

            processed_news.append({
                'title': headline,
                'publisher': source,
                'link': url,
                'providerPublishTime': timestamp
            })

        # Create DataFrame with guaranteed columns
        df = pd.DataFrame(processed_news)
        return df

    except Exception as e:
        print(f"News Fetch Error: {e}")
        return pd.DataFrame()