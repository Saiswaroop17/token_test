from flask import Flask, request, jsonify
import jwt 
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisthesecretkey'

def token_required(f):
    def decorated():
        token = request.headers['Authorization']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(data)

    return decorated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message' : 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected(data):
    return jsonify(data)


@app.route('/login')
def login():
    auth = request.get_json()

    if auth['username'] == "name" and auth['password'] == 'password':
        token = jwt.encode({'user' : auth['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return jsonify(message = "Could not verify the request")


app.run(port=80)