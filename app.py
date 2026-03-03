from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/improve", methods=["POST"])
def improve():
    data = request.json
    text = data.get("text", "")
    mode = data.get("mode", "improve")
    lang = data.get("lang", "Spanish")

    prompts = {
        "improve":   f"Improve this text to be clearer, more professional and engaging. Only return the improved text, nothing else:\n\n{text}",
        "grammar":   f"Fix all grammar, spelling and punctuation mistakes. Only return the corrected text, nothing else:\n\n{text}",
        "shorter":   f"Make this text shorter while keeping the core meaning. Only return the shortened text, nothing else:\n\n{text}",
        "expand":    f"Expand this text with more detail, examples and depth. Only return the expanded text, nothing else:\n\n{text}",
        "summarize": f"Summarize this text into clear bullet points of the key ideas. Only return the bullet points, nothing else:\n\n{text}",
        "translate": f"Translate this text to {lang}. Only return the translated text, nothing else:\n\n{text}",
    }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompts[mode]}]
    )
    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)