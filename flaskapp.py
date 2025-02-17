import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

# ------------------------------------------------------------------------------
# 1. Set Up Absolute Paths
# ------------------------------------------------------------------------------
# __file__ is the path to this current Python script, i.e., /home/ubuntu/flaskapp/flaskapp.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Point to 'uploads' folder *inside* this directory
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# Ensure the uploads folder exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

# ------------------------------------------------------------------------------
# 2. Routes
# ------------------------------------------------------------------------------

@app.route('/')
def index():
    """
    Home page: offers links to register or re-login.
    """
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration page. Accepts:
      - username, password
      - firstname, lastname
      - email, address
      - optional file upload (extra credit)
    Inserts data into SQLite 'users' table, then redirects to display_info.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        address = request.form.get('address')

        # Insert into SQLite database
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (username, password, firstname, lastname, email, address)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, firstname, lastname, email, address))
        conn.commit()
        conn.close()

        # If there's a file uploaded (extra credit), save it in UPLOAD_FOLDER
        file = request.files.get('limerick_file')
        if file and file.filename.strip():
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

        return redirect(url_for('display_info', username=username))
    else:
        return render_template('register.html')


@app.route('/display/<username>')
def display_info(username):
    """
    After registering or re-logging in, display the user's information.
    If a file (like Limerick-1-1.txt) was uploaded, calculate word count
    and offer a download link (extra credit).
    """
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
    c = conn.cursor()
    c.execute("SELECT username, firstname, lastname, email, address FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if not user:
        return "User not found!", 404

    word_count = None
    uploaded_file_name = "Limerick-1-1.txt"  # or match whatever file name you expect

    # If the known file exists in the uploads folder, count the words
    possible_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file_name)
    if os.path.exists(possible_file_path):
        with open(possible_file_path, 'r', encoding='utf-8') as f:
            contents = f.read()
            word_count = len(contents.split())

    return render_template('display.html',
                           user=user,
                           word_count=word_count,
                           uploaded_file_name=uploaded_file_name if word_count else None)


@app.route('/download/<filename>')
def download_file(filename):
    """
    Allows user to download a file from the uploads folder (extra credit).
    """
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found.", 404


@app.route('/relogin', methods=['GET', 'POST'])
def relogin():
    """
    Page to re-login by username/password and retrieve user info.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect(os.path.join(BASE_DIR, 'users.db'))
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=? AND password=?", (username, password))
        row = c.fetchone()
        conn.close()

        if row:
            return redirect(url_for('display_info', username=username))
        else:
            return "Invalid username or password!", 401
    else:
        return render_template('relogin.html')


# ------------------------------------------------------------------------------
# 3. Main Entry Point (if running with `python flaskapp.py`)
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
