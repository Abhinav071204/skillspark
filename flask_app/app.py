from flask import Flask, render_template, request, session, redirect, url_for, flash
import sys
import os
import sqlite3
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ai.recommender import get_recommendations

app = Flask(__name__)
app.secret_key = "skillspark123"

DB_FILE = "skillspark.db"

# ========== DATABASE SETUP ==========
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hobbies TEXT NOT NULL,
        level TEXT NOT NULL,
        goal TEXT NOT NULL,
        recommendations TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT,
        bio TEXT,
        interests TEXT,
        linkedin TEXT,
        github TEXT,
        updated_at TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# ========== ROUTES ==========
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/input')
def input_page():
    if "user" not in session:
        flash("Please login first!")
        return redirect(url_for('login'))
    return render_template('input.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if "user" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        hobbies = request.form.get('hobbies')
        level = request.form.get('level')
        goal = request.form.get('goal')
        result = get_recommendations(hobbies, level, goal)

        conn = get_db()
        conn.execute(
            "INSERT INTO history (username, hobbies, level, goal, recommendations, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (session['user'], hobbies, level, goal, result, datetime.now().strftime("%d %b %Y, %I:%M %p"))
        )
        conn.commit()
        conn.close()

        session['hobbies'] = hobbies
        session['level'] = level
        session['goal'] = goal
        session['recommendations'] = result

        return render_template('recommendations.html', result=result, hobbies=hobbies, level=level, goal=goal)
    return render_template('recommendations.html')

@app.route('/history')
def history():
    if "user" not in session:
        return redirect(url_for('login'))
    conn = get_db()
    records = conn.execute(
        "SELECT * FROM history WHERE username = ? ORDER BY id DESC",
        (session['user'],)
    ).fetchall()
    conn.close()
    return render_template('history.html', records=records)

@app.route('/delete_history/<int:record_id>')
def delete_history(record_id):
    if "user" not in session:
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute("DELETE FROM history WHERE id = ? AND username = ?", (record_id, session['user']))
    conn.commit()
    conn.close()
    flash("Record deleted!")
    return redirect(url_for('history'))

@app.route('/profile')
def profile():
    if "user" not in session:
        return redirect(url_for('login'))
    conn = get_db()
    prof = conn.execute(
        "SELECT * FROM profiles WHERE username = ?",
        (session['user'],)
    ).fetchone()
    total_sessions = conn.execute(
        "SELECT COUNT(*) FROM history WHERE username = ?",
        (session['user'],)
    ).fetchone()[0]
    conn.close()
    return render_template('profile.html', profile=prof, total_sessions=total_sessions)

@app.route('/profile/edit', methods=['POST'])
def edit_profile():
    if "user" not in session:
        return redirect(url_for('login'))
    full_name = request.form.get('full_name')
    bio = request.form.get('bio')
    interests = request.form.get('interests')
    linkedin = request.form.get('linkedin')
    github = request.form.get('github')
    conn = get_db()
    existing = conn.execute(
        "SELECT * FROM profiles WHERE username = ?",
        (session['user'],)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE profiles SET full_name=?, bio=?, interests=?, linkedin=?, github=?, updated_at=? WHERE username=?",
            (full_name, bio, interests, linkedin, github, datetime.now().strftime("%d %b %Y"), session['user'])
        )
    else:
        conn.execute(
            "INSERT INTO profiles (username, full_name, bio, interests, linkedin, github, updated_at) VALUES (?,?,?,?,?,?,?)",
            (session['user'], full_name, bio, interests, linkedin, github, datetime.now().strftime("%d %b %Y"))
        )
    conn.commit()
    conn.close()
    flash("Profile updated!")
    return redirect(url_for('profile'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                (username, password, datetime.now().strftime("%d %b %Y"))
            )
            conn.commit()
            flash("Account created! Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!")
            return redirect(url_for('register'))
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('home'))
        flash("Invalid credentials!")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)