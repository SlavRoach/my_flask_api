from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCybLqD-fi3bzUVpEg0kzsM-4DKgDHCqPM"
CSE_ID = "b53bb82eba6a6485f"


@app.route("/", methods=["GET"])
def home():
    # Tento route vráti HTML stránku, ktorá je v adresári "templates"
    return render_template("index.html")  # Predpokladáme, že HTML súbor sa volá "index.html"


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    if not data or "keyword" not in data:
        return jsonify({"error": "Nebolo zadané kľúčové slovo"}), 400

    keyword = data["keyword"].strip()

    if not keyword:
        return jsonify({"error": "Nebolo zadané kľúčové slovo"}), 400

    google_api_url = (f"https://www.googleapis.com/customsearch/v1"
                      f"?key={API_KEY}&cx={CSE_ID}&q={keyword}")

    try:
        resp = requests.get(google_api_url)
        resp.raise_for_status()
        data = resp.json()

        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet"),
            })

        return jsonify(results)

    except requests.RequestException as e:
        return jsonify({
            "error": "Chyba pri volaní Google API",
            "details": str(e)
        }), 500
    except Exception as e:
        return jsonify({"error": "Neočakávaná chyba", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
