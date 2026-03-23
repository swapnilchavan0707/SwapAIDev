import sys
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Fix the path so Python finds your 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Import your cleaning function
try:
    from preprocess import clean_text
except ImportError:
    # Fallback if pathing is strict in some IDEs
    from src.preprocess import clean_text


def train():
    # --- STEP 1: Load Data ---
    data_path = 'data/raw/news.csv'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found!")
        return

    df = pd.read_csv(data_path)

    # --- STEP 2: Clean text ---
    # This applies the cleaning logic from your src/preprocess.py
    df['text'] = df['text'].apply(clean_text)

    # --- STEP 3: Save to Processed Folder (THE UPDATE) ---
    # This ensures your 'processed' folder is no longer empty
    processed_path = 'data/processed'
    os.makedirs(processed_path, exist_ok=True)

    output_file = os.path.join(processed_path, 'cleaned_news.csv')
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to: {output_file}")

    # --- STEP 4: Model Training ---
    X = df['text']
    y = df['label']

    # Vectorize
    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)

    # Train
    model = LogisticRegression()
    model.fit(X_tfidf, y)

    # --- STEP 5: Save AI Assets ---
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/fake_news_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("Model trained and saved in 'models/' folder!")


if __name__ == "__main__":
    train()
