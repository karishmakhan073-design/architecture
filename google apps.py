import os
from dotenv import load_dotenv
from groq import Groq

# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Please add it to your .env file."
    )

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)


# --------------------------------------------------
# 2. Generate healthcare summary
# --------------------------------------------------
def generate_summary(
    patient_name,
    doctor_name,
    appointment_details,
    medication_information,
    visit_notes
):
    """
    Generate a patient-friendly healthcare summary.

    The AI must use only the information provided.
    It must not diagnose or invent medical information.
    """

    prompt = f"""
Patient Name:
{patient_name}

Doctor Name:
{doctor_name}

Appointment Details:
{appointment_details}

Medication Information:
{medication_information}

Visit Notes:
{visit_notes}
"""

    system_message = """
You are an AI assistant for RK Health, a healthcare
record-management application.

Generate a clear and simple patient-friendly summary.

Rules:
1. Use only the information provided.
2. Do not invent medical information.
3. Do not provide a diagnosis.
4. Do not change medication names, doses, or instructions.
5. Clearly separate confirmed information from suggestions.
6. Mention important follow-up actions if they are present
   in the provided information.
7. Keep the summary concise and easy to understand.

Format the response as:

Patient Summary:
Appointment:
Doctor:
Medications:
Visit Notes:
Follow-up Actions:
"""


    # --------------------------------------------------
    # 3. Send request to Groq
    # --------------------------------------------------
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    # --------------------------------------------------
    # 4. Extract generated summary
    # --------------------------------------------------
    summary = response.choices[0].message.content

    return summary.strip()


# --------------------------------------------------
# 5. Test the function
# --------------------------------------------------
if __name__ == "__main__":

    patient_name = "Rahul"
    doctor_name = "Dr. Kumar"

    appointment_details = """
Appointment Date: 20-08-2026
Appointment Time: 10:30 AM
Purpose: General consultation
"""

    medication_information = """
Paracetamol - Take as prescribed by the doctor.
"""

    visit_notes = """
Patient attended the scheduled appointment.
Doctor advised a follow-up appointment.
"""

    try:
        summary = generate_summary(
            patient_name,
            doctor_name,
            appointment_details,
            medication_information,
            visit_notes
        )

        print("\n========== RK HEALTH AI SUMMARY ==========\n")
        print(summary)
        print("\n===========================================\n")

    except Exception as error:
        print("Error generating summary:")
        print(error)