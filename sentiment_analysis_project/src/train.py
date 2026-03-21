import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import clean_text


def train_model():
    # Ensure models directory exists
    if not os.path.exists('models'):
        os.makedirs('models')

    # Load data
    df = pd.read_csv('data/raw_data.csv')

    # Preprocess
    print("Preprocessing text...")
    df['cleaned_text'] = df['text'].apply(clean_text)

    # Vectorization
    tfidf = TfidfVectorizer(max_features=5000)
    X = tfidf.fit_transform(df['cleaned_text'])
    y = df['sentiment']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    print("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Save artifacts
    joblib.dump(model, 'models/sentiment_model.pkl')
    joblib.dump(tfidf, 'models/tfidf_vectorizer.pkl')
    print("Success: Model and Vectorizer saved in 'models/' folder.")


if __name__ == "__main__":
    train_model()