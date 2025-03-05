import os
import smtplib
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

from pymongo import MongoClient

# Correct MongoDB Connection String
client = MongoClient("mongodb+srv://pawan962:Pawan0509@cluster0.2ulqp.mongodb.net/cybersecurity_db?retryWrites=true&w=majority")
db = client["cybersecurity_db"]
threats_collection = db["threat_logs"]

# Email Configuration
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

@app.route("/", methods=["GET"])
def home():
    """Home Route - Check if API is Running"""
    return jsonify({"message": "AI Cybersecurity Backend is Running!"})

@app.route('/detect-threat', methods=['POST'])
def detect_threat():
    """Detect a threat and trigger alerts."""
    data = request.json
    threat = {
        "attack_type": data.get("attack_type", "Unknown"),
        "source_ip": data.get("source_ip", "0.0.0.0"),
        "timestamp": data.get("timestamp", "Unknown"),
        "status": "blocked"
    }
    threats_collection.insert_one(threat)

    # Send Email Alert
    send_email_alert(
        "🚨 Cybersecurity Threat Detected!",
        f"Threat Type: {threat['attack_type']} detected from {threat['source_ip']}. Immediate action required!",
        "admin@example.com"
    )

    return jsonify({"message": "Threat detected & alerts sent!"})

@app.route('/get-threats', methods=['GET'])
def get_threats():
    """Retrieve detected threats from the database."""
    threats = list(threats_collection.find({}, {"_id": 0}))
    return jsonify(threats)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
