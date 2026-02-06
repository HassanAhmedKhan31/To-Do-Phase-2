# T-101: Test for adding a task.
import pytest
from task_manager import TaskManager

@pytest.fixture
def manager():
    """Provides a TaskManager instance for each test."""
    return TaskManager()

def test_add_task(manager: TaskManager):
    """
    Tests that a task can be added successfully.
    """
    title = "Test Task"
    description = "A description for the test task."
    
    # Add the task
    task = manager.add_task(title, description)
    
    # Assertions
    assert task is not None
    assert task['title'] == title
    assert task['description'] == description
    assert task['completed'] is False
    assert task['id'] == 1
    
    # Verify it's in the list
    all_tasks = manager.view_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0] == task

def test_update_task(manager: TaskManager):
    """
    T-103: Tests that a task can be updated successfully.
    """
    # Add a task first
    manager.add_task("Original Title", "Original Description")
    
    # Update the task
    new_title = "Updated Title"
    new_description = "Updated Description"
    updated_task = manager.update_task(1, new_title, new_description)
    
    # Assertions for the updated task
    assert updated_task is not None
    assert updated_task['title'] == new_title
    assert updated_task['description'] == new_description
    
    # Verify the task in the list is updated
    all_tasks = manager.view_tasks()
    assert all_tasks[0]['title'] == new_title
    
    # Test updating a non-existent task
    non_existent_task = manager.update_task(99, "No Title")
    assert non_existent_task is None

def test_toggle_complete_task(manager: TaskManager):
    """
    T-104: Tests that a task's completion status can be toggled.
    """
    # Add a task first
    task = manager.add_task("Test Toggle")
    assert task['completed'] is False
    
    # Toggle to True
    toggled_task = manager.toggle_complete_task(1)
    assert toggled_task is not None
    assert toggled_task['completed'] is True
    
    # Toggle back to False
    toggled_task_again = manager.toggle_complete_task(1)
    assert toggled_task_again is not None
    assert toggled_task_again['completed'] is False
    
    # Test toggling a non-existent task
    non_existent_task = manager.toggle_complete_task(99)
    assert non_existent_task is None

def test_delete_task(manager: TaskManager):
    """
    T-105: Tests that a task can be deleted successfully.
    """
    # Add a task first
    manager.add_task("To Be Deleted")
    
    # Delete the task
    result = manager.delete_task(1)
    assert result is True
    
    # Verify the task is gone
    all_tasks = manager.view_tasks()
    assert len(all_tasks) == 0
    
    # Test deleting a non-existent task
    non_existent_result = manager.delete_task(99)
    assert non_existent_result is False
