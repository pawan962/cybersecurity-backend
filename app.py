import os
import smtplib
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# ✅ Escape special characters in MongoDB credentials
USERNAME = urllib.parse.quote_plus("your_username")  # Replace with your MongoDB username
PASSWORD = urllib.parse.quote_plus("your_password")  # Replace with your MongoDB password

# ✅ MongoDB Connection
MONGO_URI = f"mongodb+srv://{pawan962}:{Pawan0509}@cluster0.2ulqp.mongodb.net/cybersecurity_db?retryWrites=true&w=majority&tls=true"
client = MongoClient(MONGO_URI)
db = client["cybersecurity_db"]
threats_collection = db["threat_logs"]

# ✅ Email Configuration (Modify this)
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
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port
    app.run(debug=True, host="0.0.0.0", port=port)
