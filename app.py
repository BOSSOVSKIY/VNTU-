from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from google.oauth2 import service_account
from googleapiclient.discovery import build
from cryptography.fernet import Fernet
import sqlite3
import os
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"

# Static folder configuration
app.static_folder = 'static'

# Google login configuration
GOOGLE_CLIENT_ID = "105994916625578123031"
GOOGLE_CLIENT_SECRET = "your_client_secret_here"
GOOGLE_REDIRECT_URI = "http://localhost:5000/login"

# VirusTotal API configuration
VIRUSTOTAL_API_KEY = "your_api_key_here"

# Database configuration
DATABASE_FILE = "malicious_senders.db"

# Encryption configuration
ENCRYPTION_KEY = Fernet.generate_key()

# Create a Fernet object with the encryption key
fernet = Fernet(ENCRYPTION_KEY)

# Create a SQLite database connection
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Create a table to store the emails of malicious link senders
cursor.execute("""
    CREATE TABLE IF NOT EXISTS malicious_senders (
        email TEXT PRIMARY KEY
    );
""")

# Commit the changes
conn.commit()

# Close the connection
conn.close()

# Google login authorization
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id =?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    email = request.form["email"]
    password = request.form["password"]
    scan_interval = request.form["scan_interval"]
    # Here, you would handle login logic with Google and VirusTotal API
    # For now, we'll just simulate a login and redirect to the dashboard
    user_id = email  # Simplified user identification
    login_user(load_user(user_id))
    return redirect(url_for("dashboard"))

@app.route("/generate_fake_data")
def generate_fake_data():
    fake_emails = [
        {"email": f"fakeuser{i}@example.com", "link": f"http://malicious-link{i}.com"}
        for i in range(1, 11)
    ]
    return jsonify(fake_emails)

@app.route("/authorize", methods=["POST"])
def authorize():
    url = request.form["url"]
    api_key = VIRUSTOTAL_API_KEY
    response = requests.post(
        f"https://www.virustotal.com/vtapi/v2/url/scan",
        headers={"Authorization": f"Bearer {api_key}"},
        data={"url": url},
    )
    if response.status_code == 200:
        # Store the URL in the database
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO malicious_senders (email) VALUES (?)", (url,))
        conn.commit()
        conn.close()
        return "Authorized successfully!"
    return "Error authorizing with VirusTotal API"

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
