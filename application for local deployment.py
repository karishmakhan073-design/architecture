import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Google Apps Script URL can be used if your
# project still uses Google Apps Script.
GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.route("/api/status", methods=["GET"])
def status():

    return jsonify({
        "success": True,
        "application": "RK Health",
        "backend": "Python Flask",
        "message": "RK Health backend is running"
    })


# --------------------------------------------------
# Frontend Configuration
# --------------------------------------------------

@app.route("/api/config", methods=["GET"])
def config():

    return jsonify({
        "success": True,

        # Safe to expose
        # because this is not a secret
        "google_script_url": GOOGLE_SCRIPT_URL or "",

        # Never send API keys or authentication
        # tokens to the browser.
        "services": {
            "groq": bool(GROQ_API_KEY),
            "twilio": bool(
                TWILIO_ACCOUNT_SID
                and TWILIO_AUTH_TOKEN
            )
        }
    })


# --------------------------------------------------
# Test API
# --------------------------------------------------

@app.route("/api/test", methods=["POST"])
def test_api():

    data = request.get_json(silent=True) or {}

    patient_name = data.get(
        "patient_name",
        ""
    ).strip()

    if not patient_name:

        return jsonify({
            "success": False,
            "message": "Patient name is required."
        }), 400

    return jsonify({
        "success": True,
        "message": "Frontend request received successfully.",
        "patient_name": patient_name
    })


# --------------------------------------------------
# Run Server
# --------------------------------------------------

if __name__ == "__main__":

    print("----------------------------------------")
    print("          RK HEALTH APPLICATION")
    print("----------------------------------------")
    print("Frontend:")
    print("http://127.0.0.1:5000")
    print("----------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )