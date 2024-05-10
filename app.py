from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__,template_folder='build')
app.config['SECRET_KEY'] = 'pestoTask'

DB_PATH = 'tasks.db'


def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, start_date DATE, end_date DATE, status TEXT)''')
    conn.commit()
    conn.close()


def add_task(title, description, start_date, end_date, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
              (title, description, start_date, end_date, status))
    conn.commit()
    conn.close()


def get_tasks(status=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


def update_task(task_id, title, description, start_date, end_date, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, start_date=?, end_date=?, status=? WHERE id=?",
              (title, description, start_date, end_date, status, task_id))
    conn.commit()
    conn.close()


def get_task_by_id(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task


def get_task_statuses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT status FROM tasks")
    statuses = [row[0] for row in c.fetchall()]
    conn.close()
    return statuses


def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


host = os.getenv("SCHEDULER_HOST", "127.0.0.1")
port = os.getenv("SCHEDULER_PORT", 5000)
debug = os.getenv("SCHEDULER_DEBUG", "True").lower() == "true"

try:
    port = int(port)
except ValueError:
    print("Error: Unable to parse SCHEDULER_PORT environment variable")

try:
    debug = bool(debug)
except ValueError:
    print("Error: Unable to parse SCHEDULER_DEBUG environment variable")

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug)
