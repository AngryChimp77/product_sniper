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

    print("=== ANALYZE STARTED ===")

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Say TEST SUCCESS"
                }
            ],
            max_tokens=20
        )

        result = response.choices[0].message.content

        print("OPENAI RESULT:", result)

        return jsonify({
            "analysis": {
                "total": 10,
                "verdict": "WORKING",
                "reason": result
            }
        })

    except Exception as e:

        print("OPENAI ERROR:", e)

        return jsonify({
            "analysis": {
                "total": 0,
                "verdict": "ERROR",
                "reason": str(e)
            }
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

