from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import os
import json
import logging
from openai import OpenAI

app = Flask(__name__, static_folder="static")

logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data"}), 400

        link = data.get("link")

        if not link:
            return jsonify({"error": "No link"}), 400


        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(link, headers=headers, timeout=15)

soup = BeautifulSoup(response.text, "html.parser")

content = ""

scripts = soup.find_all("script")

for script in scripts:

    if script.string and "runParams" in script.string:

        content = script.string

        break


if not content:

    content = soup.get_text(" ", strip=True)
        content = title + "\n" + body


        prompt = f"""
Return ONLY valid JSON.

Format:

{{
"score": 1,
"verdict": "WINNER",
"reason": "text"
}}

Product:

{content[:2000]}
"""


        completion = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {"role": "user", "content": prompt}
            ],

            response_format={"type": "json_object"}

        )


        result = completion.choices[0].message.content


        return jsonify({

            "analysis": json.loads(result)

        })


    except Exception as e:

        logging.exception("ERROR")

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)
