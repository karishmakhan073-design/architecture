from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re
import time

app = Flask(__name__)

# --------------------------------------------------
# Temporary database
# --------------------------------------------------
# For testing only.
# Later replace with Google Sheets / database.

appointments = []
medications = []
summaries = []
sms_history = []

next_appointment_id = 1
next_medication_id = 1


# --------------------------------------------------
# Validation helpers
# --------------------------------------------------

def validate_phone(phone):
    pattern = r"^\+[1-9]\d{7,14}$"
    return bool(re.match(pattern, phone))


def validate_date(date_value):

    try:
        datetime.strptime(date_value, "%Y-%m-%d")
        return True

    except (ValueError, TypeError):
        return False


# --------------------------------------------------
# Login page
# --------------------------------------------------

@app.route("/login")
def login():

    return render_template("login.html")


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Add Entry page
# --------------------------------------------------

@app.route("/add-entry")
def add_entry():

    return render_template("add_entry.html")


# --------------------------------------------------
# View Logs page
# --------------------------------------------------

@app.route("/logs")
def logs():

    return render_template("logs.html")


# --------------------------------------------------
# Prescription page
# --------------------------------------------------

@app.route("/prescription")
def prescription():

    return render_template("prescription.html")


# ==================================================
# DASHBOARD API
# ==================================================

@app.route("/api/dashboard")
def dashboard():

    completed = sum(
        1 for item in medications
        if item["status"] == "Completed"
    )

    total = len(medications)

    compliance = (
        round((completed / total) * 100)
        if total > 0
        else 0
    )

    return jsonify({

        "success": True,

        "appointments": len(appointments),

        "medications": len(medications),

        "summaries": len(summaries),

        "sms_sent": len(sms_history),

        "compliance": compliance

    })


# ==================================================
# ADD APPOINTMENT
# ==================================================

@app.route("/api/appointments", methods=["POST"])
def create_appointment():

    global next_appointment_id

    data = request.get_json(silent=True) or {}

    patient = str(
        data.get("patient", "")
    ).strip()

    doctor = str(
        data.get("doctor", "")
    ).strip()

    title = str(
        data.get("title", "")
    ).strip()

    date = str(
        data.get("date", "")
    ).strip()

    time_value = str(
        data.get("time", "")
    ).strip()

    notes = str(
        data.get("notes", "")
    ).strip()


    if not patient:

        return jsonify({
            "success": False,
            "message": "Patient name is required."
        }), 400


    if not doctor:

        return jsonify({
            "success": False,
            "message": "Doctor name is required."
        }), 400


    if not validate_date(date):

        return jsonify({
            "success": False,
            "message": "Invalid appointment date."
        }), 400


    appointment = {

        "id": next_appointment_id,

        "patient": patient,

        "doctor": doctor,

        "title": title,

        "date": date,

        "time": time_value,

        "notes": notes

    }

    appointments.append(appointment)

    next_appointment_id += 1


    return jsonify({

        "success": True,

        "message":
            "Appointment added successfully.",

        "appointment":
            appointment

    })


# ==================================================
# GET APPOINTMENTS
# ==================================================

@app.route("/api/appointments")
def get_appointments():

    return jsonify({

        "success": True,

        "appointments": appointments

    })


# ==================================================
# ADD MEDICATION
# ==================================================

@app.route("/api/medications", methods=["POST"])
def create_medication():

    global next_medication_id

    data = request.get_json(silent=True) or {}

    patient = str(
        data.get("patient", "")
    ).strip()

    medicine = str(
        data.get("medicine", "")
    ).strip()

    dosage = str(
        data.get("dosage", "")
    ).strip()

    timing = str(
        data.get("timing", "")
    ).strip()

    phone = str(
        data.get("phone", "")
    ).strip()


    if not patient:

        return jsonify({
            "success": False,
            "message": "Patient name is required."
        }), 400


    if not medicine:

        return jsonify({
            "success": False,
            "message": "Medicine name is required."
        }), 400


    if not dosage:

        return jsonify({
            "success": False,
            "message": "Dosage is required."
        }), 400


    if not validate_phone(phone):

        return jsonify({
            "success": False,
            "message":
                "Invalid phone number. Use +countrycode format."
        }), 400


    medication = {

        "id": next_medication_id,

        "patient": patient,

        "medicine": medicine,

        "dosage": dosage,

        "timing": timing,

        "phone": phone,

        "status": "Pending"

    }

    medications.append(medication)

    next_medication_id += 1


    return jsonify({

        "success": True,

        "message":
            "Medication added successfully.",

        "medication":
            medication

    })


# ==================================================
# AI SUMMARY
# ==================================================

@app.route("/api/summary", methods=["POST"])
def generate_summary():

    data = request.get_json(silent=True) or {}

    appointment_id = data.get(
        "appointment_id"
    )


    appointment = next(
        (
            item for item in appointments
            if item["id"] == appointment_id
        ),
        None
    )


    if appointment is None:

        return jsonify({

            "success": False,

            "message":
                "Appointment not found."

        }), 404


    # Demo AI summary.
    # Replace with Groq API call later.

    summary = (

        f"Patient {appointment['patient']} "
        f"attended a {appointment['title']} "
        f"appointment with {appointment['doctor']}. "

        f"Visit notes: "
        f"{appointment['notes'] or 'No notes provided.'} "

        "The patient should follow the "
        "healthcare professional's instructions "
        "and attend recommended follow-up visits."

    )


    summary_record = {

        "appointment_id":
            appointment_id,

        "summary":
            summary,

        "created_at":
            datetime.now().isoformat()

    }


    summaries.append(summary_record)


    return jsonify({

        "success": True,

        "message":
            "AI summary generated successfully.",

        "summary":
            summary

    })


# ==================================================
# SEND SMS
# ==================================================

@app.route("/api/send-sms", methods=["POST"])
def send_sms():

    data = request.get_json(silent=True) or {}

    phone = str(
        data.get("phone", "")
    ).strip()

    message = str(
        data.get("message", "")
    ).strip()


    if not validate_phone(phone):

        return jsonify({

            "success": False,

            "message":
                "Invalid phone number."

        }), 400


    if not message:

        return jsonify({

            "success": False,

            "message":
                "Message cannot be empty."

        }), 400


    sms_record = {

        "phone": phone,

        "message": message,

        "status": "Demo Sent",

        "time":
            datetime.now().isoformat()

    }


    sms_history.append(
        sms_record
    )


    return jsonify({

        "success": True,

        "message":
            "SMS reminder processed.",

        "status":
            "Demo Sent"

    })


# ==================================================
# HEALTH REPORT
# ==================================================

@app.route("/api/report")
def health_report():

    return jsonify({

        "success": True,

        "appointments":
            appointments,

        "medications":
            medications,

        "summaries":
            summaries,

        "sms_history":
            sms_history,

        "generated_at":
            datetime.now().isoformat()

    })


# ==================================================
# CALENDAR LINK
# ==================================================

@app.route("/api/calendar")
def calendar():

    if not appointments:

        return jsonify({

            "success": False,

            "message":
                "No appointment available."

        }), 404


    appointment = appointments[-1]


    title = appointment["title"]

    date = appointment["date"]

    time_value = appointment["time"]


    calendar_url = (
        "https://calendar.google.com/calendar/"
        "render?action=TEMPLATE"
        f"&text={title.replace(' ', '+')}"
        f"&dates={date.replace('-', '')}"
        f"T{time_value.replace(':', '')}00/"
        f"{date.replace('-', '')}"
        f"T{time_value.replace(':', '')}00"
    )


    return jsonify({

        "success": True,

        "calendar_url":
            calendar_url

    })


# ==================================================
# SYSTEM HEALTH CHECK
# ==================================================

@app.route("/api/health")
def health_check():

    start = time.time()

    # Basic application check

    response_time = round(
        (time.time() - start) * 1000,
        2
    )


    return jsonify({

        "success": True,

        "application":
            "RK Health",

        "status":
            "Running",

        "response_time_ms":
            response_time,

        "timestamp":
            datetime.now().isoformat()

    })


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    print("=" * 55)

    print("RK HEALTH APPLICATION")

    print("=" * 55)

    print(
        "Website: http://127.0.0.1:5000"
    )

    print(
        "Health Check: "
        "http://127.0.0.1:5000/api/health"
    )

    print("=" * 55)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )