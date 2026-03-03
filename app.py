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

    prompts = {
        "improve": f"Improve this text to make it clearer and more professional:\n\n{text}",
        "grammar": f"Fix all grammar mistakes in this text:\n\n{text}",
        "shorter": f"Make this text shorter while keeping the main meaning:\n\n{text}"
    }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompts[mode]}]
    )
    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)