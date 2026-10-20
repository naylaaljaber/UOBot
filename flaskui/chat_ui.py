from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    user_input = data.get("message", "")
    
    try:
        res = requests.post("http://127.0.0.1:5001/query", json={"text": user_input})
        bot_response = res.json().get("answer", "⚠️ No response from server.")
    except Exception as e:
        bot_response = f"⚠️ Error: {str(e)}"
    
    return jsonify({"answer": bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=8001)
