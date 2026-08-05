from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Narendra's DevOps Pipeline! 🚀",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)