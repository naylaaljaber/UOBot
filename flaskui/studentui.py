from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

FASTAPI_QUERY_URL = "http://127.0.0.1:5001/query"
FASTAPI_LOGIN_URL = "http://127.0.0.1:5001/login"  # Endpoint to load student data

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # Send student_id to FastAPI for initialization
        response = requests.post(FASTAPI_LOGIN_URL, json={"password": password})
        if response.status_code == 200:
            session["password"] = password
            session["name"] = name
            return redirect(url_for("chat"))
        else:
            return render_template("login.html", error="Login failed. Invalid password.")

    return render_template("login.html")

@app.route("/chat")
def chat():
    if "password" not in session:
        return redirect(url_for("login"))
    return render_template("student.html", name=session["name"])

@app.route("/ask", methods=["POST"])
def ask():
    if "password" not in session:
        return jsonify({"answer": "⚠️ Please log in first."})

    user_input = request.form["message"]

    # Send query to FastAPI
    response = requests.post(FASTAPI_QUERY_URL, json={"text": user_input})
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"answer": "⚠️ Error: Failed to reach assistant."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
