import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI


# Flask app
app = Flask(__name__, static_folder="static")

# OpenAI client
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


# Serve frontend
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# Analyze endpoint
@app.route("/analyze", methods=["POST"])
def analyze():

    print("=== ANALYZE CALLED ===")

    try:

        data = request.get_json()

        if not data or "link" not in data:
            return jsonify({
                "score": "0",
                "verdict": "Error",
                "reason": "No link provided"
            })

        link = data["link"]

        print("LINK:", link)


        # STEP 1 — download webpage

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        }

        response = requests.get(link, headers=headers, timeout=15)

        if response.status_code != 200:
            return jsonify({
                "score": "0",
                "verdict": "Error",
                "reason": "Failed to fetch product page"
            })


        # STEP 2 — parse HTML

        soup = BeautifulSoup(response.text, "html.parser")

title = ""

if soup.title and soup.title.string:
    title = soup.title.string

body_text = soup.get_text(separator=" ", strip=True)

content = (title + " " + body_text)[:4000]


        print("CONTENT LENGTH:", len(content))



        # STEP 3 — OpenAI analysis

        prompt = f"""
You are a professional ecommerce product analyst.

Analyze this product and return:

Score: X/10
Verdict: (Bad / Average / Good / Excellent)
Reason: short explanation

Product data:
{content}
"""


        ai = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=200

        )


        result = ai.choices[0].message.content

        print("AI RESULT:", result)



        # STEP 4 — parse AI response safely

        score = "?"
        verdict = "Unknown"
        reason = result

        for line in result.split("\n"):

            if "Score:" in line:
                score = line.split("Score:")[-1].strip()

            elif "Verdict:" in line:
                verdict = line.split("Verdict:")[-1].strip()

            elif "Reason:" in line:
                reason = line.split("Reason:")[-1].strip()



        return jsonify({

            "score": score,

            "verdict": verdict,

            "reason": reason

        })



    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({

            "score": "0",

            "verdict": "Error",

            "reason": str(e)

        })



# Run locally
if __name__ == "__main__":

    app.run(debug=True)

