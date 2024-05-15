from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pestoTask'  # Secret key for session management

DB_PATH = 'tasks.db'  # Path to SQLite database file


def create_table():
    """Create a tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, start_date DATE, end_date DATE, status TEXT)''')
    conn.commit()
    conn.close()


def add_task(title, description, start_date, end_date, status):
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
              (title, description, start_date, end_date, status))
    conn.commit()
    conn.close()


def get_tasks(status=None):
    """Retrieve tasks from the database, optionally filtered by status."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


# Similar functions for update_task, get_task_by_id, get_task_statuses, delete_task


@app.route('/')
def index():
    """Homepage route, displays all tasks."""
    if not os.path.exists(DB_PATH):
        create_table()
    return render_template('index.html', tasks=get_tasks(), statuses=get_task_statuses(), edit_task=None)


@app.route('/filter', methods=['GET', 'POST'])
def filter_tasks():
    """Filter tasks by status."""
    if request.method == 'POST':
        status = request.form['status']
        if status == 'All':
            return redirect(url_for('index'))
        return render_template('index.html', tasks=get_tasks(status), statuses=get_task_statuses(), edit_task=None)
    else:
        return redirect(url_for('index'))


@app.route('/add_task', methods=['POST'])
def add():
    """Add a new task."""
    title = request.form['title']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form['status']
    add_task(title, description, start_date, end_date, status)
    flash('Task added successfully', 'success')
    return redirect(url_for('index'))


# Similar routes for editing and deleting tasks

if __name__ == '__main__':
    # Get host, port, and debug mode from environment variables or use defaults
    host = os.getenv("SCHEDULER_HOST", "127.0.0.1")
    port = os.getenv("SCHEDULER_PORT", 8080)
    debug = os.getenv("SCHEDULER_DEBUG", "True").lower() == "true"
    try:
        port = int(port)
    except ValueError:
        print("Error: Unable to parse SCHEDULER_PORT environment variable")

    try:
        debug = bool(debug)
    except ValueError:
        print("Error: Unable to parse SCHEDULER_DEBUG environment variable")
    
    # Start the Flask app
    app.run(host=host, port=port, debug=debug)
