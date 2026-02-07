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

# Example of Trinity Reasoning Loop Integration
import os
import openai

def get_ai_suggestion_with_reasoning(prompt: str):
    """
    Demonstrates a two-turn conversation with the Trinity model to get a suggestion
    and follow up on its reasoning.
    """
    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="sk-or-v1-defe4cdd3..." # Replace with your actual key or load from env
    )

    # --- First Turn: Initial request with reasoning enabled ---
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    completion = client.chat.completions.create(
        model="arcee-ai/trinity-large-preview:free",
        messages=messages,
        extra_body={"reasoning": {"enabled": True}}
    )

    first_response = completion.choices[0].message
    reasoning_details = completion.choices[0].reasoning_details
    
    print("--- AI's Initial Response ---")
    print(first_response.content)
    print("\n--- Reasoning Details Captured ---")
    print(reasoning_details)

    # --- Second Turn: Follow-up question, passing back reasoning_details ---
    messages.append(first_response) # Add AI's first response to history
    messages.append({
        "role": "user",
        "content": "Can you elaborate on your reasoning for that suggestion?"
    })

    follow_up_completion = client.chat.completions.create(
        model="arcee-ai/trinity-large-preview:free",
        messages=messages,
        extra_body={"reasoning": {
            "enabled": True,
            "details": reasoning_details # Pass back the captured details
        }}
    )

    second_response = follow_up_completion.choices[0].message
    
    print("\n--- AI's Follow-up Response (Elaborating on Reasoning) ---")
    print(second_response.content)
    
    return first_response.content, second_response.content

# Example usage:
# if __name__ == "__main__":
#     initial_prompt = "Give me a creative name for a new task management app."
#     get_ai_suggestion_with_reasoning(initial_prompt)