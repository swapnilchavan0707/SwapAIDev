import re
import string


def clean_movie_text(text):
    """
    Cleans movie reviews: removes punctuation, numbers,
    and common words that clutter graphs.
    """
    text = str(text).lower()
    # Remove text in brackets
    text = re.sub('\[.*?\]', '', text)
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    # Remove words with numbers
    text = re.sub('\w*\d\w*', '', text)
    # Remove extra spaces
    text = re.sub(' +', ' ', text)

    # Custom: Remove 'movie' and 'film' so they don't take over the Word Cloud
    noise_words = ['movie', 'film', 'show', 'watch', 'acting', 'actor']
    for word in noise_words:
        text = text.replace(word, '')

    return text.strip()
