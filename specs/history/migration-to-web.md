# Migration from CLI to Web Application

This document records the migration of the project from a command-line interface (CLI) application to a full-stack web application.

## Key Changes:

- **Architecture:** The project was restructured into a monorepo with a Next.js frontend and a FastAPI backend.
- **Database:** The database was migrated from a local SQLite database to a cloud-native Neon PostgreSQL database.
- **API:** The backend was converted from a CLI application to a RESTful API with secure endpoints for managing tasks.
- **Authentication:** JWT-based authentication was implemented to secure the API endpoints.
- **Frontend:** A new Next.js frontend was created to provide a user-friendly web interface for interacting with the application.
