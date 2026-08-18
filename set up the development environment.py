import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =====================================================
# CHECK API KEY
# =====================================================

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


# =====================================================
# CREATE GROQ CLIENT
# =====================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =====================================================
# CREATE FLASK APPLICATION
# =====================================================

app = Flask(__name__)


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# GENERATE AI RESPONSE
# =====================================================

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        user_prompt = data.get(
            "prompt",
            ""
        ).strip()


        if not user_prompt:

            return jsonify({
                "success": False,
                "error": "Prompt cannot be empty."
            }), 400


        # ---------------------------------------------
        # Groq API request
        # ---------------------------------------------

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Generate clear, useful and concise "
                        "responses based only on the user's "
                        "request."
                    )
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.7,

            max_tokens=1000
        )


        # ---------------------------------------------
        # Extract AI response
        # ---------------------------------------------

        result = (
            response
            .choices[0]
            .message
            .content
        )


        return jsonify({

            "success": True,

            "response": result.strip()
        })


    except Exception as error:

        print(
            "Groq API Error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                "Unable to generate AI response."
        }), 500


# =====================================================
# HEALTH CHECK
# =====================================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "success": True,

        "message":
            "CaptionAI Flask application is running."
    })


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("          CAPTIONAI APPLICATION")
    print("=" * 50)
    print(
        "Open: http://127.0.0.1:5000"
    )
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )