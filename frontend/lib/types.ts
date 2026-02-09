// frontend/lib/types.ts
// Define the Task interface based on your backend model
export interface Task {
    id: number;
    title: string;
    description?: string; // Optional
    completed: boolean;
    owner_id: number; // For display, though not directly editable by frontend user
}
