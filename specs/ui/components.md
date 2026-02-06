# UI Components Specification

This document outlines the key UI components for the Next.js frontend.

## Task Component

-   **Purpose:** Displays a single task item.
-   **Props:** `task` (Task object), `onToggleComplete`, `onEdit`, `onDelete`.
-   **States:** `editing` (boolean, for inline editing).
-   **Interactions:** Checkbox for completion, edit button, delete button.

## Task List Component

-   **Purpose:** Displays a collection of Task components.
-   **Props:** `tasks` (array of Task objects), `onAddTask`, `onTaskUpdate`, `onTaskDelete`.
-   **States:** `filter` (e.g., 'all', 'completed', 'pending').
-   **Interactions:** Filtering options, sorting options.

## Layout Component

-   **Purpose:** Defines the overall page structure, including header, navigation, and main content area.
-   **Props:** `children` (React nodes).
-   **States:** None.
-   **Interactions:** User authentication status display, logout button.
