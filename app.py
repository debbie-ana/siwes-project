from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the tasks table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            assignee TEXT NOT NULL,
            deadline DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home page: display all tasks
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add new task
@app.route('/add_task', methods=('GET', 'POST'))
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        assignee = request.form['assignee']
        deadline = request.form['deadline']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (title, description, status, assignee, deadline) VALUES (?, ?, ?, ?, ?)',
                     (title, description, status, assignee, deadline))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add_task.html')

# Mark task as completed (status update)
@app.route('/complete_task/<int:id>', methods=('POST',))
def complete_task(id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET status = "Completed" WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
