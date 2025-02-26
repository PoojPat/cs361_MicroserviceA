from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


# Initialize the database
def init_db():
    with sqlite3.connect("quiz_stats.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quiz_id INTEGER NOT NULL,
                score REAL NOT NULL,
                difficulty TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


# Root endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Quiz Statistics Microservice",
        "endpoints": {
            "record_score": "POST /record-score",
            "user_stats": "GET /user-stats/<int:user_id>",
            "difficulty_stats": "GET /difficulty-stats/<string:difficulty>"
        }
    })


# Record a quiz score
@app.route('/record-score', methods=['POST'])
def record_score():
    data = request.json
    user_id = data.get('user_id')
    quiz_id = data.get('quiz_id')
    score = data.get('score')
    difficulty = data.get('difficulty')

    if None in (user_id, quiz_id, score, difficulty):
        return jsonify({"error": "Missing required fields"}), 400

    with sqlite3.connect("quiz_stats.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO quiz_performance (user_id, quiz_id, score, difficulty)
            VALUES (?, ?, ?, ?)
        ''', (user_id, quiz_id, score, difficulty))
        conn.commit()

    return jsonify({"message": "Score recorded successfully"}), 201


# Get user statistics
@app.route('/user-stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    with sqlite3.connect("quiz_stats.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*), AVG(score), MAX(score), MIN(score)
            FROM quiz_performance WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()

    if result[0] == 0:
        return jsonify({"message": "No data available for this user"}), 404

    return jsonify({
        "user_id": user_id,
        "total_quizzes": result[0],
        "average_score": result[1],
        "highest_score": result[2],
        "lowest_score": result[3],
        "timestamp": datetime.utcnow().isoformat()
    })


# Get difficulty-based statistics
@app.route('/difficulty-stats/<string:difficulty>', methods=['GET'])
def get_difficulty_stats(difficulty):
    with sqlite3.connect("quiz_stats.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT difficulty, AVG(score), COUNT(*)
            FROM quiz_performance WHERE difficulty = ? GROUP BY difficulty
        ''', (difficulty,))
        result = cursor.fetchone()

    if not result:
        return jsonify({"message": "No data available for this difficulty"}), 404

    return jsonify({
        "difficulty": result[0],
        "average_score": result[1],
        "total_attempts": result[2],
        "timestamp": datetime.utcnow().isoformat()
    })


# Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
