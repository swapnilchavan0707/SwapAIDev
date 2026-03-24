import os
import pandas as pd
from src.mail_parser import extract_email_data
from src.analyzer import load_threat_db, calculate_urgency_score
from src.visualizer import save_urgency_meter, save_link_map


def run_forensic_audit():
    print("Initializing Forensic Audit...")

    # Setup
    threat_db = load_threat_db()
    email_folder = "data/raw_emails"

    # Process every file in the folder
    files = [f for f in os.listdir(email_folder) if f.endswith(('.eml', '.txt'))]

    if not files:
        print("No email samples found in data/raw_emails/")
        return

    for file in files:
        print(f"Analyzing: {file}...")
        file_path = os.path.join(email_folder, file)
        base_name = os.path.splitext(file)[0]

        # 1. Forensic Extraction
        data = extract_email_data(file_path)

        # 2. Score Calculation
        score, _ = calculate_urgency_score(data['body'], threat_db)

        # 3. Visual Generation (Save to Folder)
        m_path = save_urgency_meter(score, base_name)
        g_path = save_link_map(data, base_name)

        print(f"   Saved: {m_path}")
        print(f"   Saved: {g_path}")

    print("\n Audit Complete. Check the 'forensic_reports' folder for results.")


if __name__ == "__main__":
    run_forensic_audit()