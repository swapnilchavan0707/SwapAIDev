import json
import pandas as pd


def load_threat_db():
    with open('data/malicious_db.json', 'r') as f:
        return json.load(f)


def calculate_urgency_score(body, threat_db):
    """Counts high-pressure words to set the Urgency Meter."""
    text = body.lower()
    keywords = threat_db.get('urgency_keywords', [])

    # Count occurrences
    count = sum(1 for word in keywords if word in text)

    # Normalize score 0-100 (Max 10 keywords for 100%)
    score = min((count / 10) * 100, 100)
    return score, count


def get_sender_risk(sender_email, tld_csv_path='data/tld_risk_scores.csv'):
    """Checks TLD against the risk database for the Bubble Chart."""
    tld_df = pd.read_csv(tld_csv_path)
    sender_tld = "." + sender_email.split('.')[-1].replace(">", "")

    match = tld_df[tld_df['TLD'] == sender_tld]
    if not match.empty:
        return match.iloc[0]['Risk_Score'], match.iloc[0]['Category']
    return 20, "Unknown"  # Default low-mid risk for common TLDs
