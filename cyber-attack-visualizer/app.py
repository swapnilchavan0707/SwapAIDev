import streamlit as st
import os
import pandas as pd
from src.mail_parser import extract_email_data
from src.analyzer import load_threat_db, calculate_urgency_score, get_sender_risk
from src.graph_engine import build_link_graph, plot_link_map
from utils.risk_visualizer import generate_urgency_meter

# 1. Page Config & Times New Roman Styling
st.set_page_config(page_title="Cyber Attack Visualizer", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="st-"], h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        font-family: "Times New Roman", Times, serif !important;
    }
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡 Cybersecurity Attack Visualizer (Spam/Phishing)")
st.markdown("Forensic analysis of suspicious emails, malicious links, and sender reputation.")

# 2. File Upload & Setup
threat_db = load_threat_db()

uploaded_file = st.file_uploader("Upload a Phishing Email Sample (.eml or .txt)", type=["eml", "txt"])

if uploaded_file:
    # Save temp file for parsing
    with open("temp_email.eml", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 3. Data Extraction
    with st.spinner("Analyzing email structure..."):
        email_data = extract_email_data("temp_email.eml")
        urgency_score, word_count = calculate_urgency_score(email_data['body'], threat_db)
        risk_score, risk_cat = get_sender_risk(email_data['sender'])

        # 4. Top Metrics Row
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Urgency Score", f"{urgency_score:.0f}%", delta="High Risk" if urgency_score > 60 else "Normal")
        col_m2.metric("Sender TLD Risk", risk_cat)
        col_m3.metric("Links Extracted", len(email_data['links']))
        col_m4.metric("Threat Keywords", word_count)

        st.divider()

        # 5. Visuals Row: Urgency Meter & Link Map
        col_v1, col_v2 = st.columns([1, 2])

        with col_v1:
            st.subheader("Urgency Meter")
            meter_fig = generate_urgency_meter(urgency_score)
            st.pyplot(meter_fig)

            st.info(f"**Sender:** {email_data['sender']}\n\n**Subject:** {email_data['subject']}")

        with col_v2:
            st.subheader("Link Analysis Map")
            G = build_link_graph(email_data)
            graph_fig = plot_link_map(G)
            st.pyplot(graph_fig)

        st.divider()

        # 6. Detailed Link Report
        st.subheader("Malicious Link Breakdown")
        if email_data['links']:
            link_df = pd.DataFrame(email_data['links'])
            # Add a 'Status' flag for the UI
            link_df['Risk Status'] = link_df['domain'].apply(
                lambda x: "High Risk" if 'xyz' in x or 'bit.ly' in x else "Unknown")
            st.table(link_df[['full_url', 'domain', 'Risk Status']])
        else:
            st.success("No external links detected in this sample.")

    # Cleanup temp file
    os.remove("temp_email.eml")

else:
    st.info("Drag and drop a phishing sample to view the attack structure.")
