// frontend/app/page.tsx
'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, removeAuthToken } from '@/lib/auth';
import { getTasks } from '@/lib/api';
import { Task } from '@/lib/types';
import TaskList from '@/app/components/TaskList';
import TaskForm from '@/app/components/TaskForm';

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/auth/login');
    } else {
      fetchTasks();
    }
  }, [router]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const fetchedTasks = await getTasks();
      setTasks(fetchedTasks);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
      // If unauthorized, redirect to login
      if (err.message === 'No authentication token found.' || err.message === 'Could not validate credentials') {
        router.push('/auth/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    removeAuthToken();
    router.push('/auth/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-500">Error: {error}</p>
        <button onClick={handleLogout} className="ml-4 text-indigo-600 hover:text-indigo-900">
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-xl mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-extrabold text-gray-900">Your Tasks</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>

        <TaskForm onTaskCreated={fetchTasks} />

        <TaskList tasks={tasks} onTaskUpdated={fetchTasks} />
      </div>
    </div>
  );
}