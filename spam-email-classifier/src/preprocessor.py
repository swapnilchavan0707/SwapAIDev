import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download necessary NLTK data components
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def clean_text(self, text):
        """
        Performs:
        1. Punctuation removal
        2. Lowercasing
        3. Tokenization
        4. Stopword removal
        5. Stemming
        """
        # Remove punctuation
        text = "".join([char for char in text if char not in string.punctuation])

        # Convert to lowercase and split into words
        words = text.lower().split()

        # Remove stopwords and apply Porter Stemming
        # e.g., 'running' -> 'run', 'winner' -> 'win'
        cleaned_words = [
            self.stemmer.stem(word)
            for word in words
            if word not in self.stop_words
        ]

        # Rejoin into a single string
        return " ".join(cleaned_words)


# Example usage for testing locally:
if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample = "WINNER! You are running for a Rs.1000 prize. Claim now!"
    print(f"Original: {sample}")
    print(f"Cleaned:  {preprocessor.clean_text(sample)}")
