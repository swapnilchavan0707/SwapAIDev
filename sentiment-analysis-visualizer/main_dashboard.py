import sys
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# 1. Add the path to look for files inside the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Import your custom modules
try:
    from preprocess import clean_movie_text
    from visualizer import generate_sentiment_cloud, plot_sentiment_result
except ImportError:
    # Fallback for some IDE configurations
    from src.preprocess import clean_movie_text
    from src.visualizer import generate_sentiment_cloud, plot_sentiment_result


def run_sentiment_dashboard():
    # Paths for model assets
    model_path = 'models/sentiment_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'
    processed_data_path = 'data/processed/cleaned_reviews.csv'

    # Check if files exist
    if not os.path.exists(model_path) or not os.path.exists(processed_data_path):
        print("Error: Model or Processed Data not found!")
        print("Please run 'python src/train_model.py' first.")
        return

    # Load AI Brain and Data
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    df = pd.read_csv(processed_data_path)

    print("\n" + "=" * 40)
    print("Movie Sentiment AI Dashboard")
    print("=" * 40)

    # --- VISUAL 1: Positive Word Cloud ---
    print("Generating Positive Review Word Cloud...")
    pos_data = df[df['sentiment'] == 1]['review'].astype(str)
    generate_sentiment_cloud(pos_data, "Top Positive Emotion Words", "YlGn")

    # --- VISUAL 2: Negative Word Cloud ---
    print("Generating Negative Review Word Cloud...")
    neg_data = df[df['sentiment'] == 0]['review'].astype(str)
    generate_sentiment_cloud(neg_data, "Top Negative Emotion Words", "OrRd")

    # --- VISUAL 3: Manual Review Analysis ---
    print("\nPaste review to analyze")
    user_review = input("> ")

    if user_review.strip():
        # Clean and Predict
        cleaned = clean_movie_text(user_review)
        vec = vectorizer.transform([cleaned])

        # Get Probabilities [Negative %, Positive %]
        probs = model.predict_proba(vec)[0]
        labels = ['Negative', 'Positive']

        print(f"\nAI Analysis Complete. Showing Confidence Graph...")
        plot_sentiment_result(probs, labels)
    else:
        print("No text entered. Dashboard closing.")

    print("\nVisual Analysis Finished.")


if __name__ == "__main__":
    # Force Times New Roman for a professional project look
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    run_sentiment_dashboard()
