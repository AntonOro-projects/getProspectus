import distutils.util
from os import abort
from backend.database_helper import *
from flask import Flask, jsonify, request, send_from_directory
import secrets
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = "../backend/files/pdfs/"
online_users = []
initialize()


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.headers.get("username")
    password = request.headers.get("password")

    verified = verify_user_exists(username, password)
    result = {}
    if verified["success"]:
        token = secrets.token_urlsafe(32)
        online_users.append(token)
        result["token"] = token

    result["success"] = verified["success"]

    return jsonify(result)


@app.route('/thirdpartylogin', methods=['GET', 'POST'])
def third_party_login():
    token = request.headers.get("token")
    online_users.append(token)
    result = {"token": token}
    return jsonify(result)


@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.headers.get("username")
    password = request.headers.get("password")
    signed_up = sign_up_user(username, password)

    return jsonify(signed_up)


@app.route('/logout', methods=['POST'])
def logout():
    token = request.args.get("token")
    result = {}
    if token in online_users:
        result["success"] = True
        result["message"] = "You are now logged out!"
        online_users.remove(token)
    else:
        result["success"] = False
        result["message"] = "You are already logged out"
    return jsonify(result)


@app.route('/search', methods=['GET', 'POST'])
def search():
    token = request.headers.get("token")
    search_words = request.headers.get("search_words")
    exact_match = bool(distutils.util.strtobool(request.headers.get("exact_match")))

    result = []
    if token in online_users:
        result = searchDB(search_words, exact_match)
    if not result:
        result = []
    return jsonify(result)


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/pdf/<path:filename>', methods=['GET', 'POST'])
def pdf(filename):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename=filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
