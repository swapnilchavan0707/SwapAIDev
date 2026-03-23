import sys
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Add src to path to import clean_movie_text
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from preprocess import clean_movie_text


def train_sentiment():
    # 1. Load Data
    data_path = 'data/raw/movie_reviews.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found!")
        return

    df = pd.read_csv(data_path)

    # 2. Clean and SAVE TO PROCESSED FOLDER
    print("Cleaning data...")
    df['review'] = df['review'].apply(clean_movie_text)

    processed_path = 'data/processed'
    os.makedirs(processed_path, exist_ok=True)
    df.to_csv(f'{processed_path}/cleaned_reviews.csv', index=False)
    print(f"Processed data saved to {processed_path}/cleaned_reviews.csv")

    # 3. Model Training
    X = df['review']
    y = df['sentiment']

    vectorizer = TfidfVectorizer(max_features=2000)
    X_tfidf = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_tfidf, y)

    # 4. Save AI Brain
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/sentiment_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("Sentiment model trained and saved!")


if __name__ == "__main__":
    train_sentiment()