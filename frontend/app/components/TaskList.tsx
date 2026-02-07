"use client";

import React, { useEffect, useState, useCallback } from "react";
import { fetchTasks, Task } from "@/lib/api";
import { TaskItem } from "./TaskItem";

export const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadTasks = useCallback(async () => {
    try {
      setLoading(true);
      const fetchedTasks = await fetchTasks();
      setTasks(fetchedTasks);
    } catch (err) {
      setError("Failed to fetch tasks. Please try again later.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const handleTaskToggle = useCallback((updatedTask: Task) => {
    setTasks((prevTasks) =>
      prevTasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
    );
  }, []);

  if (loading) {
    return <div className="text-center text-lg mt-8">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 text-lg mt-8">{error}</div>;
  }

  if (tasks.length === 0) {
    return <div className="text-center text-lg mt-8">No tasks found.</div>;
  }

  return (
    <div className="w-full max-w-md mx-auto bg-white dark:bg-zinc-800 shadow-md rounded-lg mt-8">
      <h2 className="text-2xl font-semibold p-4 border-b border-gray-200 dark:border-gray-700">My Tasks</h2>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <TaskItem task={task} onTaskToggle={handleTaskToggle} />
          </li>
        ))}
      </ul>
    </div>
  );
};
