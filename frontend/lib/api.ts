// frontend/lib/api.ts
import { getAuthToken } from './auth';
import { Task } from '@/lib/types';

const API_BASE_URL = '/api'; // Assumes /api rewrites to backend

export const fetchApi = async (
    endpoint: string,
    method: string = 'GET',
    body: any = null,
    includeAuth: boolean = true
) => {
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
    };

    if (includeAuth) {
        const token = getAuthToken();
        if (!token) {
            // In a real app, you might redirect to login or throw a specific error
            throw new Error('No authentication token found.');
        }
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
        method,
        headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 204) { // No Content
        return null;
    }

    const data = await response.json();

    if (!response.ok) {
        const errorMessage = data.detail || 'Something went wrong';
        throw new Error(errorMessage);
    }

    return data;
};

// Task-specific API calls
export const getTasks = () => fetchApi('/tasks/');
export const createTask = (task: Partial<Task>) => fetchApi('/tasks/', 'POST', task);
export const updateTask = (id: number, task: Partial<Task>) => fetchApi(`/tasks/${id}`, 'PUT', task);
export const toggleTaskCompletion = (id: number) => fetchApi(`/tasks/${id}/toggle`, 'PATCH');
export const deleteTask = (id: number) => fetchApi(`/tasks/${id}`, 'DELETE');
