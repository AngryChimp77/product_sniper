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

    data = request.get_json()
    link = data.get("link")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": link}
        ]
    )

    result = response.choices[0].message.content

    return jsonify({
        "score": "10",
        "verdict": "WORKING",
        "reason": result
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

