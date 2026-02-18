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

    print("REQUEST RECEIVED")

    try:

        data = request.get_json()
        link = data.get("link")

        print("LINK:", link)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this product link and return score 1-10, verdict SCALE TEST or PASS, and short reason: {link}"
                }
            ],
            max_tokens=100
        )

        result = response.choices[0].message.content

        return jsonify({
            "analysis": {
                "total": 5,
                "verdict": "TEST",
                "reason": result
            }
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "analysis": {
                "total": 0,
                "verdict": "ERROR",
                "reason": str(e)
            }
        })

if __name__ == "__main__":
    app.run()

