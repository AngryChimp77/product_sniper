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

        if not data or "link" not in data:
            return jsonify({"error": "No link provided"}), 400

        link = data["link"]

        logging.info(f"Link received: {link}")

        headers = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"

        }

        response = requests.get(link, headers=headers, timeout=15)

        if response.status_code != 200:

            return jsonify({"error": "Failed to fetch page"}), 500


        soup = BeautifulSoup(response.text, "html.parser")


        title = ""

        if soup.title and soup.title.string:

            title = soup.title.string.strip()

        body = soup.get_text(" ", strip=True)

        content = str(title) + "\n" + str(body)


        logging.info("Scraping success")


prompt = f"""

Analyze this dropshipping product.

Return your answer ONLY as valid JSON.

Use this exact JSON format:

{{
"score": number from 1 to 10,
"verdict": "WINNER" or "LOSER",
"reason": "short explanation"
}}

Product:

{content[:3000]}

"""

        completion = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {"role": "user", "content": prompt}

            ],

            response_format={"type": "json_object"}

        )


        result_json = completion.choices[0].message.content


        return jsonify({

            "analysis": json.loads(result_json)

        })


    except Exception as e:

        logging.exception("ERROR")

        return jsonify({

            "error": str(e)

        }), 500


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)
