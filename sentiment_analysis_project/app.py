import streamlit as st
import os
import sys

# Add the current directory to path so it can find the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.predict import predict_sentiment

# 1. Page Configuration
st.set_page_config(page_title="Sentiment Analyzer", layout="centered")

# 2. Inject Custom CSS for Times New Roman Font
st.markdown(
    """
    <style>
    /* Import and apply Times New Roman to all elements */
    * {
        font-family: "Times New Roman", Times, serif !important;
    }

    /* Styling the Main Title */
    .main-title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Styling the Prediction Result Box */
    .result-box {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
    }

    .pos {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .neg {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. App UI
st.markdown('<div class="main-title">Sentiment Analysis Project</div>', unsafe_allow_html=True)

st.write("Enter a sentence below to determine if the sentiment is **Positive** or **Negative**.")

# Input text area
user_input = st.text_area("User Review / Text Input:", placeholder="Type something like 'I love this project!'...")

# Predict Button
if st.button("Analyze Sentiment"):
    if user_input.strip():
        # Call the prediction function from src/predict.py
        result = predict_sentiment(user_input)

        # Displaying result with custom styled boxes
        if result == "Positive":
            st.markdown(f'<div class="result-box pos">Result: {result} 😊</div>', unsafe_allow_html=True)
        elif result == "Negative":
            st.markdown(f'<div class="result-box neg">Result: {result} ☹️</div>', unsafe_allow_html=True)
        else:
            # For errors (like model file missing)
            st.error(result)
    else:
        st.warning("Please enter some text before clicking predict.")

# 4. Footer
st.markdown("---")
st.caption("Project powered by Python, Scikit-Learn, and Streamlit.")