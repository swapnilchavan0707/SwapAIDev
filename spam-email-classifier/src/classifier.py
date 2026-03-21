from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class SpamClassifier:
    def __init__(self, alpha=1.0):
        # alpha=1.0 is Laplace smoothing, which handles words not seen in training
        self.model = MultinomialNB(alpha=alpha)

    def train(self, X_train, y_train):
        """
        Trains the Naive Bayes model using the vectorized training data.
        """
        self.model.fit(X_train, y_train)
        print("Model training complete.")

    def evaluate(self, X_test, y_test):
        """
        Evaluates the model and prints performance metrics.
        """
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        return accuracy, report

    def predict(self, X_vectorized):
        """
        Predicts the class (0 or 1) for new, vectorized email text.
        """
        return self.model.predict(X_vectorized)

    def save_model(self, path='models/spam_model.pkl'):
        """
        Saves the trained model to a file using joblib.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        print(f"Model saved to {path}")

    def load_model(self, path='models/spam_model.pkl'):
        """
        Loads a saved model from disk for making predictions.
        """
        if os.path.exists(path):
            self.model = joblib.load(path)
            return True
        return False
