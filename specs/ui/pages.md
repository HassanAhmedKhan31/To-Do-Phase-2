# UI Pages Specification

This document outlines the main pages/routes for the Next.js frontend application using the App Router.

## `/` (Homepage/Task List)

-   **Purpose:** Displays the main list of tasks for the authenticated user.
-   **Components:** `TaskList`, `Task`, `Layout`.
-   **Data:** Fetches tasks from the backend API.
-   **Interactions:** Add new tasks, view existing tasks, mark tasks as complete/pending, edit tasks, delete tasks.

## `/login`

-   **Purpose:** Allows users to log in to the application.
-   **Components:** Login form.
-   **Data:** Sends credentials to the backend `/token` endpoint.
-   **Interactions:** Input fields for email and password, submit button.

## `/register`

-   **Purpose:** Allows new users to create an account.
-   **Components:** Registration form.
-   **Data:** Sends user details to the backend `/register` endpoint.
-   **Interactions:** Input fields for email and password, submit button.
