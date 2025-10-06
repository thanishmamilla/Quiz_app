# import sqlite3
# import json
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, JWTManager
# from werkzeug.security import generate_password_hash, check_password_hash # For password security

# app = Flask(__name__)
# # Allow all origins for development
# CORS(app) 

# DATABASE = 'quiz.db'

# # --- JWT Configuration ---
# app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this-in-production" # Change this!
# jwt = JWTManager(app)

# # Custom JWT Claims Loader to include user role in the token
# @jwt.additional_claims_loader
# def add_claims_to_access_token(identity):
#     conn = get_db_connection()
#     # identity is the username
#     user = conn.execute("SELECT role FROM users WHERE username = ?", (identity,)).fetchone()
#     conn.close()
#     return {"role": user['role']} if user else {"role": "user"}

# # --- Database Utility and Initialization ---

# def get_db_connection():
#     """Establishes a connection to the database."""
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row  # Access columns by name
#     return conn

# def init_db():
#     """Initializes the database and populates it with sample data."""
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # 1. Create Users table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             username TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL,
#             role TEXT NOT NULL DEFAULT 'user' -- 'user' or 'admin'
#         )
#     ''')
    
#     # 2. Create Quizzes table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS quizzes (
#             id INTEGER PRIMARY KEY,
#             title TEXT NOT NULL
#         )
#     ''')

#     # 3. Create Questions table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS questions (
#             id INTEGER PRIMARY KEY,
#             quiz_id INTEGER NOT NULL,
#             question_text TEXT NOT NULL,
#             option_1 TEXT NOT NULL,
#             option_2 TEXT NOT NULL,
#             option_3 TEXT NOT NULL,
#             option_4 TEXT NOT NULL,
#             correct_option_index INTEGER NOT NULL, -- 0-based index (0, 1, 2, or 3)
#             FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
#         )
#     ''')

#     # --- Sample Data Insertion ---
    
#     # Insert default admin and user if not exists
#     cursor.execute("SELECT COUNT(*) FROM users")
#     if cursor.fetchone()[0] == 0:
#         admin_pass_hash = generate_password_hash("adminpass")
#         user_pass_hash = generate_password_hash("userpass")
#         cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                        ('admin', admin_pass_hash, 'admin'))
#         cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                        ('testuser', user_pass_hash, 'user'))

#     # Insert sample quizzes if tables are empty
#     cursor.execute("SELECT COUNT(*) FROM quizzes")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", ('Python Basics',))
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", ('World Geography',))
        
#         # Python Quiz (quiz_id 1)
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (1, "Which keyword is used for a function in Python?", "class", "import", "def", "for", 2))
        
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (1, "What is the primary way to define a block of code in Python?", "Indentation", "Curly Braces {}", "Parentheses ()", "Semicolons ;", 0))

#         # Geography Quiz (quiz_id 2)
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (2, "What is the capital of Canada?", "Toronto", "Ottawa", "Vancouver", "Montreal", 1))

#     conn.commit()
#     conn.close()

# # Initialize DB when the app starts
# with app.app_context():
#     init_db()

# # --- Authentication Endpoints (These were already complete) ---

# @app.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({"msg": "Missing username or password"}), 400

#     conn = get_db_connection()
#     try:
#         password_hash = generate_password_hash(password)
#         conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                      (username, password_hash, 'user'))
#         conn.commit()
#         return jsonify({"msg": "User created successfully"}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({"msg": "Username already exists"}), 409
#     finally:
#         conn.close()

# @app.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     conn = get_db_connection()
#     user = conn.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
#     conn.close()

#     if user and check_password_hash(user['password_hash'], password):
#         access_token = create_access_token(identity=user['username']) 
#         return jsonify(access_token=access_token, user_role=user['role'])
    
#     return jsonify({"msg": "Bad username or password"}), 401

# # --- Admin Endpoint: Add New Quiz (This was already complete) ---

# @app.route('/api/quizzes', methods=['POST'])
# @jwt_required()
# def add_quiz():
#     claims = get_jwt()
#     if claims.get('role') != 'admin':
#         return jsonify({"msg": "Admin privileges required"}), 403
    
#     data = request.get_json()
#     title = data.get('title')
#     questions = data.get('questions', [])

#     if not title or not questions:
#         return jsonify({"msg": "Missing title or questions data"}), 400

#     conn = get_db_connection()
#     try:
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", (title,))
#         quiz_id = cursor.lastrowid

#         for q in questions:
#             cursor.execute("""
#                 INSERT INTO questions 
#                 (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             """, (quiz_id, q['text'], q['options'][0], q['options'][1], q['options'][2], q['options'][3], q['correct_index']))
        
#         conn.commit()
#         return jsonify({"msg": "Quiz added successfully", "quiz_id": quiz_id}), 201
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"msg": f"An error occurred: {str(e)}"}), 500
#     finally:
#         conn.close()

# # --- Quiz Endpoints (Restored implementations) ---

# @app.route('/api/quizzes', methods=['GET'])
# def get_quizzes():
#     """Returns a list of available quizzes (PUBLIC access)."""
#     conn = get_db_connection()
#     try:
#         # Fetch all quiz IDs and titles
#         quizzes = conn.execute("SELECT id, title FROM quizzes").fetchall()
        
#         # Convert the list of SQLite rows to a list of dictionaries (JSON format)
#         return jsonify([dict(quiz) for quiz in quizzes])
        
#     except Exception as e:
#         # Log the error and return a generic server error
#         print(f"Database error in get_quizzes: {e}")
#         return jsonify({"error": "Could not fetch quizzes due to a server error."}), 500
#     finally:
#         conn.close()

# @app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
# @jwt_required(optional=True) 
# def get_questions(quiz_id):
#     """Returns all questions for a specific quiz (without correct answers)."""
#     conn = get_db_connection()
    
#     questions_data = conn.execute(
#         "SELECT id, question_text, option_1, option_2, option_3, option_4 FROM questions WHERE quiz_id = ?", 
#         (quiz_id,)
#     ).fetchall()
    
#     conn.close()

#     questions_list = []
#     for q in questions_data:
#         questions_list.append({
#             'id': q['id'],
#             'text': q['question_text'],
#             'options': [q['option_1'], q['option_2'], q['option_3'], q['option_4']]
#         })
    
#     if not questions_list:
#         return jsonify({"error": "Quiz not found or has no questions"}), 404
        
#     return jsonify(questions_list)


# @app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
# @jwt_required() 
# def submit_quiz(quiz_id):
#     """Calculates the score and returns results (Requires Login)."""
#     try:
#         user_answers = request.json.get('answers', {}) # { "question_id": selected_index }
#     except Exception:
#         return jsonify({"error": "Invalid JSON or missing 'answers' field"}), 400

#     conn = get_db_connection()
    
#     question_ids = tuple(user_answers.keys())
#     if not question_ids:
#         return jsonify({"error": "No answers provided"}), 400

#     # Fetch correct answers for submitted questions in this quiz
#     query = f"""
#         SELECT id, question_text, correct_option_index, option_1, option_2, option_3, option_4
#         FROM questions 
#         WHERE id IN ({','.join(['?'] * len(question_ids))}) AND quiz_id = ?
#     """
    
#     params = list(question_ids) + [quiz_id]
#     correct_data = conn.execute(query, params).fetchall()
#     conn.close()

#     if not correct_data:
#          return jsonify({"error": "Questions not found for this quiz ID"}), 404

#     # Calculate Score
#     score = 0
#     results = []
    
#     for row in correct_data:
#         q_id = str(row['id'])
#         correct_index = row['correct_option_index']
#         user_index = user_answers.get(q_id, -1) 

#         is_correct = user_index == correct_index
#         if is_correct:
#             score += 1
            
#         all_options = [row['option_1'], row['option_2'], row['option_3'], row['option_4']]
        
#         results.append({
#             "id": q_id,
#             "text": row['question_text'],
#             "is_correct": is_correct,
#             "user_answer_index": user_index,
#             "correct_answer_index": correct_index,
#             "correct_answer_text": all_options[correct_index]
#         })
        
#     # Return results
#     return jsonify({
#         "score": score,
#         "total_questions": len(correct_data),
#         "results": results
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)



# import sqlite3
# import json
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, JWTManager
# from werkzeug.security import generate_password_hash, check_password_hash 

# app = Flask(__name__)
# CORS(app) 

# DATABASE = 'quiz.db'

# # --- JWT Configuration ---
# app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this-in-production"
# jwt = JWTManager(app)

# # Custom JWT Claims Loader
# @jwt.additional_claims_loader
# def add_claims_to_access_token(identity):
#     conn = get_db_connection()
#     user = conn.execute("SELECT role FROM users WHERE username = ?", (identity,)).fetchone()
#     conn.close()
#     return {"role": user['role']} if user else {"role": "user"}

# # --- Database Utility and Initialization ---

# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # 1. Create Users table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY,
#             username TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL,
#             role TEXT NOT NULL DEFAULT 'user'
#         )
#     ''')
    
#     # 2. Create Quizzes table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS quizzes (
#             id INTEGER PRIMARY KEY,
#             title TEXT NOT NULL
#         )
#     ''')

#     # 3. Create Questions table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS questions (
#             id INTEGER PRIMARY KEY,
#             quiz_id INTEGER NOT NULL,
#             question_text TEXT NOT NULL,
#             option_1 TEXT NOT NULL,
#             option_2 TEXT NOT NULL,
#             option_3 TEXT NOT NULL,
#             option_4 TEXT NOT NULL,
#             correct_option_index INTEGER NOT NULL, -- 0-based index (0, 1, 2, or 3)
#             FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
#         )
#     ''')

#     # --- Sample Data Insertion ---
    
#     # Insert default admin and user
#     cursor.execute("SELECT COUNT(*) FROM users")
#     if cursor.fetchone()[0] == 0:
#         admin_pass_hash = generate_password_hash("adminpass")
#         user_pass_hash = generate_password_hash("userpass")
#         cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                        ('admin', admin_pass_hash, 'admin'))
#         cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                        ('testuser', user_pass_hash, 'user'))

#     # Insert sample quizzes
#     cursor.execute("SELECT COUNT(*) FROM quizzes")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", ('Python Basics',))
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", ('World Geography',))
        
#         # Python Quiz (quiz_id 1)
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (1, "Which keyword is used for a function in Python?", "class", "import", "def", "for", 2))
        
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (1, "What is the primary way to define a block of code in Python?", "Indentation", "Curly Braces {}", "Parentheses ()", "Semicolons ;", 0))

#         # Geography Quiz (quiz_id 2)
#         cursor.execute("""
#             INSERT INTO questions 
#             (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (2, "What is the capital of Canada?", "Toronto", "Ottawa", "Vancouver", "Montreal", 1))

#     conn.commit()
#     conn.close()

# with app.app_context():
#     init_db()

# # --- Authentication Endpoints ---

# @app.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({"msg": "Missing username or password"}), 400

#     conn = get_db_connection()
#     try:
#         password_hash = generate_password_hash(password)
#         conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
#                      (username, password_hash, 'user'))
#         conn.commit()
#         return jsonify({"msg": "User created successfully"}), 201
#     except sqlite3.IntegrityError:
#         return jsonify({"msg": "Username already exists"}), 409
#     finally:
#         conn.close()

# @app.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     conn = get_db_connection()
#     user = conn.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
#     conn.close()

#     if user and check_password_hash(user['password_hash'], password):
#         access_token = create_access_token(identity=user['username']) 
#         return jsonify(access_token=access_token, user_role=user['role'], username=user['username'])
    
#     return jsonify({"msg": "Bad username or password"}), 401

# # --- Admin Endpoint: Add New Quiz ---

# @app.route('/api/quizzes', methods=['POST'])
# @jwt_required()
# def add_quiz():
#     claims = get_jwt()
#     if claims.get('role') != 'admin':
#         return jsonify({"msg": "Admin privileges required"}), 403
    
#     data = request.get_json()
#     title = data.get('title')
#     questions = data.get('questions', [])

#     if not title or not questions:
#         return jsonify({"msg": "Missing title or questions data"}), 400

#     conn = get_db_connection()
#     try:
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO quizzes (title) VALUES (?)", (title,))
#         quiz_id = cursor.lastrowid

#         for q in questions:
#             cursor.execute("""
#                 INSERT INTO questions 
#                 (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             """, (quiz_id, q['text'], q['options'][0], q['options'][1], q['options'][2], q['options'][3], q['correct_index']))
        
#         conn.commit()
#         return jsonify({"msg": "Quiz added successfully", "quiz_id": quiz_id}), 201
#     except Exception as e:
#         conn.rollback()
#         return jsonify({"msg": f"An error occurred: {str(e)}"}), 500
#     finally:
#         conn.close()

# # --- Quiz Endpoints ---

# @app.route('/api/quizzes', methods=['GET'])
# def get_quizzes():
#     """Returns a list of available quizzes (PUBLIC access)."""
#     conn = get_db_connection()
#     try:
#         quizzes = conn.execute("SELECT id, title FROM quizzes").fetchall()
#         return jsonify([dict(quiz) for quiz in quizzes])
#     except Exception as e:
#         print(f"Database error in get_quizzes: {e}")
#         return jsonify({"error": "Could not fetch quizzes due to a server error."}), 500
#     finally:
#         conn.close()

# @app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
# @jwt_required(optional=True) 
# def get_questions(quiz_id):
#     """Returns all questions for a specific quiz (without correct answers)."""
#     conn = get_db_connection()
    
#     questions_data = conn.execute(
#         "SELECT id, question_text, option_1, option_2, option_3, option_4 FROM questions WHERE quiz_id = ?", 
#         (quiz_id,)
#     ).fetchall()
    
#     conn.close()

#     questions_list = []
#     for q in questions_data:
#         questions_list.append({
#             'id': q['id'],
#             'text': q['question_text'],
#             'options': [q['option_1'], q['option_2'], q['option_3'], q['option_4']]
#         })
    
#     if not questions_list:
#         return jsonify({"error": "Quiz not found or has no questions"}), 404
        
#     return jsonify(questions_list)


# @app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
# @jwt_required() 
# def submit_quiz(quiz_id):
#     """Calculates the score and returns results (Requires Login)."""
#     try:
#         user_answers = request.json.get('answers', {})
#     except Exception:
#         return jsonify({"error": "Invalid JSON or missing 'answers' field"}), 400

#     conn = get_db_connection()
    
#     question_ids = tuple(user_answers.keys())
#     if not question_ids:
#         return jsonify({"error": "No answers provided"}), 400

#     # Fetch correct answers for submitted questions in this quiz
#     query = f"""
#         SELECT id, question_text, correct_option_index, option_1, option_2, option_3, option_4
#         FROM questions 
#         WHERE id IN ({','.join(['?'] * len(question_ids))}) AND quiz_id = ?
#     """
    
#     params = list(question_ids) + [quiz_id]
#     correct_data = conn.execute(query, params).fetchall()
#     conn.close()

#     if not correct_data:
#          return jsonify({"error": "Questions not found for this quiz ID"}), 404

#     # Calculate Score
#     score = 0
#     results = []
    
#     for row in correct_data:
#         q_id = str(row['id'])
#         correct_index = row['correct_option_index']
#         user_index = user_answers.get(q_id, -1) 

#         is_correct = user_index == correct_index
#         if is_correct:
#             score += 1
            
#         all_options = [row['option_1'], row['option_2'], row['option_3'], row['option_4']]
        
#         results.append({
#             "id": q_id,
#             "text": row['question_text'],
#             "is_correct": is_correct,
#             "user_answer_index": user_index,
#             "correct_answer_index": correct_index,
#             "correct_answer_text": all_options[correct_index]
#         })
        
#     # Return results
#     return jsonify({
#         "score": score,
#         "total_questions": len(correct_data),
#         "results": results
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

import sqlite3
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
# Allow all origins for development
CORS(app) 

DATABASE = 'quiz.db'

# --- JWT Configuration ---
# WARNING: Change this key in production
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this-in-production"
jwt = JWTManager(app)

# Custom JWT Claims Loader: Ensures the user's role is stored in the JWT payload
@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    conn = get_db_connection()
    user = conn.execute("SELECT role FROM users WHERE username = ?", (identity,)).fetchone()
    conn.close()
    return {"role": user['role']} if user else {"role": "user"}

# --- Database Utility and Initialization ---

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by column name
    return conn

def init_db():
    """Initializes the database and populates it with default users/quizzes."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')
    
    # 2. Create Quizzes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL
        )
    ''')

    # 3. Create Questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            option_1 TEXT NOT NULL,
            option_2 TEXT NOT NULL,
            option_3 TEXT NOT NULL,
            option_4 TEXT NOT NULL,
            correct_option_index INTEGER NOT NULL, -- 0-based index (0, 1, 2, or 3)
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        )
    ''')

    # --- Sample Data Insertion ---
    
    # Insert default admin and user (only if tables are empty)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_pass_hash = generate_password_hash("adminpass")
        user_pass_hash = generate_password_hash("userpass")
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       ('Admin', admin_pass_hash, 'admin'))
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       ('tuser', user_pass_hash, 'user'))

    # Insert sample quizzes (only if tables are empty)
    
    conn.commit()
    conn.close()

with app.app_context():
    init_db()

# --- Authentication Endpoints ---

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                     (username, password_hash, 'user'))
        conn.commit()
        return jsonify({"msg": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"msg": "Username already exists"}), 409
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute("SELECT username, password_hash, role FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=user['username']) 
        # CRITICAL: Return username for frontend score storage
        return jsonify(access_token=access_token, user_role=user['role'], username=user['username']) 
    
    return jsonify({"msg": "Bad username or password"}), 401

# --- Admin Endpoint: Add New Quiz ---

@app.route('/api/quizzes', methods=['POST'])
@jwt_required()
def add_quiz():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin privileges required"}), 403
    
    data = request.get_json()
    title = data.get('title')
    questions = data.get('questions', [])

    if not title or not questions:
        return jsonify({"msg": "Missing title or questions data"}), 400

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quizzes (title) VALUES (?)", (title,))
        quiz_id = cursor.lastrowid

        for q in questions:
            # Note: q['options'] is expected to be a list of 4 strings
            cursor.execute("""
                INSERT INTO questions 
                (quiz_id, question_text, option_1, option_2, option_3, option_4, correct_option_index) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (quiz_id, q['text'], q['options'][0], q['options'][1], q['options'][2], q['options'][3], q['correct_index']))
        
        conn.commit()
        return jsonify({"msg": "Quiz added successfully", "quiz_id": quiz_id}), 201
    except Exception as e:
        conn.rollback()
        # Ensure error message is clear, especially if data format is bad
        return jsonify({"msg": f"An error occurred during quiz insertion: {str(e)}"}), 500
    finally:
        conn.close()

# --- Quiz Endpoints ---

@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    """Returns a list of available quizzes (PUBLIC access)."""
    conn = get_db_connection()
    try:
        quizzes = conn.execute("SELECT id, title FROM quizzes").fetchall()
        # Return valid JSON response
        return jsonify([dict(quiz) for quiz in quizzes])
    except Exception as e:
        print(f"Database error in get_quizzes: {e}")
        return jsonify({"error": "Could not fetch quizzes due to a server error."}), 500
    finally:
        conn.close()

@app.route('/api/quizzes/<int:quiz_id>/questions', methods=['GET'])
@jwt_required(optional=True) 
def get_questions(quiz_id):
    """Returns all questions for a specific quiz (without correct answers)."""
    conn = get_db_connection()
    
    questions_data = conn.execute(
        "SELECT id, question_text, option_1, option_2, option_3, option_4 FROM questions WHERE quiz_id = ?", 
        (quiz_id,)
    ).fetchall()
    
    conn.close()

    questions_list = []
    for q in questions_data:
        questions_list.append({
            'id': q['id'],
            'text': q['question_text'],
            'options': [q['option_1'], q['option_2'], q['option_3'], q['option_4']]
        })
    
    if not questions_list:
        return jsonify({"error": "Quiz not found or has no questions"}), 404
        
    return jsonify(questions_list)


@app.route('/api/quizzes/<int:quiz_id>/submit', methods=['POST'])
@jwt_required() 
def submit_quiz(quiz_id):
    """Calculates the score and returns results (Requires Login)."""
    try:
        user_answers = request.json.get('answers', {})
    except Exception:
        return jsonify({"error": "Invalid JSON or missing 'answers' field"}), 400

    conn = get_db_connection()
    
    question_ids = tuple(user_answers.keys())
    if not question_ids:
        return jsonify({"error": "No answers provided"}), 400

    # Fetch correct answers
    # Use f-string formatting safely here since question_ids contains only keys from a controlled object
    query = f"""
        SELECT id, question_text, correct_option_index, option_1, option_2, option_3, option_4
        FROM questions 
        WHERE id IN ({','.join(['?'] * len(question_ids))}) AND quiz_id = ?
    """
    
    params = list(question_ids) + [quiz_id]
    correct_data = conn.execute(query, params).fetchall()
    conn.close()

    if not correct_data:
         return jsonify({"error": "Questions not found for this quiz ID"}), 404

    # Calculate Score
    score = 0
    results = []
    
    for row in correct_data:
        q_id = str(row['id'])
        correct_index = row['correct_option_index']
        user_index = user_answers.get(q_id, -1) 

        is_correct = user_index == correct_index
        if is_correct:
            score += 1
            
        all_options = [row['option_1'], row['option_2'], row['option_3'], row['option_4']]
        
        results.append({
            "id": q_id,
            "text": row['question_text'],
            "is_correct": is_correct,
            "user_answer_index": user_index,
            "correct_answer_index": correct_index,
            "correct_answer_text": all_options[correct_index]
        })
        
    # Return results
    return jsonify({
        "score": score,
        "total_questions": len(correct_data),
        "results": results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)