# T-101 to T-105: Core business logic for all tasks.
from typing import List, Optional
from models import Task

class TaskManager:
    """Manages the lifecycle of tasks."""
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """T-101: Adds a new task."""
        new_task: Task = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "completed": False
        }
        self._tasks.append(new_task)
        self._next_id += 1
        return new_task

    def view_tasks(self) -> List[Task]:
        """T-102: Retrieves all tasks."""
        return self._tasks

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """T-103: Updates a task's title or description."""
        for task in self._tasks:
            if task["id"] == task_id:
                if title is not None:
                    task["title"] = title
                if description is not None:
                    task["description"] = description
                return task
        return None

    def toggle_complete_task(self, task_id: int) -> Optional[Task]:
        """T-104: Toggles the completion status of a task."""
        for task in self._tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        """T-105: Deletes a task by its ID."""
        task_to_delete = None
        for task in self._tasks:
            if task["id"] == task_id:
                task_to_delete = task
                break
        if task_to_delete:
            self._tasks.remove(task_to_delete)
            return True
        return False
