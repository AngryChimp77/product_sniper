from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import os
import openai
import json
import logging

app = Flask(__name__, static_folder="static")

# Logging setup
logging.basicConfig(level=logging.INFO)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")


# Serve frontend
@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")


# Analyze endpoint
@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data or "link" not in data:
            return jsonify({"error": "No link provided"}), 400

        link = data["link"]

        logging.info(f"Received link: {link}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(link, headers=headers, timeout=15)

        if response.status_code != 200:
            logging.error("Failed to fetch page")
            return jsonify({"error": "Failed to fetch product page"}), 500

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("title")

        title = title_tag.get_text(strip=True) if title_tag else ""

        body = soup.get_text(separator=" ", strip=True)

        content = title + "\n" + body

        if not content.strip():
            return jsonify({"error": "Failed to extract product content"}), 500

        logging.info("Scraping successful")


        prompt = f"""

You are an expert dropshipping product analyst.

Analyze this product.

Return STRICT JSON only.

Product content:

{content[:4000]}

Format:

{{
"score": number from 1 to 10,
"verdict": "WINNER" or "LOSER",
"reason": "short explanation"
}}

"""

        completion = openai.ChatCompletion.create(

            model="gpt-4o-mini",

            messages=[
                {"role": "system", "content": "You are a product analyst."},
                {"role": "user", "content": prompt}
            ],

            temperature=0.3

        )

        result_text = completion.choices[0].message.content

        logging.info("OpenAI response received")

        try:

            result_json = json.loads(result_text)

        except:

            return jsonify({"error": "OpenAI returned invalid format", "raw": result_text}), 500


        return jsonify({

            "analysis": result_json

        })


    except Exception as e:

        logging.exception("Error occurred")

        return jsonify({

            "error": str(e)

        }), 500



# Render requires this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
