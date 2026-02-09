# UI Pages Specification

This document outlines the main pages/routes for the Next.js frontend application using the App Router.

## `/` (Homepage/Dashboard)

-   **Purpose:** Displays the main dashboard with the current user's task list and a form to add new tasks. It acts as the primary authenticated view.
-   **Components:** `TaskList`, `TaskForm`, `TaskItem`, Global Layout.
-   **Data:** Fetches tasks from the backend API (`GET /api/tasks`).
-   **Interactions:** Adds new tasks, views existing tasks, toggles task completion, edits task details, deletes tasks, and handles user logout.
-   **Authentication:** Requires authentication; redirects to `/auth/login` if not authenticated.

## `/auth/login`

-   **Purpose:** Allows users to log in to the application using Better Auth.
-   **Components:** Login form, Auth Layout.
-   **Data:** Sends credentials to a simulated Better Auth endpoint, receives JWT.
-   **Interactions:** Input fields for email and password, submit button, link to signup. Redirects to `/` on successful login.

## `/auth/signup`

-   **Purpose:** Allows new users to create an account using Better Auth.
-   **Components:** Signup form, Auth Layout.
-   **Data:** Sends user details to a simulated Better Auth endpoint, receives JWT.
-   **Interactions:** Input fields for email and password, submit button, link to login. Redirects to `/` on successful signup.