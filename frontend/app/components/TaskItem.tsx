"use client";

import React, { useState } from "react";
import { Task, toggleTaskCompletion } from "@/lib/api";

interface TaskItemProps {
  task: Task;
  onTaskToggle: (updatedTask: Task) => void;
}

export const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskToggle }) => {
  const [isCompleted, setIsCompleted] = useState(task.completed);
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    if (isToggling) return;

    setIsToggling(true);
    // Optimistic update
    setIsCompleted(!isCompleted);

    try {
      const updatedTask = await toggleTaskCompletion(task.id);
      onTaskToggle(updatedTask); // Notify parent component of the actual update
    } catch (error) {
      console.error("Failed to toggle task completion:", error);
      // Revert optimistic update if API call fails
      setIsCompleted(isCompleted);
    } finally {
      setIsToggling(false);
    }
  };

  const taskClasses = `
    flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700
    ${isCompleted ? "line-through text-gray-500 dark:text-gray-400" : "text-black dark:text-white"}
  `;

  return (
    <div className={taskClasses}>
      <div className="flex items-center">
        <input
          type="checkbox"
          checked={isCompleted}
          onChange={handleToggle}
          className="mr-3 h-5 w-5 cursor-pointer accent-blue-500"
          disabled={isToggling}
        />
        <span className="text-lg">{task.title}</span>
      </div>
      {task.description && (
        <span className="text-sm text-gray-400 dark:text-gray-500">
          {task.description}
        </span>
      )}
    </div>
  );
};
