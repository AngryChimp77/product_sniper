import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI


app = Flask(__name__, static_folder="static")


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


@app.route("/")
def home():
    return send_from_directory("static", "index.html")



@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        print("=== ANALYZE CALLED ===")

        data = request.get_json()
        link = data.get("link")

        print("LINK:", link)


        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(link, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")


        print("CONTENT LENGTH:", len(content))

title = ""

if soup.title and soup.title.string:
    title = soup.title.string
else:
    title = "No title"


text = soup.get_text()

if not text:
    text = "No description"

text = text[:3000]


content = title + "\n" + text

        ai = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"""
Analyze this product and respond EXACTLY in this format:

Score: X/10
Verdict: Winner or Average or Loser
Reason: short explanation

Product:
{content}
"""
            }],
            max_tokens=200
        )


        result = ai.choices[0].message.content

        print("AI RESULT:", result)


        return jsonify({
            "result": result
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "result": "Error: " + str(e)
        })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )

