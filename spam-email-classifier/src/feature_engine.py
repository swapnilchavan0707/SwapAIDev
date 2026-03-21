from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

class FeatureEngine:
    def __init__(self, max_features=3000):
        # max_features limits the vocabulary to the top 3000 words to prevent overfitting
        self.vectorizer = TfidfVectorizer(max_features=max_features)

    def fit_transform(self, text_series):
        """
        Learns the vocabulary and returns the document-term matrix.
        """
        return self.vectorizer.fit_transform(text_series)

    def transform(self, text_series):
        """
        Transforms text into the learned TF-IDF space (used for prediction).
        """
        return self.vectorizer.transform(text_series)

    def save_vectorizer(self, path='models/vectorizer.pkl'):
        """
        Saves the fitted vectorizer so it can be reused for live predictions.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.vectorizer, path)
        print(f"Vectorizer saved to {path}")

    def load_vectorizer(self, path='models/vectorizer.pkl'):
        """
        Loads a saved vectorizer from disk.
        """
        if os.path.exists(path):
            self.vectorizer = joblib.load(path)
            return True
        return False