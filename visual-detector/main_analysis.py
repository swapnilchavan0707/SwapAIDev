import sys
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# 1. Fix the path so Python finds your 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# 2. Import your modules
try:
    from preprocess import clean_text
    from visualizer import generate_wordcloud, plot_prediction_bar
except ImportError:
    from src.preprocess import clean_text
    from src.visualizer import generate_wordcloud, plot_prediction_bar

def run_visual_analysis():
    # 1. Check if model exists
    model_path = 'models/fake_news_model.pkl'
    vectorizer_path = 'models/vectorizer.pkl'

    if not os.path.exists(model_path):
        print("Error: Model files not found! Run 'python train_model.py' first.")
        return

    # 2. Load Model and Data
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    df = pd.read_csv('data/raw/news.csv')

    print("\n--- AI visualization started here ---")

    # --- FIGURE 1: Word Cloud for FAKE News ---
    print("Generating Word Cloud for Fake News...")
    fake_data = df[df['label'] == 0]['text'].apply(clean_text)
    generate_wordcloud(fake_data, "Most Common Words in FAKE News", "Reds")

    # --- FIGURE 2: Word Cloud for REAL News ---
    print("Generating Word Cloud for Real News...")
    real_data = df[df['label'] == 1]['text'].apply(clean_text)
    generate_wordcloud(real_data, "Most Common Words in REAL News", "Greens")

    # --- FIGURE 3: Manual Input & Confidence Graph ---
    print("\n" + "=" * 40)
    print("Paste content here..")
    user_input = input("> ")

    if user_input.strip():
        # Process the input
        cleaned = clean_text(user_input)
        vec = vectorizer.transform([cleaned])

        # Get probabilities (how sure the AI is)
        probs = model.predict_proba(vec)[0] # Extract first row
        labels = ['Fake', 'Real']

        print(f"Analysis Complete. Showing Confidence Bar Chart...")
        plot_prediction_bar(probs, labels)
    else:
        print("No text entered. Skipping confidence graph.")

    print("\nAnalysis finished. All figures displayed.")

if __name__ == "__main__":
    # Apply Times New Roman global styling
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    run_visual_analysis()