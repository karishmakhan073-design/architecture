import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from .env
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


def generate_health_summary(
    appointment_record,
    visit_notes,
    medication_details,
    health_logs
):
    """
    Generate a simple, patient-friendly summary
    using the Groq Llama model.
    """

    prompt = f"""
You are an AI assistant for RK Health.

Create a clear and patient-friendly summary using ONLY
the information provided below.

IMPORTANT RULES:
1. Do not invent medical information.
2. Do not diagnose the patient.
3. Do not change medication names, doses, or instructions.
4. Do not assume information that is not provided.
5. Clearly separate confirmed information from suggestions.
6. Keep the summary concise and easy to understand.
7. Mention follow-up actions if they are explicitly available.

APPOINTMENT RECORD:
{appointment_record}

VISIT NOTES:
{visit_notes}

MEDICATION DETAILS:
{medication_details}

HEALTH LOGS:
{health_logs}

Return the result using this structure:

Patient Visit Summary
---------------------
Appointment:
Visit Notes:
Medications:
Health Information:
Follow-up Actions:
Important Notes:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You generate safe, accurate and "
                        "patient-friendly healthcare summaries."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1200
        )

        summary = response.choices[0].message.content

        if not summary:
            raise ValueError("AI returned an empty summary.")

        return summary.strip()

    except Exception as error:
        print("Error generating AI summary:", error)
        return None


if __name__ == "__main__":

    # Example RK Health data
    appointment_record = """
Doctor: Dr. Rao
Date: 18 August 2026
Appointment Type: General Consultation
"""

    visit_notes = """
Patient visited the doctor for a routine consultation.
The doctor reviewed the patient's previous health records.
"""

    medication_details = """
Paracetamol - as prescribed by the doctor.
"""

    health_logs = """
Blood pressure recorded during the visit.
Patient reported feeling better compared with the previous visit.
"""

    summary = generate_health_summary(
        appointment_record,
        visit_notes,
        medication_details,
        health_logs
    )

    if summary:
        print("\n========== RK HEALTH AI SUMMARY ==========\n")
        print(summary)
        print("\n==========================================")
    else:
        print("Unable to generate the health summary.")