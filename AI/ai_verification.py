from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/api/verify", methods=["POST"])
def verify_image_text():
    data = request.get_json()
    image_url = data.get("imageUrl", "")
    text = data.get("text", "")

    if not image_url or not text:
        return jsonify({"error": "Both imageUrl and text required"}), 400

    # Generate fake but realistic confidence values
    keywords = ["donation", "education", "relief", "ngo", "charity", "help"]
    confidence = 50 + random.randint(-10, 10)
    for kw in keywords:
        if kw in text.lower():
            confidence += 5
    if "fake" in image_url or "broken" in image_url:
        confidence -= random.randint(20, 40)

    confidence = max(0, min(100, confidence))

    return jsonify({
        "confidence": confidence,
        "details": {
            "model": "Simulated ImpactEcho Verifier",
            "image_url": image_url,
            "text": text,
            "notes": "Confidence generated heuristically"
        }
    }), 200


if __name__ == "__main__":
    print("✅ Simulated AI Verification running on http://localhost:8003")
    app.run(host="0.0.0.0", port=8003)
