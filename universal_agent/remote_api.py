from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import Database
from core.types import Task
import asyncio

app = Flask(__name__)
CORS(app)  # Enable CORS for remote access
db = Database()

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "name": "Nexus Remote API",
        "version": "1.0"
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_all_tasks()
    return jsonify([{
        "id": t.id,
        "description": t.description,
        "status": t.status.value,
        "result": t.result,
        "error": t.error,
        "created_at": t.created_at.isoformat()
    } for t in tasks])

@app.route('/api/submit', methods=['POST'])
def submit_task():
    data = request.json
    description = data.get('description')
    if description:
        task = Task(description=description)
        db.save_task(task)
        return jsonify({"status": "success", "id": task.id})
    return jsonify({"status": "error"}), 400

@app.route('/api/status', methods=['GET'])
def get_status():
    tasks = db.get_all_tasks()
    return jsonify({
        "total_tasks": len(tasks),
        "pending": len([t for t in tasks if t.status.value == "pending"]),
        "running": len([t for t in tasks if t.status.value == "running"]),
        "completed": len([t for t in tasks if t.status.value == "completed"]),
        "failed": len([t for t in tasks if t.status.value == "failed"])
    })

def run_remote_api(host='0.0.0.0', port=8080):
    """Run the remote API server"""
    print(f"[REMOTE API] Starting on http://{host}:{port}")
    print(f"[REMOTE API] Access from other devices at http://<your-ip>:{port}")
    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    run_remote_api()
