import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import Config
from .types import Task, TaskStatus

class Database:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        
        # Tasks Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT,
                priority INTEGER,
                status TEXT,
                created_at TEXT,
                result TEXT,
                error TEXT,
                metadata TEXT
            )
        ''')
        
        # Knowledge Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id TEXT PRIMARY KEY,
                data TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_task(self, task: Task):
        conn = self._get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tasks (id, description, priority, status, created_at, result, error, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.description,
            task.priority,
            task.status.value,
            task.created_at.isoformat(),
            str(task.result) if task.result else None,
            task.error,
            json.dumps(task.metadata)
        ))
        
        conn.commit()
        conn.close()

    def get_task(self, task_id: str) -> Optional[Task]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Task(
                id=row[0],
                description=row[1],
                priority=row[2],
                status=TaskStatus(row[3]),
                created_at=datetime.fromisoformat(row[4]),
                result=row[5],
                error=row[6],
                metadata=json.loads(row[7])
            )
        return None

    def get_all_tasks(self) -> List[Task]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            tasks.append(Task(
                id=row[0],
                description=row[1],
                priority=row[2],
                status=TaskStatus(row[3]),
                created_at=datetime.fromisoformat(row[4]),
                result=row[5],
                error=row[6],
                metadata=json.loads(row[7])
            ))
        return tasks

    def save_knowledge(self, node_id: str, data: Dict[str, Any]):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge (id, data, updated_at)
            VALUES (?, ?, ?)
        ''', (node_id, json.dumps(data), datetime.now().isoformat()))
        conn.commit()
        conn.close()
