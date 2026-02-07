const API_BASE_URL = "http://127.0.0.1:8000"; // Assuming backend runs on port 8000

export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: number;
}

// Function to get a dummy token for now. In a real app, this would come from authentication.
const getAuthToken = (): string => {
  // In a real application, this would come from a secure authentication flow.
  if (typeof window !== "undefined") {
    // 1. Check localStorage
    const localStorageToken = localStorage.getItem("auth_token");
    if (localStorageToken) return localStorageToken;

    // 2. Check for the specific cookie
    const cookieToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("better-auth.session_token="))
      ?.split("=")[1];
    if (cookieToken) return cookieToken;
  }

  // 3. Fallback to placeholder
  return "YOUR_AUTH_TOKEN";
};

export const fetchTasks = async (): Promise<Task[]> => {
  const response = await fetch(`${API_BASE_URL}/api/tasks/`, {
    headers: {
      Authorization: `Bearer ${getAuthToken()}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch tasks");
  }
  return response.json();
};

export const toggleTaskCompletion = async (taskId: number): Promise<Task> => {
  const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/toggle`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getAuthToken()}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to toggle task completion");
  }
  return response.json();
};