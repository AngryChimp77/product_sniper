import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder="static")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        print("=== ANALYZE CALLED ===")

        data = request.json
        link = data.get("link")

        print("LINK:", link)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(link, headers=headers, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")

        # SAFE TITLE EXTRACTION
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string

        body_text = soup.get_text(separator=" ", strip=True)

        content = (title + " " + body_text)[:4000]

        print("CONTENT LENGTH:", len(content))


        prompt = f"""
Analyze this product and score it 1-10 for dropshipping potential.

Product data:
{content}

Respond EXACTLY in this format:

Score: X/10
Verdict: Winning / Average / Bad
Reason: short explanation
"""


        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )


        result = completion.choices[0].message.content

        print("AI RESULT:", result)

        return jsonify({"result": result})


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({"result": "Invalid analysis"})


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)

