from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCybLqD-fi3bzUVpEg0kzsM-4DKgDHCqPM"
CSE_ID = "b53bb82eba6a6485f"

def call_google_api(keyword):
    google_api_url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?key={API_KEY}&cx={CSE_ID}&q={keyword}"
    )
    resp = requests.get(google_api_url)
    resp.raise_for_status()
    return resp.json()

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    keyword = data.get("keyword", "").strip()

    if not keyword:
        return jsonify({"error": "Nebolo zadané kľúčové slovo"}), 400

    try:
        data = call_google_api(keyword)

        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            })

        return jsonify(results)

    except requests.RequestException as e:
        return jsonify({"error": "Chyba pri volaní Google API", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Neočakávaná chyba", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Na Renderi bude tento port automaticky priradený
    app.run(host="0.0.0.0", port=port, debug=True)
