from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import Error
from config import db

app = Flask(__name__)
CORS(app)

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
  
@app.route('/user/<username>' ,methods=['GET'])
def fetchUser(username):
  
  cursor = db.cursor()
  cursor.execute("SELECT username, email, created_at from users where username = %s", (username,))

  result = cursor.fetchone()
  if result:
    username, email, created_at = result
    return jsonify({'username': username, 'email': email, 'created_at': str(created_at)}), 200
    
  else:
      return jsonify({'error': "User not found"}), 404
    
@app.route('/login', methods=["POST"])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')
  
  print(request.data)
  print(request.get_json())
  print(type(email))
  print(email)
  
  try:
    cursor = db.cursor()
    cursor.execute("SELECT password from users where email = %s", (email,))
    
    result = cursor.fetchone()
    cursor.close()
    
    if (result):
      passwordFetched = result[0]
      if (passwordFetched == password):
        return jsonify({'message': 'Logged in successfully'}), 201
    
      else:
        return jsonify({'message': 'Incorrect credentials'}), 404
      
    else:      
      return jsonify({'message': 'Incorrect credentials'}), 404
  
  except Error as e:
    return jsonify({'error':str(e)}), 400
    
@app.route('/user/<username>', methods=['PUT'])
def updateUser(username):
  
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')
  
  cursor = db.cursor()
  cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
  
  result = cursor.fetchone()
  
  if result:
    try:  
      if email and password:
        
        cursor.execute("UPDATE users SET email = %s, password = %s WHERE username = %s", (email, password, username))
        db.commit()
        return jsonify({'message': 'Updated email and password successfully'}), 200
      
      elif email:
        
        cursor.execute("UPDATE users SET email = %s WHERE username = %s", (email, username))
        db.commit()
        return jsonify({'message': 'Updated email successfully'}), 200
        
      elif password:
        
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (password, username))
        db.commit()
        return jsonify({'message': 'Updated password successfully'}), 200
    
    except Error as e:
      return jsonify({'error': str(e)}), 400
    
  else:
    return jsonify({'error': 'No such user exists'}), 404
  
@app.route('/user/<username>', methods=['DELETE'])
def deleteUser(username):
  
  cursor = db.cursor()
  cursor.execute("SELECT username FROM users WHERE username = %s", (username,))  
  
  result = cursor.fetchone()
  
  if result:
    
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    db.commit()
    return jsonify({'message': 'Sucessfully deleted ' + username}), 200
    
  else:
    return jsonify({'error': 'No such user found'}), 404  
  

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)