from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'your_secret_key'  
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    IdUser = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Token = db.Column(db.String(255))

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('userName', None)
    password = request.json.get('password', None)
    
    user = User.query.filter_by(UserName=username).first()
    if user and user.Password == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@app.route('/hello', methods=['GET'])
@jwt_required()
def hello_world():
    return jsonify(message="Hello World"), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
