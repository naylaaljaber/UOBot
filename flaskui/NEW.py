from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

FASTAPI_QUERYGUEST_URL = "http://127.0.0.1:5001/queryguest"
FASTAPI_QUERY_URL = "http://127.0.0.1:5001/query"
FASTAPI_LOGIN_URL = "http://127.0.0.1:5001/login"
FASTAPI_LOGOUT_URL = "http://127.0.0.1:5001/logout"

@app.route("/")
def guest_chat():
    return render_template("chat.html")  # Guest UI

@app.route("/message", methods=["POST"])
def guest_message():
    data = request.get_json()
    user_input = data.get("message", "")
    try:
        res = requests.post(FASTAPI_QUERYGUEST_URL, json={"text": user_input})
        bot_response = res.json().get("answer", "⚠️ No response from server.")
    except Exception as e:
        bot_response = f"⚠️ Error: {str(e)}"
    return jsonify({"answer": bot_response})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # Validate student
        response = requests.post(FASTAPI_LOGIN_URL, json={"password": password})
        if response.status_code == 200:
            session["password"] = password
            session["name"] = name
            return redirect(url_for("student_chat"))
        else:
            return render_template("login.html", error="Login failed.")

    return render_template("login.html")

@app.route("/chat")
def student_chat():
    if "password" not in session:
        return redirect(url_for("login"))
    return render_template("student.html", name=session["name"])

@app.route("/ask", methods=["POST"])
def ask():
    if "password" not in session:
        return jsonify({"answer": "⚠️ Please log in first."})

    user_input = request.form["message"]
    response = requests.post(FASTAPI_QUERY_URL, json={"text": user_input})
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"answer": "⚠️ Error: Failed to reach assistant."})

@app.route("/logout", methods=["GET", "POST"])
def logout():
    requests.post(FASTAPI_LOGOUT_URL, json={"text": "logout"})
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(debug=True, port=8001)
