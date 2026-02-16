import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder="static")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    link = data.get("link")

    prompt = f"""
You are a strict dropshipping product validator.

Analyze this product link:
{link}

Respond ONLY in JSON:

{{
"total": number 1-10,
"verdict": "KILL" or "TEST",
"reason": "short explanation"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return jsonify(response.choices[0].message.content)

