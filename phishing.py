{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 ArialMT;\f1\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww29200\viewh18380\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs29\fsmilli14667 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import imapclient
\f1\fs24 \

\f0\fs29\fsmilli14667 import email
\f1\fs24 \

\f0\fs29\fsmilli14667 import re
\f1\fs24 \

\f0\fs29\fsmilli14667 import requests
\f1\fs24 \

\f0\fs29\fsmilli14667 from email.header import decode_header
\f1\fs24 \

\f0\fs29\fsmilli14667 import pandas as pd
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # IMAP Server Details (Change for Gmail, Outlook, Yahoo, etc.)
\f1\fs24 \

\f0\fs29\fsmilli14667 IMAP_SERVER = "imap.gmail.com"
\f1\fs24 \

\f0\fs29\fsmilli14667 EMAIL_ACCOUNT = "xvikramsharma@gmail.com"
\f1\fs24 \

\f0\fs29\fsmilli14667 EMAIL_PASSWORD = "Xvikram++"\'a0 # Use App Passwords if 2FA is enabled
\f1\fs24 \

\f0\fs29\fsmilli14667 FOLDER = "INBOX"\'a0 # Change to 'Spam' to collect flagged phishing emails
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # VirusTotal API (Optional for URL Checking)
\f1\fs24 \

\f0\fs29\fsmilli14667 VIRUSTOTAL_API_KEY = "your_virustotal_api_key"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Connect to Email via IMAP
\f1\fs24 \

\f0\fs29\fsmilli14667 def fetch_emails():
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0with imapclient.IMAPClient(IMAP_SERVER, ssl=True) as client:
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0client.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0client.select_folder(FOLDER, readonly=True)
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0# Fetch all emails
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0messages = client.search(["ALL"])
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0raw_emails = client.fetch(messages, ["RFC822"])
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0emails = []
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0for msgid, data in raw_emails.items():
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0msg = email.message_from_bytes(data[b"RFC822"])
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0email_details = parse_email(msg)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0emails.append(email_details)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0return emails
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Parse Email Content
\f1\fs24 \

\f0\fs29\fsmilli14667 def parse_email(msg):
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0subject, encoding = decode_header(msg["Subject"])[0]
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0subject = subject.decode(encoding) if isinstance(subject, bytes) else subject
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0sender = msg["From"]
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0reply_to = msg.get("Reply-To", "N/A")
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0# Extract URLs
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0urls = extract_links(msg)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0return \{"Subject": subject, "Sender": sender, "Reply-To": reply_to, "URLs": urls\}
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Extract Links from Email Body
\f1\fs24 \

\f0\fs29\fsmilli14667 def extract_links(msg):
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0urls = []
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0if msg.is_multipart():
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0for part in msg.walk():
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0if part.get_content_type() == "text/plain":
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0text = part.get_payload(decode=True).decode(errors="ignore")
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0urls.extend(re.findall(r"http[s]?://[^\\s]+", text))
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0return urls
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Check URLs Against VirusTotal (Optional)
\f1\fs24 \

\f0\fs29\fsmilli14667 def check_urls(urls):
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0safe, phishing = [], []
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0for url in urls:
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0response = requests.get(f"https://www.virustotal.com/api/v3/urls/\{url\}",\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0headers=\{"x-apikey": VIRUSTOTAL_API_KEY\})
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0data = response.json()
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0if data.get("data", \{\}).get("attributes", \{\}).get("last_analysis_stats", \{\}).get("malicious", 0) > 0:
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0phishing.append(url)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0else:
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0safe.append(url)
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0return safe, phishing
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Main Execution
\f1\fs24 \

\f0\fs29\fsmilli14667 emails = fetch_emails()
\f1\fs24 \

\f0\fs29\fsmilli14667 df = pd.DataFrame(emails)
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Save Data to CSV for Analysis
\f1\fs24 \

\f0\fs29\fsmilli14667 df.to_csv("phishing_emails.csv", index=False)
\f1\fs24 \
\

\f0\fs29\fsmilli14667 print("Phishing email analysis completed. Check phishing_emails.csv")
\f1\fs24 \
\
\
\
}