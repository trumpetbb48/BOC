from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "body_of_christ_secret_key"  # change plus tard

LYRICS_FILE = "lyrics.json"

ADMIN_PASSWORD = "jesus123"  # change ce mot de passe
CHORALE_PASSWORD = "chorale123"
# ========= Utils =========
def load_lyrics():
    if not os.path.exists(LYRICS_FILE):
        with open(LYRICS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(LYRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_lyric(lyric):
    lyrics = load_lyrics()
    lyrics.append(lyric)
    with open(LYRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(lyrics, f, indent=4, ensure_ascii=False)

def is_logged_in():
    return session.get("admin_logged_in")

def is_chorale():
    return session.get("chorale_logged_in")
# ========= Pages =========
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_page"))
        else:
            error = "Mot de passe incorrect"
    return render_template("login.html", error=error)



@app.route("/chorale-login", methods=["GET", "POST"])
def chorale_login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == CHORALE_PASSWORD:
            session["chorale_logged_in"] = True
            return redirect(url_for("chorale_page"))
        else:
            error = "Mot de passe incorrect"
    return render_template("chorale_login.html", error=error)


@app.route("/chorale")
def chorale_page():
    if not is_chorale():
        return redirect(url_for("chorale_login"))
    return render_template("lyrics_chorale.html")

@app.route("/chorale-logout")
def chorale_logout():
    session.pop("chorale_logged_in", None)
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("lyrics_page"))

@app.route("/admin")
def admin_page():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("admin_lyrics.html")

# addddddddddddddddddddddd
@app.route("/assemblee")
def assemblee_page():
    return render_template("lyrics_assemblee.html")

# @app.route("/chorale")
# def chorale_page():
#     return render_template("lyrics_chorale.html")



# ========= API =========
@app.route("/lyrics", methods=["GET"])
def get_lyrics():
    return jsonify(load_lyrics())

@app.route("/lyrics", methods=["POST"])
def add_lyric():
    if not is_logged_in():
        return "Unauthorized", 401
    data = request.get_json()
    save_lyric(data)
    return "Lyric added successfully"

# addddddddddddddddddddddddddd

@app.route("/lyrics/<category>")
def get_lyrics_by_category(category):
    lyrics = load_lyrics()
    filtered = [l for l in lyrics if l.get("category") == category]
    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)
