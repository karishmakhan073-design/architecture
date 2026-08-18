from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

# -----------------------------------------------------
# Temporary in-memory storage
# -----------------------------------------------------
# This is for testing.
# Later you can replace this with Google Sheets.

appointments = [
    {
        "id": 1,
        "patient": "Rahul Kumar",
        "doctor": "Dr. Priya",
        "title": "General Checkup",
        "date": "2026-08-20",
        "time": "10:30",
        "notes": "Regular health checkup",
        "summary": ""
    }
]

medications = [
    {
        "id": 1,
        "patient": "Rahul Kumar",
        "medicine": "Medicine A",
        "dosage": "1 tablet",
        "timing": "Morning",
        "phone": "+919876543210",
        "status": "Pending"
    }
]

next_appointment_id = 2
next_medication_id = 2


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def validate_phone(phone):
    """
    Basic international phone number validation.
    Example:
    +919876543210
    """

    pattern = r"^\+[1-9]\d{7,14}$"

    return bool(re.match(pattern, phone))


def validate_date(date_value):
    """
    Check whether the date is valid.
    """

    try:
        datetime.strptime(
            date_value,
            "%Y-%m-%d"
        )

        return True

    except (ValueError, TypeError):

        return False


def generate_demo_summary(appointment):
    """
    Demo AI summary.

    Replace this function later with your
    Groq API integration.
    """

    patient = appointment["patient"]
    doctor = appointment["doctor"]
    title = appointment["title"]
    notes = appointment["notes"]

    summary = f"""
Visit Overview:
{patient} attended a {title} appointment with {doctor}.

Visit Notes:
{notes if notes else "No additional visit notes were provided."}

Recommendations:
The patient should follow the instructions provided by the healthcare professional.

Follow-up:
Attend the next scheduled appointment and continue following the healthcare professional's advice.

Note:
This is an AI-assisted summary and does not replace professional medical advice.
"""

    return summary.strip()


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():

    total_appointments = len(
        appointments
    )

    total_medications = len(
        medications
    )

    completed = sum(
        1
        for item in medications
        if item["status"] == "Completed"
    )

    if total_medications > 0:

        compliance = round(
            (completed / total_medications) * 100
        )

    else:

        compliance = 0

    return jsonify({

        "success": True,

        "appointments": total_appointments,

        "medications": total_medications,

        "compliance": compliance,

        "recent_activity":
            total_appointments + total_medications

    })


# =====================================================
# GET APPOINTMENTS
# =====================================================

@app.route(
    "/api/appointments",
    methods=["GET"]
)
def get_appointments():

    return jsonify({

        "success": True,

        "appointments": appointments

    })


# =====================================================
# ADD APPOINTMENT
# =====================================================

@app.route(
    "/api/appointments",
    methods=["POST"]
)
def add_appointment():

    global next_appointment_id

    data = request.get_json(
        silent=True
    ) or {}

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

    time = str(
        data.get("time", "")
    ).strip()

    notes = str(
        data.get("notes", "")
    ).strip()


    # Validation

    if not patient:

        return jsonify({
            "success": False,
            "message":
                "Patient name is required."
        }), 400


    if not doctor:

        return jsonify({
            "success": False,
            "message":
                "Doctor name is required."
        }), 400


    if not title:

        return jsonify({
            "success": False,
            "message":
                "Appointment title is required."
        }), 400


    if not validate_date(date):

        return jsonify({
            "success": False,
            "message":
                "Please enter a valid appointment date."
        }), 400


    if not time:

        return jsonify({
            "success": False,
            "message":
                "Appointment time is required."
        }), 400


    appointment = {

        "id":
            next_appointment_id,

        "patient":
            patient,

        "doctor":
            doctor,

        "title":
            title,

        "date":
            date,

        "time":
            time,

        "notes":
            notes,

        "summary":
            ""

    }


    appointments.append(
        appointment
    )

    next_appointment_id += 1


    return jsonify({

        "success": True,

        "message":
            "Appointment added successfully.",

        "appointment":
            appointment

    })


# =====================================================
# GET MEDICATIONS
# =====================================================

@app.route(
    "/api/medications",
    methods=["GET"]
)
def get_medications():

    return jsonify({

        "success": True,

        "medications":
            medications

    })


# =====================================================
# ADD MEDICATION
# =====================================================

@app.route(
    "/api/medications",
    methods=["POST"]
)
def add_medication():

    global next_medication_id

    data = request.get_json(
        silent=True
    ) or {}

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
            "message":
                "Patient name is required."
        }), 400


    if not medicine:

        return jsonify({
            "success": False,
            "message":
                "Medicine name is required."
        }), 400


    if not dosage:

        return jsonify({
            "success": False,
            "message":
                "Dosage is required."
        }), 400


    if not timing:

        return jsonify({
            "success": False,
            "message":
                "Medication timing is required."
        }), 400


    if not validate_phone(phone):

        return jsonify({
            "success": False,
            "message":
                "Enter a valid phone number such as +919876543210."
        }), 400


    medication = {

        "id":
            next_medication_id,

        "patient":
            patient,

        "medicine":
            medicine,

        "dosage":
            dosage,

        "timing":
            timing,

        "phone":
            phone,

        "status":
            "Pending"

    }


    medications.append(
        medication
    )

    next_medication_id += 1


    return jsonify({

        "success": True,

        "message":
            "Medication reminder added successfully.",

        "medication":
            medication

    })


# =====================================================
# GENERATE AI SUMMARY
# =====================================================

@app.route(
    "/api/summary",
    methods=["POST"]
)
def generate_summary():

    data = request.get_json(
        silent=True
    ) or {}

    appointment_id = data.get(
        "appointment_id"
    )


    try:

        appointment_id = int(
            appointment_id
        )

    except (
        ValueError,
        TypeError
    ):

        return jsonify({
            "success": False,
            "message":
                "Invalid appointment ID."
        }), 400


    appointment = next(
        (
            item
            for item in appointments
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


    summary = generate_demo_summary(
        appointment
    )


    appointment["summary"] = summary


    return jsonify({

        "success": True,

        "message":
            "AI summary generated successfully.",

        "summary":
            summary

    })


# =====================================================
# SEND SMS
# =====================================================

@app.route(
    "/api/send-sms",
    methods=["POST"]
)
def send_sms():

    data = request.get_json(
        silent=True
    ) or {}

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
                "SMS message cannot be empty."
        }), 400


    # Demo response.
    # Real Twilio code can be connected here.

    return jsonify({

        "success": True,

        "message":
            "SMS reminder request processed.",

        "phone":
            phone,

        "status":
            "Demo SMS sent"

    })


# =====================================================
# GENERATE REPORT
# =====================================================

@app.route(
    "/api/report",
    methods=["GET"]
)
def generate_report():

    completed = sum(
        1
        for item in medications
        if item["status"] == "Completed"
    )

    total = len(
        medications
    )

    compliance = (
        round(
            completed / total * 100
        )
        if total
        else 0
    )


    summaries = [

        {
            "appointment_id":
                item["id"],

            "summary":
                item["summary"]

        }

        for item in appointments

        if item["summary"]

    ]


    return jsonify({

        "success": True,

        "appointments":
            appointments,

        "medications":
            medications,

        "summaries":
            summaries,

        "compliance":
            compliance

    })


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    print("=" * 55)

    print(
        "RK HEALTH - Flask Application"
    )

    print("=" * 55)

    print(
        "Open: http://127.0.0.1:5000"
    )

    print("=" * 55)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )