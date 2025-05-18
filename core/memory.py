'''
Purpose: Local memory manager for todos, project state, and logs.

Responsibilities:
- Persist and retrieve todos
- Log interactions
- Store project state

Spec:
- save_todo(item: dict)
- get_todos() -> list[dict]
- mark_complete(index: int)
- save_log(entry: str)
'''

import yaml
from pathlib import Path

class MemoryManager:
    def __init__(self, base_path: Path = Path(".")):
        self.memory_dir = base_path / ".coductor"
        self.todo_path = self.memory_dir / "todo.yml"
        self.memory_path = self.memory_dir / "memory.yml"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Ensure files exist, else crete them with default values
        for path in [self.todo_path, self.memory_path]:
            if not path.exists():
                path.write_text(yaml.dump([] if "todo" in str(path) else {}))

    def load_todos(self):
        with open(self.todo_path, 'r') as f:
            return yaml.safe_load(f) or []

    def save_todos(self, todos):
        with open(self.todo_path, 'w') as f:
            yaml.safe_dump(todos, f)

    def add_todo(self, task: str, status: str = "pending"):
        todos = self.load_todos()
        todos.append({"task": task, "status": status})
        self.save_todos(todos)

    def update_todo_status(self, task: str, status: str):
        todos = self.load_todos()
        for t in todos:
            if t["task"] == task:
                t["status"] = status
        self.save_todos(todos)

    def load_memory(self):
        with open(self.memory_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def save_memory(self, memory_data: dict):
        with open(self.memory_path, 'w') as f:
            yaml.safe_dump(memory_data, f)

    def update_memory(self, key: str, value):
        memory = self.load_memory()
        memory[key] = value
        self.save_memory(memory)
