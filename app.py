"""
Flask-Based Student Registration Web Application
--------------------------------------------------
Provides:
  GET  /          -> registration form
  POST /          -> handle registration form submission
  GET  /students  -> list all registered students
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "student_user"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "studentsdb"),
}


def get_db_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()
        address = request.form.get("address", "").strip()

        # Server-side validation
        if not name or not email or not phone or not course or not address:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                INSERT INTO students
                (name, email, phone, course, address)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, phone, course, address))
            conn.commit()

            cursor.close()
            conn.close()

            flash("Student Registered Successfully!", "success")
            return redirect(url_for("register"))

        except Error as e:
            flash(f"Database error: {e}", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/students")
def students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, phone, course, address
            FROM students
            ORDER BY id DESC
            """
        )
        all_students = cursor.fetchall()

        cursor.close()
        conn.close()

    except Error as e:
        flash(f"Database error: {e}", "error")
        all_students = []

    return render_template("students.html", students=all_students)


if __name__ == "__main__":
    # Runs on all interfaces so it's reachable via the EC2 public IP on port 5000
    app.run(host="0.0.0.0", port=5000, debug=False)
