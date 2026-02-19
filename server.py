import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder="static")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    print("ANALYZE CALLED")

    try:

        data = request.get_json()

        print("DATA:", data)

        link = data.get("link")

        print("LINK:", link)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this product briefly: {link}"
                }
            ],
            max_tokens=100
        )

        print("OPENAI RESPONSE:", response)

        result = response.choices[0].message.content

        return jsonify({
            "score": "10",
            "verdict": "WORKING",
            "reason": result
        })

    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "score": "0",
            "verdict": "ERROR",
            "reason": str(e)
        })

