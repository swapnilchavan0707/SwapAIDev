import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def generate_sentiment_cloud(data, title, color_map):
    """Generates a word cloud for Positive or Negative reviews."""
    text = " ".join(data)
    wc = WordCloud(width=800, height=400, background_color='white', colormap=color_map).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(title, fontsize=18, fontname='Times New Roman')
    plt.axis("off")
    plt.show()


def plot_sentiment_result(probs, labels):
    """Creates a Bar Chart showing how Positive or Negative the AI thinks it is."""
    plt.figure(figsize=(7, 4))
    sns.barplot(x=labels, y=probs, palette=['#e74c3c', '#2ecc71'])
    plt.title("AI Sentiment Analysis", fontsize=15, fontname='Times New Roman')
    plt.ylabel("Confidence (%)")
    plt.ylim(0, 1)

    # Add percentage labels
    for i, p in enumerate(probs):
        plt.text(i, p + 0.02, f'{p * 100:.1f}%', ha='center', fontname='Times New Roman')

    plt.show()