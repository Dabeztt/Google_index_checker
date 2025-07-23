from flask import Flask, render_template, request, jsonify
from serpapi import GoogleSearch
import time
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

def is_indexed(url):
    try:
        params = {
            "engine": "google",
            "q": f"site:{url}",
            "api_key": SERP_API_KEY,
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])

        return {"indexed": len(organic_results) > 0}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_urls():
    data = request.get_json()
    urls = data.get("urls", [])
    results = []

    for url in urls:
        status = is_indexed(url)
        if "error" in status:
            return jsonify({"error": status["error"]}), 500
        results.append({
            "url": url,
            "status": "Indexed" if status["indexed"] else "Not Indexed"
        })
        time.sleep(1.2) 

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)