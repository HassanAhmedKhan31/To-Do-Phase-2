// frontend/app/components/TaskItem.tsx
'use client';

import React, { useState } from 'react';
import { FaTrash, FaCheckCircle, FaRegCircle, FaEdit, FaSave, FaTimes } from 'react-icons/fa';
import { toggleTaskCompletion, deleteTask, updateTask } from '@/lib/api';
import { Task } from '@/lib/types';

interface TaskItemProps {
  task: Task;
  onTaskUpdated: () => void; // Callback to refresh parent list
}

export default function TaskItem({ task, onTaskUpdated }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.title);
  const [editedDescription, setEditedDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleToggle = async () => {
    setLoading(true);
    setError('');
    try {
      await toggleTaskCompletion(task.id);
      onTaskUpdated();
    } catch (err: any) {
      setError(err.message || 'Failed to toggle task status');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    setLoading(true);
    setError('');
    try {
      await deleteTask(task.id);
      onTaskUpdated();
    } catch (err: any) {
      setError(err.message || 'Failed to delete task');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    setLoading(true);
    setError('');
    try {
      await updateTask(task.id, { title: editedTitle, description: editedDescription });
      setIsEditing(false);
      onTaskUpdated();
    } catch (err: any) {
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditedTitle(task.title);
    setEditedDescription(task.description || '');
    setError('');
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white shadow rounded-lg">
      <div className="flex items-center flex-grow">
        <button onClick={handleToggle} disabled={loading} className="mr-3 text-2xl p-1">
          {task.completed ? <FaCheckCircle className="text-green-500" /> : <FaRegCircle className="text-gray-400" />}
        </button>
        {isEditing ? (
          <div className="flex-grow space-y-1">
            <input
              type="text"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
              className="w-full text-lg font-medium border-b border-gray-300 focus:outline-none focus:border-indigo-500"
              disabled={loading}
            />
            <textarea
              value={editedDescription}
              onChange={(e) => setEditedDescription(e.target.value)}
              className="w-full text-sm text-gray-600 border-b border-gray-300 focus:outline-none focus:border-indigo-500"
              rows={1}
              disabled={loading}
            />
          </div>
        ) : (
          <div className="flex-grow">
            <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`text-sm text-gray-600 ${task.completed ? 'line-through' : ''}`}>
                {task.description}
              </p>
            )}
          </div>
        )}
        {error && <p className="text-red-500 text-sm ml-4">{error}</p>}
      </div>

      <div className="flex items-center space-x-2 ml-4">
        {isEditing ? (
          <>
            <button onClick={handleSaveEdit} disabled={loading} className="text-green-500 hover:text-green-700 p-1">
              <FaSave size={20} />
            </button>
            <button onClick={handleCancelEdit} disabled={loading} className="text-gray-500 hover:text-gray-700 p-1">
              <FaTimes size={20} />
            </button>
          </>
        ) : (
          <button onClick={() => setIsEditing(true)} disabled={loading} className="text-blue-500 hover:text-blue-700 p-1">
            <FaEdit size={20} />
          </button>
        )}
        <button onClick={handleDelete} disabled={loading} className="text-red-500 hover:text-red-700 p-1">
          <FaTrash size={20} />
        </button>
      </div>
    </div>
  );
}