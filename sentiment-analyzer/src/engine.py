from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


class SentimentEngine:
    """
    The AI Brain of the project.
    It processes raw text into mathematical emotional trajectories.
    """

    def __init__(self):
        # Initialize the VADER sentiment analyzer
        self.analyzer = SentimentIntensityAnalyzer()

    def clean_text(self, text):
        """Basic cleaning to remove empty lines and extra spaces."""
        return text.strip()

    def get_sentences(self, text):
        """Splits text into meaningful chunks/sentences."""
        # Splitting by common sentence terminators
        sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if len(s.strip()) > 3]
        return sentences

    def analyze_trend(self, text):
        """
        Processes text and returns a list of dictionaries
        representing the 'Emotional Arc' of the content.
        """
        cleaned_text = self.clean_text(text)
        sentences = self.get_sentences(cleaned_text)

        trend_data = []

        for index, sentence in enumerate(sentences):
            # The 'compound' score is the normalized, weighted composite score
            # ranging from -1 (extremely negative) to +1 (extremely positive).
            scores = self.analyzer.polarity_scores(sentence)

            trend_data.append({
                "Point": index + 1,
                "Sentence": sentence[:50] + "..." if len(sentence) > 50 else sentence,
                "Sentiment Score": scores['compound'],
                "Positivity": scores['pos'],
                "Negativity": scores['neg'],
                "Neutrality": scores['neu']
            })

        return trend_data

    def get_summary(self, trend_data):
        """Calculates high-level stats for the UI dashboard."""
        if not trend_data:
            return None

        df = pd.DataFrame(trend_data)
        avg_score = df['Sentiment Score'].mean()

        # Determine the overall 'Vibe'
        if avg_score >= 0.05:
            label = "Positive"
        elif avg_score <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return {
            "average_score": round(avg_score, 3),
            "label": label,
            "peak_positive": df['Sentiment Score'].max(),
            "peak_negative": df['Sentiment Score'].min(),
            "count": len(df)
        }
