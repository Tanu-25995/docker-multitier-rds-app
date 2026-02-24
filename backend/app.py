from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/students")
def students():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )
    """)

    cur.execute("SELECT COUNT(*) FROM students")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("INSERT INTO students (name) VALUES ('Tanuja'), ('DevOps Learner')")
        conn.commit()

    cur.execute("SELECT id, name FROM students")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "name": r[1]} for r in rows])
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name) VALUES (%s)", (name,))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()

    return jsonify({"id": new_id, "name": name}), 201
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name=%s WHERE id=%s", (name, student_id))
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "student not found"}), 404

    cur.close()
    conn.close()
    return jsonify({"id": student_id, "name": name})


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return jsonify({"error": "student not found"}), 404

    cur.close()
    conn.close()
    return jsonify({"deleted": student_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
