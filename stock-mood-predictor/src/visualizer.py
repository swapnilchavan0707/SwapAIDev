import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Standardized font for all charts
CHART_FONT = "Times New Roman"


def plot_trend_line(df, ticker):
    """
    Overlays daily news sentiment on top of stock closing prices.
    Uses 'Times New Roman' for all text elements.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Stock Price Line
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['Close'], name="Stock Price", line=dict(color='#007bff')),
        secondary_y=False,
    )

    # Add Sentiment Score Bars
    fig.add_trace(
        go.Bar(x=df['date'], y=df['sentiment_score'], name="News Sentiment", opacity=0.4, marker_color='orange'),
        secondary_y=True,
    )

    fig.update_layout(
        title=dict(text=f"{ticker} | Price vs. Market Mood Overlay", x=0.5),
        template="plotly_dark",
        font_family=CHART_FONT,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Specifically ensure axis titles use the font
    fig.update_yaxes(title_text="Sentiment Score (-1 to 1)", secondary_y=True)

    return fig


def plot_candlestick_with_signals(df):
    """
    Standard trading chart with AI markers.
    Uses 'Times New Roman' for the range slider and labels.
    """
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Market Data"
    )])

    # AI Signals: Buy if sentiment is strongly positive (> 0.4)
    buys = df[df['sentiment_score'] > 0.4]
    fig.add_trace(go.Scatter(
        x=buys['date'],
        y=buys['Low'] * 0.97,
        mode='markers',
        marker=dict(symbol='triangle-up', size=14, color='#00ff00'),
        name='AI Buy Signal'
    ))

    fig.update_layout(
        title=dict(text="Trading Technicals with AI Sentiment Markers", x=0.5),
        template="plotly_dark",
        font_family=CHART_FONT,
        yaxis_title="Stock Price",
        xaxis_rangeslider_visible=True  # Standard for candlesticks
    )

    return fig


def plot_correlation_heatmap(corr_matrix):
    """
    Visualizes the relationship between news keywords and price changes.
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale='RdBu_r',
        title="Keyword Correlation Heatmap"
    )

    fig.update_layout(
        font_family=CHART_FONT,
        template="plotly_dark",
        title_x=0.5
    )

    return fig