from flask import Flask, request, jsonify
import hmac, hashlib, base64, os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/generate-token', methods=['POST'])
def gen_token():
    data = request.get_json(force=True) or {}
    tx = data.get('input')
    if not tx:
        return jsonify({"error": "Missing input"}), 400

    sk = os.getenv("SECRET_KEY")
    if not sk:
        return jsonify({"error":"No SECRET_KEY"}), 500

    sig = hmac.new(sk.encode(), tx.encode(), hashlib.sha256).digest()
    token = base64.b64encode(sig).decode()
    return jsonify({"token": token})

@app.route('/', methods=['GET'])
def home():
    return "API running!", 200
