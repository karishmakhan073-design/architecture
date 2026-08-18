import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

app = Flask(__name__)

DATABASE = "rk_health.db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to the .env file."
    )

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# DATABASE
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_db()

    cursor = connection.cursor()

    # -----------------------------------------
    # Appointments table
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_name TEXT NOT NULL,

            doctor_name TEXT NOT NULL,

            appointment_title TEXT NOT NULL,

            appointment_date TEXT NOT NULL,

            appointment_time TEXT NOT NULL,

            visit_notes TEXT,

            created_at TEXT NOT NULL
        )
    """)


    # -----------------------------------------
    # Medications table
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_name TEXT NOT NULL,

            medicine_name TEXT NOT NULL,

            dosage TEXT NOT NULL,

            timing TEXT NOT NULL,

            phone_number TEXT NOT NULL,

            reminder_status TEXT DEFAULT 'Pending',

            created_at TEXT NOT NULL
        )
    """)


    # -----------------------------------------
    # AI summaries table
    # -----------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            appointment_id INTEGER NOT NULL,

            summary TEXT NOT NULL,

            created_at TEXT NOT NULL
        )
    """)


    connection.commit()

    connection.close()


# =========================================================
# VALIDATION
# =========================================================

def validate_required(value, field_name):

    if not value or not str(value).strip():

        return False, (
            f"{field_name} is required."
        )

    return True, ""


def validate_date(date_value):

    try:

        datetime.strptime(
            date_value,
            "%Y-%m-%d"
        )

        return True, ""

    except ValueError:

        return False, (
            "Date must be in YYYY-MM-DD format."
        )


def validate_time(time_value):

    try:

        datetime.strptime(
            time_value,
            "%H:%M"
        )

        return True, ""

    except ValueError:

        return False, (
            "Time must be in HH:MM format."
        )


def validate_phone(phone):

    phone = str(phone).strip()

    if not phone.startswith("+"):

        return False, (
            "Phone number should include country code."
        )

    digits = phone[1:]

    if not digits.isdigit():

        return False, (
            "Phone number contains invalid characters."
        )

    if len(digits) < 10 or len(digits) > 15:

        return False, (
            "Invalid phone number length."
        )

    return True, ""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# ADD APPOINTMENT
# =========================================================

@app.route(
    "/api/appointments",
    methods=["POST"]
)
def add_appointment():

    data = request.get_json(
        silent=True
    ) or {}


    fields = [
        ("patient_name", "Patient name"),
        ("doctor_name", "Doctor name"),
        ("appointment_title", "Appointment title"),
        ("appointment_date", "Appointment date"),
        ("appointment_time", "Appointment time")
    ]


    for field, name in fields:

        valid, message = validate_required(
            data.get(field),
            name
        )

        if not valid:

            return jsonify({
                "success": False,
                "message": message
            }), 400


    valid, message = validate_date(
        data["appointment_date"]
    )

    if not valid:

        return jsonify({
            "success": False,
            "message": message
        }), 400


    valid, message = validate_time(
        data["appointment_time"]
    )

    if not valid:

        return jsonify({
            "success": False,
            "message": message
        }), 400


    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO appointments (
            patient_name,
            doctor_name,
            appointment_title,
            appointment_date,
            appointment_time,
            visit_notes,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        data["patient_name"].strip(),

        data["doctor_name"].strip(),

        data["appointment_title"].strip(),

        data["appointment_date"],

        data["appointment_time"],

        data.get(
            "visit_notes",
            ""
        ).strip(),

        datetime.now().isoformat()
    ))


    appointment_id = cursor.lastrowid

    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message":
            "Appointment added successfully.",

        "appointment_id":
            appointment_id
    })


# =========================================================
# GET APPOINTMENTS
# =========================================================

@app.route(
    "/api/appointments",
    methods=["GET"]
)
def get_appointments():

    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM appointments
        ORDER BY appointment_date, appointment_time
    """)


    records = [
        dict(row)
        for row in cursor.fetchall()
    ]


    connection.close()


    return jsonify({

        "success": True,

        "appointments":
            records
    })


# =========================================================
# ADD MEDICATION
# =========================================================

@app.route(
    "/api/medications",
    methods=["POST"]
)
def add_medication():

    data = request.get_json(
        silent=True
    ) or {}


    fields = [
        ("patient_name", "Patient name"),
        ("medicine_name", "Medicine name"),
        ("dosage", "Dosage"),
        ("timing", "Medicine timing"),
        ("phone_number", "Phone number")
    ]


    for field, name in fields:

        valid, message = validate_required(
            data.get(field),
            name
        )

        if not valid:

            return jsonify({
                "success": False,
                "message": message
            }), 400


    valid, message = validate_phone(
        data["phone_number"]
    )

    if not valid:

        return jsonify({
            "success": False,
            "message": message
        }), 400


    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO medications (
            patient_name,
            medicine_name,
            dosage,
            timing,
            phone_number,
            reminder_status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        data["patient_name"].strip(),

        data["medicine_name"].strip(),

        data["dosage"].strip(),

        data["timing"].strip(),

        data["phone_number"].strip(),

        "Pending",

        datetime.now().isoformat()
    ))


    medication_id = cursor.lastrowid

    connection.commit()

    connection.close()


    return jsonify({

        "success": True,

        "message":
            "Medication reminder added.",

        "medication_id":
            medication_id
    })


# =========================================================
# GET MEDICATIONS
# =========================================================

@app.route(
    "/api/medications",
    methods=["GET"]
)
def get_medications():

    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM medications
        ORDER BY created_at DESC
    """)


    records = [
        dict(row)
        for row in cursor.fetchall()
    ]


    connection.close()


    return jsonify({

        "success": True,

        "medications":
            records
    })


# =========================================================
# AI HEALTH SUMMARY
# =========================================================

@app.route(
    "/api/summaries/<int:appointment_id>",
    methods=["POST"]
)
def generate_summary(
    appointment_id
):

    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM appointments
        WHERE id = ?
    """, (appointment_id,))


    appointment = cursor.fetchone()


    if not appointment:

        connection.close()

        return jsonify({

            "success": False,

            "message":
                "Appointment not found."
        }), 404


    # -----------------------------------------
    # Prepare AI input
    # -----------------------------------------

    prompt = f"""
Patient Name:
{appointment["patient_name"]}

Doctor:
{appointment["doctor_name"]}

Appointment:
{appointment["appointment_title"]}

Date:
{appointment["appointment_date"]}

Time:
{appointment["appointment_time"]}

Visit Notes:
{appointment["visit_notes"]}
"""


    system_prompt = """
You are the AI assistant for RK Health.

Create a short, clear and patient-friendly
health visit summary.

Include:

1. Visit Overview
2. Recommendations mentioned in the notes
3. Follow-up Guidance

Important rules:

- Use only the information supplied.
- Do not invent medical information.
- Do not diagnose the patient.
- Do not change medication instructions.
- Do not make unsupported medical recommendations.
- If information is not available, say so.
"""


    try:

        response = (
            groq_client
            .chat
            .completions
            .create(

                model=
                    "llama-3.3-70b-versatile",

                messages=[

                    {
                        "role": "system",

                        "content":
                            system_prompt
                    },

                    {
                        "role": "user",

                        "content":
                            prompt
                    }
                ],

                temperature=0.3,

                max_tokens=800
            )
        )


        summary = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        # -----------------------------------------
        # Store summary
        # -----------------------------------------

        cursor.execute("""
            INSERT INTO summaries (
                appointment_id,
                summary,
                created_at
            )

            VALUES (?, ?, ?)
        """, (

            appointment_id,

            summary,

            datetime.now().isoformat()
        ))


        connection.commit()

        connection.close()


        return jsonify({

            "success": True,

            "summary":
                summary
        })


    except Exception as error:

        connection.close()

        return jsonify({

            "success": False,

            "message":
                "AI summary generation failed.",

            "error":
                str(error)
        }), 500


# =========================================================
# HEALTH REPORT
# =========================================================

@app.route(
    "/api/report",
    methods=["GET"]
)
def generate_report():

    connection = get_db()

    cursor = connection.cursor()


    # Appointments
    cursor.execute("""
        SELECT *
        FROM appointments
        ORDER BY appointment_date DESC
    """)

    appointments = [
        dict(row)
        for row in cursor.fetchall()
    ]


    # Medications
    cursor.execute("""
        SELECT *
        FROM medications
        ORDER BY created_at DESC
    """)

    medications = [
        dict(row)
        for row in cursor.fetchall()
    ]


    # Summaries
    cursor.execute("""
        SELECT *
        FROM summaries
        ORDER BY created_at DESC
    """)

    summaries = [
        dict(row)
        for row in cursor.fetchall()
    ]


    connection.close()


    pending_reminders = sum(
        1
        for medicine in medications
        if medicine["reminder_status"]
        == "Pending"
    )


    completed_reminders = sum(
        1
        for medicine in medications
        if medicine["reminder_status"]
        == "Completed"
    )


    report = {

        "generated_at":
            datetime.now().isoformat(),

        "appointments":
            appointments,

        "medications":
            medications,

        "summaries":
            summaries,

        "compliance": {

            "total_reminders":
                len(medications),

            "pending":
                pending_reminders,

            "completed":
                completed_reminders
        }
    }


    return jsonify({

        "success": True,

        "report":
            report
    })


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

@app.route(
    "/api/stats",
    methods=["GET"]
)
def get_stats():

    connection = get_db()

    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM appointments"
    )

    appointments = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM medications"
    )

    medications = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM summaries"
    )

    summaries = cursor.fetchone()[0]


    connection.close()


    return jsonify({

        "success": True,

        "statistics": {

            "appointments":
                appointments,

            "medications":
                medications,

            "summaries":
                summaries
        }
    })


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    initialize_database()


    print("=" * 55)
    print("              RK HEALTH")
    print("=" * 55)
    print("Healthcare Record Management System")
    print()
    print(
        "Open: http://127.0.0.1:5000"
    )
    print("=" * 55)


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )