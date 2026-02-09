# UI Components Specification

This document outlines the key UI components for the Next.js frontend.

## `TaskItem` Component

-   **Purpose:** Displays a single task item with its title, description, and status. Provides actions to interact with the task.
-   **Location:** `frontend/app/components/TaskItem.tsx`
-   **Props:**
    *   `task`: (`Task` object from `lib/types.ts`) - The task data to display.
    *   `onTaskUpdated`: (`() => void`) - Callback function to notify the parent component (e.g., `TaskList`) to refresh its data after a task modification.
-   **State:** Manages editing mode (`isEditing`), edited task details (`editedTitle`, `editedDescription`), loading state (`loading`), and any local errors (`error`).
-   **Interactions:**
    *   **Toggle Completion:** Clicking the checkbox/icon toggles the task's `completed` status via `toggleTaskCompletion` API call.
    *   **Edit Task:** An edit button (`FaEdit`) switches the component into editing mode, allowing `title` and `description` to be modified.
    *   **Save Edit:** A save button (`FaSave`) sends updated `title` and `description` to the backend via `updateTask` API call.
    *   **Cancel Edit:** A cancel button (`FaTimes`) discards changes and exits editing mode.
    *   **Delete Task:** A trash icon (`FaTrash`) deletes the task via `deleteTask` API call (with confirmation).

## `TaskList` Component

-   **Purpose:** Displays a collection of `TaskItem` components.
-   **Location:** `frontend/app/components/TaskList.tsx`
-   **Props:**
    *   `tasks`: (`Task[]`) - An array of task objects to display.
    *   `onTaskUpdated`: (`() => void`) - Callback function passed down to `TaskItem` components, which in turn calls the parent to refresh the list.
-   **State:** None (stateless, renders provided tasks).
-   **Interactions:** Renders `TaskItem` for each task. Displays a message if no tasks are present.

## `TaskForm` Component

-   **Purpose:** Provides a form for users to add new tasks.
-   **Location:** `frontend/app/components/TaskForm.tsx`
-   **Props:**
    *   `onTaskCreated`: (`() => void`) - Callback function to notify the parent component (e.g., Dashboard) to refresh the task list after a new task is successfully created.
-   **State:** Manages input fields (`title`, `description`), loading state (`loading`), and any local errors (`error`).
-   **Interactions:** Input fields for `title` and `description`. A submit button creates a new task via `createTask` API call.

## Global Layout Component

-   **Purpose:** Defines the overall page structure for authenticated users, including header, navigation (if any), main content area, and logout functionality.
-   **Location:** `frontend/app/layout.tsx` (main layout)
-   **Props:** `children` (React nodes).
-   **State:** None.
-   **Interactions:** N/A (this is the root layout).

## Auth Layout Component

-   **Purpose:** Provides a specific layout for authentication-related pages (login, signup), typically centered content without global navigation.
-   **Location:** `frontend/app/auth/layout.tsx`
-   **Props:** `children` (React nodes).
-   **State:** None.
-   **Interactions:** N/A.

## `Login` Page

-   **Purpose:** Renders the login form and handles authentication flow.
-   **Location:** `frontend/app/auth/login/page.tsx`
-   **Props:** None.
-   **State:** Manages email, password input, error messages, and redirects.
-   **Interactions:** Calls `loginWithBetterAuth` from `lib/auth.ts`. Redirects on success/failure.

## `Signup` Page

-   **Purpose:** Renders the signup form and handles user registration flow.
-   **Location:** `frontend/app/auth/signup/page.tsx`
-   **Props:** None.
-   **State:** Manages email, password input, error messages, and redirects.
-   **Interactions:** Calls `signupWithBetterAuth` from `lib/auth.ts`. Redirects on success/failure.