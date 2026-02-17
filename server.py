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
                {"role": "user", "content": link}
            ],
            max_tokens=50
        )

        print("OPENAI RESPONDED")

        result = response.choices[0].message.content

        return jsonify({
            "score": "OK",
            "verdict": "OK",
            "reason": result
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "score": "Error",
            "verdict": "Error",
            "reason": str(e)
        })

if __name__ == "__main__":
    app.run()

