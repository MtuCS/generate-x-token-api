from flask import Flask, request, jsonify
import hmac, hashlib, base64, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 💡 Dùng đúng code từ ảnh 1
def generate_token(secret_key, transaction_id):
    signature = hmac.new(secret_key.encode('utf-8'),
                         transaction_id.encode('utf-8'),
                         hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')

@app.route('/generate-token', methods=['POST'])
def gen_token():
    data = request.get_json(force=True) or {}
    tx = data.get('input')

    if not tx:
        return jsonify({"error": "Missing input"}), 400

    sk = os.getenv("SECRET_KEY")
    if not sk:
        return jsonify({"error": "No SECRET_KEY"}), 500

    token = generate_token(sk, tx)
    return jsonify({"token": token.strip()})


@app.route('/', methods=['GET'])
def home():
    return "API running!", 200
