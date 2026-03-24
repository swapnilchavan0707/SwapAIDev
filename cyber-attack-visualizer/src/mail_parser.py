import email
from bs4 import BeautifulSoup
import re
import tldextract


def extract_email_data(file_path):
    """Parses .eml or .txt files for headers, links, and body text."""
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)

    # 1. Extract Basic Headers
    sender = msg.get('From', 'Unknown')
    subject = msg.get('Subject', 'No Subject')
    reply_to = msg.get('Reply-To', 'None')

    # 2. Extract Body and Links
    body = ""
    links = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" or content_type == "text/html":
                payload = part.get_payload(decode=True).decode(errors='ignore')
                body += payload
    else:
        body = msg.get_payload(decode=True).decode(errors='ignore')

    # Find URLs using Regex
    links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', body)

    # Extract Domain and TLD for each link
    domain_info = []
    for link in links:
        ext = tldextract.extract(link)
        domain_info.append({
            'full_url': link,
            'domain': f"{ext.domain}.{ext.suffix}",
            'tld': f".{ext.suffix}"
        })

    return {
        'sender': sender,
        'subject': subject,
        'reply_to': reply_to,
        'body': body,
        'links': domain_info
    }
