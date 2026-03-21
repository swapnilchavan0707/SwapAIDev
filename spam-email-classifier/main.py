import pandas as pd
from src.preprocessor import TextPreprocessor
from src.feature_engine import FeatureEngine
from src.classifier import SpamClassifier
from sklearn.model_selection import train_test_split


def run_pipeline():
    # 1. Initialize Components
    preprocessor = TextPreprocessor()
    engine = FeatureEngine()
    classifier = SpamClassifier()

    # 2. Load and Preprocess Data
    print("Loading data...")
    try:
        df = pd.read_csv('data/spam_data.csv')
    except FileNotFoundError:
        print("Error: data/spam_data.csv not found!")
        return

    print("Cleaning text (this may take a moment)...")
    df['cleaned_text'] = df['text'].apply(preprocessor.clean_text)

    # 3. Feature Extraction
    X = engine.fit_transform(df['cleaned_text'])
    y = df['label']

    # 4. Split and Train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training model...")
    classifier.train(X_train, y_train)

    # 5. Evaluate
    accuracy, report = classifier.evaluate(X_test, y_test)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:\n", report)

    # 6. Save for future use
    engine.save_vectorizer()
    classifier.save_model()

    # 7. Real-time Prediction Test
    print("\n--- Testing Single Prediction ---")
    test_email = "CONGRATULATIONS! You've won a $500 gift card. Click here now!"

    # Process the new email exactly like the training data
    cleaned_email = preprocessor.clean_text(test_email)
    vectorized_email = engine.transform([cleaned_email])
    prediction = classifier.predict(vectorized_email)

    result = "SPAM" if prediction[0] == 1 else "HAM (Legit)"
    print(f"Email: {test_email}")
    print(f"Prediction: {result}")


if __name__ == "__main__":
    run_pipeline()