import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder="static")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()
        link = data.get("link")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are a product research expert. "
                    "Always return ONLY valid JSON in this format: "
                    "{ total: number, verdict: 'TEST' or 'SCALE', reason: 'text' }."
                },
                {
                    "role": "user",
                    "content": f"Analyze this product link: {link}"
                }
            ],
            max_tokens=200
        )

        result = response.choices[0].message.content

        return jsonify({
            "analysis": result
        })

    except Exception as e:

        return jsonify({
            "analysis": {
                "total": 0,
                "verdict": "ERROR",
                "reason": str(e)
            }
        })

if __name__ == "__main__":
    app.run()

