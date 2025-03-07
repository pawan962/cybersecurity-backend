import certifi
import os
import smtplib
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
import os
import smtplib
import urllib.parse
import certifi
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# ✅ MongoDB Credentials (ENCODED to prevent errors)
USERNAME = urllib.parse.quote_plus("pawan962")  # Replace with your username
PASSWORD = urllib.parse.quote_plus("Pawan0509")  # Replace with your password

import certifi
MONGO_URI = "mongodb+srv://pawan962:Pawan0509@your-cluster.mongodb.net/cybersecurity_db?retryWrites=true&w=majority&tls=true"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client["cybersecurity_db"]
threats_collection = db["threat_logs"]

@app.route('/get-threats', methods=['GET'])
def get_threats():
    """Retrieve stored threats from MongoDB."""
    threats = list(threats_collection.find({}, {"_id": 0}))
    return jsonify(threats)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

# ✅ Email Configuration
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_16_character_app_password"

def send_email_alert(subject, body, recipient):
    """Send an email alert using Gmail SMTP."""
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_USER, recipient, message)
        server.quit()
        print(f"✅ Email alert sent successfully to {recipient}!")
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")

@app.route('/detect-threat', methods=['POST'])
def detect_threat():
    """Detect a threat and trigger alerts."""
    threat = {
        "attack_type": "DDoS",
        "source_ip": "192.168.1.100",
        "timestamp": "2025-03-02T12:00:00Z",
        "status": "blocked"
    }
    threats_collection.insert_one(threat)

    # Send Email Alert
    send_email_alert(
        "🚨 Cybersecurity Threat Detected!",
        f"Threat Type: {threat['attack_type']} detected from {threat['source_ip']}. Immediate action required!",
        "admin@example.com"
    )

    return jsonify({"message": "Threat detected & alert sent!"})

@app.route('/get-threats', methods=['GET'])
def get_threats():
    """Retrieve stored threats from MongoDB."""
    threats = list(threats_collection.find({}, {"_id": 0}))
    return jsonify(threats)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

