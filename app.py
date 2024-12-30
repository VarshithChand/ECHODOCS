from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Used for session management

# Configurations for file upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx',
                      'xlsx', 'csv', 'ppt', 'pptx', 'mp4', 'avi', 'zip', 'rar'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy user and superuser data
USER_DATA = {"testusser": "password1", "testuser2": "password2"}  # Regular user
SUPERUSER_DATA = {"admin": "adminpassword"}  # Superuser

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def login():
    """Login route."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USER_DATA and password == USER_DATA[username]:
            session["username"] = username
            session["is_superuser"] = False  # Regular user
            return redirect(url_for("welcome"))
        elif username in SUPERUSER_DATA and password == SUPERUSER_DATA[username]:
            session["username"] = username
            session["is_superuser"] = True  # Superuser
            return redirect(url_for("superuser_dashboard"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/welcome")
def welcome():
    """Welcome page for regular users."""
    if "username" in session and not session.get("is_superuser"):
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
        return render_template("welcome.html", username=session["username"], files=uploaded_files)
    return redirect(url_for("login"))

@app.route("/superuser_dashboard")
def superuser_dashboard():
    """Dashboard for the superuser."""
    if "username" in session and session.get("is_superuser"):
        uploaded_files = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
        return render_template("superuser_dashboard.html", users=list(USER_DATA.keys()), files=uploaded_files)
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    """Logout route."""
    session.pop("username", None)
    session.pop("is_superuser", None)
    return redirect(url_for("login"))

@app.route("/uploads", methods=["GET", "POST"])
def uploads():
    """Handles file uploads for both regular users and superusers."""
    if "username" not in session:
        return redirect(url_for("login"))

    # Determine the appropriate dashboard URL
    dashboard_url = url_for('superuser_dashboard') if session.get("is_superuser") else url_for('welcome')

    if request.method == "POST":
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("uploads"))

    uploaded_files = os.listdir(app.config["UPLOAD_FOLDER"]) if os.path.exists(app.config["UPLOAD_FOLDER"]) else []
    return render_template("uploads.html", files=uploaded_files, dashboard_url=dashboard_url)

@app.route("/delete_files", methods=["POST"])
def delete_files():
    """Handles deletion of selected files."""
    if "username" not in session:
        return redirect(url_for("login"))

    selected_files = request.form.getlist("selected_files")
    for file in selected_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.exists(file_path):
            os.remove(file_path)

    return redirect(url_for("uploads"))

@app.route("/manage_users", methods=["POST"])
def manage_users():
    """Allows the superuser to add or delete users."""
    if "username" in session and session.get("is_superuser"):
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")

        if action == "add" and username and password:
            USER_DATA[username] = password
        elif action == "delete" and username in USER_DATA:
            del USER_DATA[username]

    return redirect(url_for("superuser_dashboard"))

@app.route("/serve_file/<filename>")
def serve_file(filename):
    """Serves files from the uploads directory."""
    if "username" not in session:
        return redirect(url_for("login"))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
