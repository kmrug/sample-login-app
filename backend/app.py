from flask import Flask, jsonify, request
from mysql.connector import Error
from config import db

app = Flask(__name__)

@app.route('/')
def home():
  return 'Flask backend is running'

@app.route('/signup', methods=['POST'])
def signup():
  data = request.get_json()
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')

  try:
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    
    db.commit()
    return jsonify({'message': 'User registered successfully'}), 201
  
  except Error as e:
    return jsonify({'error':str(e)}), 400

if __name__ == '__main__':
  app.run(debug=True)