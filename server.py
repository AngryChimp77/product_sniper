import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pytrends.request import TrendReq
from openai import OpenAI

# =========================
# CONFIG
# =========================

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=OPENAI_API_KEY)



# =========================
# INIT
# =========================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")


pytrends = TrendReq(hl="en-US", tz=360)


# =========================
# HELPERS
# =========================

def get_google_trends(keyword: str) -> int:
    try:
        pytrends.build_payload([keyword], timeframe="today 12-m")
        data = pytrends.interest_over_time()

        if data.empty:
            return 0

        return int(data[keyword].mean())

    except Exception:
        return 0


def ai_analyze(context: str) -> dict:

    prompt = f"""
You are a conservative ecommerce analyst.

Score 0–2:

Demand
Pain
Visual
Margin
Competition

Return JSON:

{{
  "demand": 0,
  "pain": 0,
  "visual": 0,
  "margin": 0,
  "competition": 0,
  "total": 0,
  "verdict": "KILL/TEST/SCALE",
  "reason": "Short explanation"
}}

Data:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        raw = response.choices[0].message.content

        return json.loads(raw)

    except Exception as e:
        return {
            "error": str(e)
        }



# =========================
# API
# =========================

@app.get("/analyze")
def analyze(link: str):

    keyword = (
        link.split("/")[-1]
        .replace("-", " ")
        .replace("_", " ")
        [:40]
    )

    trends = get_google_trends(keyword)

    context = f"""
Product: {link}
Keyword: {keyword}
Trends: {trends}/100
"""

    result = ai_analyze(context)

    return {
        "link": link,
        "keyword": keyword,
        "google_trends": trends,
        "analysis": result
    }
