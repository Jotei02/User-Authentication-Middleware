from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Secret key for JWT encoding and decoding
app.config['SECRET_KEY'] = 'your_secret_key'

# Mock user data (in a real application, this would come from a database)
users = {
    "user1": "password1",
    "user2": "password2"
}

# Middleware function to check for JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Decode the token using the secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Route to authenticate a user and generate a token
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if users.get(auth.username) == auth.password:
        # Generate token with expiration time of 30 minutes
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

# Protected route that requires token authentication
@app.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Welcome {current_user}!'})

# Public route accessible without authentication
@app.route('/public', methods=['GET'])
def public_route():
    return jsonify({'message': 'This is a public route!'})

if __name__ == '__main__':
    app.run(debug=True)
