from flask import Flask, request, jsonify, render_template
import json, os

app = Flask(__name__)

LYRICS_FILE = "lyrics.json"

# ========= Utils =========
def load_lyrics():
    if not os.path.exists(LYRICS_FILE):
        with open(LYRICS_FILE, "w") as f:
            json.dump([], f)
    with open(LYRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_lyric(lyric):
    lyrics = load_lyrics()
    lyrics.append(lyric)
    with open(LYRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(lyrics, f, indent=4, ensure_ascii=False)

# ========= Pages =========
@app.route("/")
def lyrics_page():
    return render_template("lyrics.html")

@app.route("/admin")
def admin_page():
    return render_template("admin_lyrics.html")

# ========= API =========
@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    return jsonify(load_lyrics())

@app.route("/lyrics", methods=["POST"])
def add_lyric():
    data = request.get_json()
    save_lyric(data)
    return "Lyric added successfully"

if __name__ == "__main__":
    app.run(debug=True)
