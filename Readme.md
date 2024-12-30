# Setting Up a Python-Flask Application on a Linux Instance

This guide provides step-by-step instructions to set up a Flask application on a Linux instance with HTTP and custom TCP protocols.

---

## Steps to Set Up the Linux Instance

1. **Create a Linux instance**.
2. **Enable HTTP Server**:
   - Keep the server `http` on.
   - Ensure the port range is set to **80**.
3. **Create Custom TCP Protocol**:
   - Add a custom TCP protocol with the server port range **5000**.

---

## After Launching the Linux Instance

### Connect to the Instance
1. Open the console and connect to the Linux instance.

### Commands to Set Up the Environment and Application
Below are the commands to set up the Flask application:

1. Switch to the root user:
   ```bash
   sudo su
   ```
2. Install Apache HTTP server:
   ```bash
   yum install httpd
   ```
3. Start the HTTP service:
   ```bash
   service httpd start
   ```
4. Install Python 3:
   ```bash
   sudo yum install python-3 -y
   ```
5. Install GCC and Python development tools:
   ```bash
   sudo yum install gcc python-devel -y
   ```
6. Install `virtualenv` for creating isolated environments:
   ```bash
   sudo yum install virtualenv
   ```
7. Create a project directory:
   ```bash
   mkdir project_name
   ```
8. Navigate into the project directory:
   ```bash
   cd project_name
   ```
9. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   ```
10. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
11. Install Flask and Gunicorn (WSGI server):
    ```bash
    pip install Flask gunicorn
    ```
12. Create the main application file:
    ```bash
    vim app.py
    ```
13. Create the following directories for templates, static files, and uploads:
    ```bash
    mkdir templates
    mkdir static
    mkdir uploads
    ```
14. Navigate into the `templates` directory and create the following HTML files:
    ```bash
    cd templates
    vim login.html
    vim welcome.html
    vim uploads.html
    vim superuser_dashboard.html
    ```
15. Navigate to the `static` directory and create the CSS file:
    ```bash
    cd ../static
    vim login.css
    vim uploads.css
    vim superuser_dashboard.css
     ```
16. Return to the project root directory:
    ```bash
    cd ..
    ```

---

## Running the Project

1. Start the server using Gunicorn:
   ```bash
   gunicorn -w 1 -b 0.0.0.0:5000 app:app
   ```
   - **Explanation**:
     - `-w 1`: Specifies the number of workers (1 worker in this case).
     - `-b 0.0.0.0:5000`: Binds the server to all IPs on port 5000.
     - `app:app`: Specifies the module (`app`) and the Flask app instance (`app`).

2. The server will start running at **port 5000**.

---

## Notes

- Replace `project_name` with your desired project folder name.
- Use `vim` to edit or create the respective files (you can replace it with another text editor if preferred).
- Ensure all required software packages are installed successfully before proceeding to the next step.

---

Follow these steps to set up your Flask application and start the server. Happy coding! 🎉
