from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from profile_summariser import summarise_profile

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = summarise_profile(name)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=True)
