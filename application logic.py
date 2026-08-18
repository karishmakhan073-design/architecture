import os
import re
import json
from datetime import datetime

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# Optional integrations
try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from the .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)


# =========================================================
# GOOGLE SHEETS CONFIGURATION
# =========================================================

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_CREDENTIALS_FILE",
    "credentials.json"
)

HEADERS = [
    "ID",
    "Patient Name",
    "Doctor Name",
    "Appointment Date",
    "Appointment Time",
    "Appointment Details",
    "Medication Information",
    "Phone Number",
    "Visit Notes",
    "Reminder Status",
    "AI Summary",
    "Calendar Link",
    "Created At",
    "Updated At"
]


def get_sheet():
    """
    Connect to Google Sheets.
    """

    if not gspread or not Credentials:
        raise RuntimeError(
            "Google Sheets packages are not installed."
        )

    if not SHEET_ID:
        raise RuntimeError(
            "GOOGLE_SHEET_ID is missing from .env"
        )

    if not os.path.exists(GOOGLE_CREDENTIALS_FILE):
        raise RuntimeError(
            f"{GOOGLE_CREDENTIALS_FILE} was not found."
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(SHEET_ID)

    worksheet = spreadsheet.sheet1

    # Create headers if sheet is empty
    if not worksheet.row_values(1):
        worksheet.append_row(HEADERS)

    return worksheet


# =========================================================
# VALIDATION HELPERS
# =========================================================

def validate_patient_name(name):
    if not name:
        return False, "Patient name is required."

    name = str(name).strip()

    if len(name) < 2:
        return False, "Patient name is too short."

    if not re.match(r"^[A-Za-z .'-]+$", name):
        return False, "Patient name contains invalid characters."

    return True, ""


def validate_date(date_string):
    if not date_string:
        return False, "Appointment date is required."

    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True, ""
    except ValueError:
        return False, "Appointment date must use YYYY-MM-DD format."


def validate_time(time_string):
    if not time_string:
        return False, "Appointment time is required."

    try:
        datetime.strptime(time_string, "%H:%M")
        return True, ""
    except ValueError:
        return False, "Appointment time must use HH:MM format."


def validate_phone(phone):
    if not phone:
        return False, "Phone number is required."

    phone = str(phone).strip()

    # Accepts international numbers such as +919876543210
    if not re.match(r"^\+?[1-9]\d{9,14}$", phone):
        return False, "Invalid phone number format."

    return True, ""


def validate_medication(medication):
    if not medication:
        return False, "Medication information is required."

    if len(str(medication).strip()) < 2:
        return False, "Medication information is incomplete."

    return True, ""


def validate_data(data):
    """
    Validate all important healthcare fields.
    """

    checks = [
        validate_patient_name(
            data.get("patient_name")
        ),
        validate_date(
            data.get("appointment_date")
        ),
        validate_time(
            data.get("appointment_time")
        ),
        validate_phone(
            data.get("phone_number")
        ),
        validate_medication(
            data.get("medication_information")
        )
    ]

    for valid, message in checks:
        if not valid:
            return False, message

    return True, ""


# =========================================================
# FORMATTING HELPERS
# =========================================================

def format_appointment(data):
    return (
        f"{data.get('appointment_date')} "
        f"at {data.get('appointment_time')}"
    )


def format_medication(medication):
    return str(medication).strip()


def create_id():
    return datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )


def current_timestamp():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =========================================================
# AI SUMMARY
# =========================================================

def generate_ai_summary(data):
    """
    Generate a patient-friendly summary using Groq.
    """

    prompt = f"""
Patient Name:
{data.get('patient_name')}

Doctor Name:
{data.get('doctor_name', '')}

Appointment:
{format_appointment(data)}

Appointment Details:
{data.get('appointment_details', '')}

Medication Information:
{data.get('medication_information', '')}

Visit Notes:
{data.get('visit_notes', '')}
"""

    system_prompt = """
You are an AI assistant for RK Health.

Create a simple and patient-friendly healthcare visit summary.

Rules:
1. Use only the information provided.
2. Do not invent medical information.
3. Do not diagnose the patient.
4. Do not change medication names, doses, or instructions.
5. Do not add medical facts that are not provided.
6. Clearly mention follow-up actions when they are provided.
7. Keep the response concise.

Use this structure:

Patient Summary:
Appointment:
Doctor:
Medications:
Visit Notes:
Follow-up Actions:
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()


# =========================================================
# GOOGLE CALENDAR LINK
# =========================================================

def generate_calendar_link(data):
    """
    Generate a Google Calendar event URL.
    """

    import urllib.parse

    date = data.get("appointment_date")
    time = data.get("appointment_time")

    title = (
        f"RK Health Appointment - "
        f"{data.get('patient_name')}"
    )

    details = data.get(
        "appointment_details",
        ""
    )

    start = f"{date}T{time}:00"

    try:
        from datetime import datetime, timedelta

        start_dt = datetime.strptime(
            start,
            "%Y-%m-%dT%H:%M:%S"
        )

        end_dt = start_dt + timedelta(minutes=30)

        start_string = start_dt.strftime(
            "%Y%m%dT%H%M%S"
        )

        end_string = end_dt.strftime(
            "%Y%m%dT%H%M%S"
        )

        params = {
            "action": "TEMPLATE",
            "text": title,
            "dates": (
                f"{start_string}/{end_string}"
            ),
            "details": details
        }

        return (
            "https://calendar.google.com/calendar/render?"
            + urllib.parse.urlencode(params)
        )

    except ValueError:
        return ""


# =========================================================
# TWILIO SMS
# =========================================================

def send_sms(phone_number, message):
    """
    Send SMS using Twilio.
    """

    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

    if not account_sid:
        return {
            "success": False,
            "status": "Twilio not configured"
        }

    if not TwilioClient:
        return {
            "success": False,
            "status": "Twilio package not installed"
        }

    try:
        client = TwilioClient(
            account_sid,
            auth_token
        )

        sms = client.messages.create(
            body=message,
            from_=twilio_number,
            to=phone_number
        )

        return {
            "success": True,
            "status": "SMS sent",
            "message_sid": sms.sid
        }

    except Exception as error:
        return {
            "success": False,
            "status": str(error)
        }


# =========================================================
# ADD LOG
# =========================================================

def add_log(data):
    """
    Store a healthcare record in Google Sheets.
    """

    valid, message = validate_data(data)

    if not valid:
        return {
            "success": False,
            "status": message
        }

    record_id = create_id()
    timestamp = current_timestamp()

    summary = ""

    calendar_link = generate_calendar_link(data)

    row = [
        record_id,
        data.get("patient_name"),
        data.get("doctor_name", ""),
        data.get("appointment_date"),
        data.get("appointment_time"),
        data.get("appointment_details", ""),
        format_medication(
            data.get("medication_information")
        ),
        data.get("phone_number"),
        data.get("visit_notes", ""),
        "Pending",
        summary,
        calendar_link,
        timestamp,
        timestamp
    ]

    sheet = get_sheet()
    sheet.append_row(row)

    return {
        "success": True,
        "status": "Record added successfully",
        "id": record_id,
        "calendar_link": calendar_link
    }


# =========================================================
# GET LOGS
# =========================================================

def get_logs():
    """
    Retrieve all healthcare records.
    """

    sheet = get_sheet()

    records = sheet.get_all_records()

    return {
        "success": True,
        "appointments": records
    }


# =========================================================
# FIND RECORD
# =========================================================

def find_record(record_id):
    sheet = get_sheet()

    records = sheet.get_all_records()

    for index, record in enumerate(records, start=2):
        if str(record.get("ID")) == str(record_id):
            return sheet, index, record

    return None, None, None


# =========================================================
# UPDATE LOG
# =========================================================

def update_log(data):
    record_id = data.get("id")

    if not record_id:
        return {
            "success": False,
            "status": "Record ID is required."
        }

    sheet, row_number, old_record = find_record(
        record_id
    )

    if not old_record:
        return {
            "success": False,
            "status": "Record not found."
        }

    patient_name = data.get(
        "patient_name",
        old_record.get("Patient Name")
    )

    appointment_date = data.get(
        "appointment_date",
        old_record.get("Appointment Date")
    )

    appointment_time = data.get(
        "appointment_time",
        old_record.get("Appointment Time")
    )

    medication = data.get(
        "medication_information",
        old_record.get("Medication Information")
    )

    valid, message = validate_patient_name(
        patient_name
    )

    if not valid:
        return {
            "success": False,
            "status": message
        }

    valid, message = validate_date(
        appointment_date
    )

    if not valid:
        return {
            "success": False,
            "status": message
        }

    valid, message = validate_time(
        appointment_time
    )

    if not valid:
        return {
            "success": False,
            "status": message
        }

    valid, message = validate_medication(
        medication
    )

    if not valid:
        return {
            "success": False,
            "status": message
        }

    updated = [
        record_id,
        patient_name,
        data.get(
            "doctor_name",
            old_record.get("Doctor Name")
        ),
        appointment_date,
        appointment_time,
        data.get(
            "appointment_details",
            old_record.get("Appointment Details")
        ),
        medication,
        data.get(
            "phone_number",
            old_record.get("Phone Number")
        ),
        data.get(
            "visit_notes",
            old_record.get("Visit Notes")
        ),
        old_record.get(
            "Reminder Status",
            "Pending"
        ),
        old_record.get(
            "AI Summary",
            ""
        ),
        generate_calendar_link(data),
        old_record.get(
            "Created At",
            current_timestamp()
        ),
        current_timestamp()
    ]

    sheet.update(
        f"A{row_number}:N{row_number}",
        [updated]
    )

    return {
        "success": True,
        "status": "Record updated successfully"
    }


# =========================================================
# DELETE LOG
# =========================================================

def delete_log(record_id):
    if not record_id:
        return {
            "success": False,
            "status": "Record ID is required."
        }

    sheet, row_number, record = find_record(
        record_id
    )

    if not record:
        return {
            "success": False,
            "status": "Record not found."
        }

    sheet.delete_rows(row_number)

    return {
        "success": True,
        "status": "Record deleted successfully"
    }


# =========================================================
# DASHBOARD STATISTICS
# =========================================================

def get_stats():
    sheet = get_sheet()

    records = sheet.get_all_records()

    total = len(records)

    pending = 0
    completed = 0

    for record in records:

        status = str(
            record.get("Reminder Status", "")
        ).lower()

        if status == "pending":
            pending += 1

        elif status == "completed":
            completed += 1

    return {
        "success": True,
        "statistics": {
            "total_records": total,
            "pending_reminders": pending,
            "completed_reminders": completed
        }
    }


# =========================================================
# GENERATE AND STORE SUMMARY
# =========================================================

def generate_summary(record_id):
    sheet, row_number, record = find_record(
        record_id
    )

    if not record:
        return {
            "success": False,
            "status": "Record not found."
        }

    data = {
        "patient_name": record.get(
            "Patient Name"
        ),
        "doctor_name": record.get(
            "Doctor Name"
        ),
        "appointment_date": record.get(
            "Appointment Date"
        ),
        "appointment_time": record.get(
            "Appointment Time"
        ),
        "appointment_details": record.get(
            "Appointment Details"
        ),
        "medication_information": record.get(
            "Medication Information"
        ),
        "visit_notes": record.get(
            "Visit Notes"
        )
    }

    summary = generate_ai_summary(data)

    # AI Summary column = K
    sheet.update_cell(
        row_number,
        11,
        summary
    )

    # Updated timestamp
    sheet.update_cell(
        row_number,
        14,
        current_timestamp()
    )

    return {
        "success": True,
        "summary": summary
    }


# =========================================================
# RUN ONCE
# =========================================================

def run_once():
    """
    Execute scheduled operations.

    This example checks pending reminders.
    """

    sheet = get_sheet()

    records = sheet.get_all_records()

    processed = 0

    for index, record in enumerate(
        records,
        start=2
    ):

        status = str(
            record.get(
                "Reminder Status",
                ""
            )
        ).lower()

        if status != "pending":
            continue

        phone = record.get(
            "Phone Number"
        )

        patient = record.get(
            "Patient Name"
        )

        appointment = record.get(
            "Appointment Date"
        )

        if phone and appointment:

            message = (
                f"RK Health Reminder: "
                f"{patient}, you have an appointment "
                f"on {appointment}."
            )

            result = send_sms(
                phone,
                message
            )

            if result["success"]:
                # Reminder Status column = J
                sheet.update_cell(
                    index,
                    10,
                    "Sent"
                )

            processed += 1

    return {
        "success": True,
        "status": "Scheduled operation completed",
        "processed": processed
    }


# =========================================================
# API ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "application": "RK Health",
        "message": "RK Health backend is running."
    })


# =========================================================
# MAIN REQUEST HANDLER
# =========================================================

@app.route("/api", methods=["GET", "POST"])
def api_handler():

    try:

        # GET parameters
        if request.method == "GET":
            action = request.args.get("action")
            data = request.args.to_dict()

        # POST JSON data
        else:
            data = request.get_json(
                silent=True
            ) or {}

            action = data.get("action")

        # -------------------------------------------------
        # ADD
        # -------------------------------------------------

        if action == "addLog":
            return jsonify(
                add_log(data)
            )

        # -------------------------------------------------
        # GET
        # -------------------------------------------------

        elif action == "getLogs":
            return jsonify(
                get_logs()
            )

        # -------------------------------------------------
        # UPDATE
        # -------------------------------------------------

        elif action == "updateLog":
            return jsonify(
                update_log(data)
            )

        # -------------------------------------------------
        # DELETE
        # -------------------------------------------------

        elif action == "deleteLog":

            record_id = data.get("id")

            return jsonify(
                delete_log(record_id)
            )

        # -------------------------------------------------
        # STATISTICS
        # -------------------------------------------------

        elif action == "getStats":
            return jsonify(
                get_stats()
            )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        elif action == "generateSummary":

            record_id = data.get("id")

            return jsonify(
                generate_summary(record_id)
            )

        # -------------------------------------------------
        # SMS
        # -------------------------------------------------

        elif action == "sendSMS":

            result = send_sms(
                data.get("phone_number"),
                data.get("message")
            )

            return jsonify(result)

        # -------------------------------------------------
        # SCHEDULED OPERATION
        # -------------------------------------------------

        elif action == "runOnce":
            return jsonify(
                run_once()
            )

        # -------------------------------------------------
        # INVALID ACTION
        # -------------------------------------------------

        else:

            return jsonify({
                "success": False,
                "status": "Invalid action."
            }), 400

    except Exception as error:

        return jsonify({
            "success": False,
            "status": "Server error",
            "error": str(error)
        }), 500


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print("-----------------------------------------")
    print("       RK HEALTH BACKEND")
    print("-----------------------------------------")
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("-----------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )