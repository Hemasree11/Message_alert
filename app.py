from flask import Flask, request, render_template, jsonify
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send-sos", methods=["POST"])
def send_sos():
    data = request.json
    phone = data.get("phone")
    message = data.get("message", "🚨 SOS Alert: Immediate help needed!")
    try:
        msg = client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=phone
        )
        return jsonify({"status": "success", "sid": msg.sid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
