import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify
from core.database import Database
from core.types import Task

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks')
def get_tasks():
    tasks = db.get_all_tasks()
    # Convert tasks to dict for JSON serialization
    return jsonify([{
        "id": t.id,
        "description": t.description,
        "status": t.status.value,
        "result": t.result,
        "error": t.error
    } for t in tasks])

@app.route('/api/submit', methods=['POST'])
def submit_task():
    from flask import request
    data = request.json
    description = data.get('description')
    if description:
        # In a real app, we would push this to the Orchestrator
        # For now, we just save it to DB as pending
        from core.types import Task
        task = Task(description=description)
        db.save_task(task)
        return jsonify({"status": "success", "id": task.id})
    return jsonify({"status": "error"}), 400

def run_dashboard():
    app.run(port=5000)

if __name__ == "__main__":
    run_dashboard()
