import requests


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()
        link = data.get("link")

        print("Fetching:", link)

        page = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0"
        })

        html = page.text[:8000]


        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ecommerce product analyst. Score product 1-10 and explain briefly."
                },
                {
                    "role": "user",
                    "content": html
                }
            ],
            max_tokens=200
        )


        result = response.choices[0].message.content


        return jsonify({
            "analysis": {
                "total": 7,
                "verdict": "SCALE",
                "reason": result
            }
        })


    except Exception as e:

        return jsonify({
            "analysis": {
                "total": 0,
                "verdict": "ERROR",
                "reason": str(e)
            }
        })

