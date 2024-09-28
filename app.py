from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect('users.db')
    return conn

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Form page route
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        bio = request.form['bio']

        # Basic error handling
        if not name or not age or not bio:
            flash("All fields are required!", "error")
            return redirect(url_for('form'))

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, age, bio) VALUES (?, ?, ?)", (name, age, bio))
        conn.commit()
        conn.close()
        flash("User data saved successfully!", "success")
        return redirect(url_for('display'))

    return render_template('form.html')

# Display page route
@app.route('/display')
def display():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('display.html', users=users)

# API endpoint to return all user data as JSON
@app.route('/api/users')
def api_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    # Format the data as JSON
    user_list = [{"id": user[0], "name": user[1], "age": user[2], "bio": user[3]} for user in users]
    return jsonify(user_list)

# Edit user page route
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        bio = request.form['bio']

        # Basic error handling
        if not name or not age or not bio:
            flash("All fields are required!", "error")
            return redirect(url_for('edit', user_id=user_id))

        cursor.execute("UPDATE users SET name = ?, age = ?, bio = ? WHERE id = ?", (name, age, bio, user_id))
        conn.commit()
        conn.close()
        flash("User data updated successfully!", "success")
        return redirect(url_for('display'))

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

# Delete user API
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User data deleted successfully!", "success")
    return redirect(url_for('display'))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
