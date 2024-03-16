from flask import Flask, request, jsonify, session

app =  Flask(__name__)
app.secret_key = "super secret key"

USERNAME = "admin"
PASSWORD = "password"


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


# Decorador para verificar la autenticación

def requires_auth(view):
    def wrapper_view(*args, **kwargs):
        if 'username' not in session or not check_auth(session['username'], session['password']):
            return jsonify({"message": "Unauthorized"}), 401
        return view(*args, **kwargs)
    return wrapper_view

@app.route("/login", methods=["POST"])
def login():
    username =  request.json.get('username')
    password =  request.json.get('password')

    if check_auth(username, password):
        session['username'] = username
        session['password'] = password
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Unauthorized"}), 401


@app.route("/secure", methods=["GET"])
@requires_auth
def secure_endpoint():
    return jsonify({"message": "Secure content"})


@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return jsonify({"message": "Logout successful"})


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello World"})

@app.route("/saludo/<nombre>", methods=["GET"])
def saludo(nombre):
    return jsonify({"message": f"Hello {nombre}"})

