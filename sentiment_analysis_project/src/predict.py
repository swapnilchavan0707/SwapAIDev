import joblib
import os
from .preprocess import clean_text

# Get the path of the models folder relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'sentiment_model.pkl')
VECTOR_PATH = os.path.join(BASE_DIR, 'models', 'tfidf_vectorizer.pkl')


def predict_sentiment(text):
    try:
        # Load the saved model and vectorizer
        model = joblib.load(MODEL_PATH)
        tfidf = joblib.load(VECTOR_PATH)

        # Process the input
        cleaned = clean_text(text)
        vectorized = tfidf.transform([cleaned])

        # Predict
        prediction = model.predict(vectorized)[0]

        return "Positive" if prediction == 1 else "Negative"
    except FileNotFoundError:
        return "Error: Model files not found. Please run train.py first."