import os
from dotenv import load_dotenv
from groq import Groq
from twilio.rest import Client


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# 2. Read credentials
# --------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


# --------------------------------------------------
# 3. Check required configuration
# --------------------------------------------------

required_variables = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "TWILIO_ACCOUNT_SID": TWILIO_ACCOUNT_SID,
    "TWILIO_AUTH_TOKEN": TWILIO_AUTH_TOKEN,
    "TWILIO_PHONE_NUMBER": TWILIO_PHONE_NUMBER,
    "GOOGLE_SHEET_ID": GOOGLE_SHEET_ID,
}

missing_variables = [
    name for name, value in required_variables.items()
    if not value
]

if missing_variables:
    raise ValueError(
        "Missing configuration: "
        + ", ".join(missing_variables)
    )


# --------------------------------------------------
# 4. Initialize Groq AI client
# --------------------------------------------------

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# --------------------------------------------------
# 5. Initialize Twilio client
# --------------------------------------------------

twilio_client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)


# --------------------------------------------------
# 6. Generate healthcare summary using Groq
# --------------------------------------------------

def generate_health_summary(
    appointment_record,
    visit_notes,
    medication_details,
    health_logs
):
    prompt = f"""
Create a simple and patient-friendly healthcare summary.

Appointment:
{appointment_record}

Visit Notes:
{visit_notes}

Medication Details:
{medication_details}

Health Logs:
{health_logs}

Rules:
- Use only the information provided.
- Do not invent medical information.
- Do not diagnose the patient.
- Do not change medication names, doses, or instructions.
- Clearly mention important follow-up actions.
- Keep the summary concise and easy to understand.
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a healthcare information summarization "
                    "assistant. Summarize provided records accurately "
                    "without making medical diagnoses."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content


# --------------------------------------------------
# 7. Send SMS using Twilio
# --------------------------------------------------

def send_sms(to_phone_number, message):
    message = twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=to_phone_number
    )

    return message.sid


# --------------------------------------------------
# 8. Test the application
# --------------------------------------------------

if __name__ == "__main__":

    print("RK Health configuration loaded successfully.")

    appointment = """
    Appointment with doctor on 20 August 2026.
    """

    visit_notes = """
    Patient attended the scheduled appointment.
    Doctor advised regular follow-up.
    """

    medication = """
    Continue the medication according to the doctor's instructions.
    """

    health_logs = """
    Patient recorded the appointment and medication details.
    """

    print("\nGenerating AI summary...")

    summary = generate_health_summary(
        appointment,
        visit_notes,
        medication,
        health_logs
    )

    print("\n----- HEALTH SUMMARY -----")
    print(summary)
    print("-------------------------")