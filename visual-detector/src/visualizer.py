import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np


def generate_wordcloud(data, title, color):
    """Generates a word cloud image from a column of text."""
    text = " ".join(data)
    wc = WordCloud(width=800, height=400, background_color='white', colormap=color).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.title(title, fontsize=20, fontname='Times New Roman')
    plt.axis("off")
    plt.show()


def plot_prediction_bar(probs, labels):
    """Creates a Bar Chart showing AI confidence."""
    plt.figure(figsize=(6, 4))
    sns.barplot(x=labels, y=probs[0], palette=['#ff4b4b', '#00cc96'])
    plt.title("AI Prediction Confidence", fontsize=14, fontname='Times New Roman')
    plt.ylabel("Probability (%)")
    plt.ylim(0, 1)

    # Add percentage labels on top of bars
    for i, p in enumerate(probs[0]):
        plt.text(i, p + 0.02, f'{p * 100:.1f}%', ha='center', fontname='Times New Roman')

    plt.show()
