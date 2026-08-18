import os
from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please create a .env file and add your Groq API key."
    )


# --------------------------------------------------
# 2. Create Groq client
# --------------------------------------------------

client = Groq(api_key=api_key)


# --------------------------------------------------
# 3. Generate healthcare summary
# --------------------------------------------------

def generate_health_summary(
    appointment_record,
    visit_notes,
    medication_details,
    health_logs
):
    system_prompt = """
You are an AI assistant for RK Health.

Your task is to convert healthcare appointment records
into a short, clear, and patient-friendly summary.

Follow these rules:

1. Do not invent medical information.
2. Use only the information provided.
3. Do not make a diagnosis.
4. Do not change medication names, doses, or instructions.
5. Use simple language.
6. Keep the summary short and easy to understand.
7. Clearly mention important follow-up actions.
8. If information is missing, write "Not provided".
9. Do not provide independent medical advice.
10. Remind the patient to follow their healthcare professional's instructions.

Use this format:

VISIT SUMMARY:
Brief summary of the appointment.

KEY FINDINGS:
Important information from the visit.

MEDICATIONS:
Medication information exactly as provided.

FOLLOW-UP ACTIONS:
Important next steps from the records.

PATIENT NOTE:
A short and simple reminder.
"""

    user_prompt = f"""
Create a patient-friendly healthcare summary
using the following RK Health records.

APPOINTMENT RECORD:
{appointment_record}

VISIT NOTES:
{visit_notes}

MEDICATION DETAILS:
{medication_details}

HEALTH LOGS:
{health_logs}

Return the summary using the required format.
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.8,
            max_completion_tokens=2048
        )

        return response.choices[0].message.content

    except Exception as error:

        return f"Groq API Error: {error}"


# --------------------------------------------------
# 4. Main program
# --------------------------------------------------

def main():

    print("=" * 60)
    print("             RK HEALTH AI SUMMARY SYSTEM")
    print("=" * 60)

    appointment_record = """
Date: 14 August 2026
Department: General Medicine
Appointment Type: Follow-up visit
"""

    visit_notes = """
Patient reported occasional tiredness.
Doctor reviewed the previous health records.
No new symptoms were recorded during the visit.
"""

    medication_details = """
Medication information was not provided.
"""

    health_logs = """
Blood pressure: 120/80 mmHg
Temperature: 98.4 F
Patient reported improved sleep compared with the previous week.
"""

    print("\nGenerating healthcare summary...\n")

    summary = generate_health_summary(
        appointment_record,
        visit_notes,
        medication_details,
        health_logs
    )

    print(summary)

    print("\n")
    print("=" * 60)
    print("Summary generation completed.")
    print("=" * 60)


# --------------------------------------------------
# 5. Start program
# --------------------------------------------------

if __name__ == "__main__":
    main()