// frontend/app/components/TaskList.tsx
'use client';

import React from 'react';
import TaskItem from './TaskItem';
import { Task } from '@/lib/types';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void; // Callback to refresh parent list
}

export default function TaskList({ tasks, onTaskUpdated }: TaskListProps) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No tasks yet! Add one above.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} onTaskUpdated={onTaskUpdated} />
      ))}
    </div>
  );
}