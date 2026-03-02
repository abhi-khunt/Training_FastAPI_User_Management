# FastAPI User Management System

A complete **User Management System** built using FastAPI with session-based JWT authentication, role-based authorization, task management, profile management, and admin control panel.

---

# Overview

This system provides:

- User Registration and Login
- Session-based Authentication using JWT stored in server session
- Role-based Authorization (User, Sub-Admin, Admin)
- Task Management System
- Profile Management
- Admin Dashboard
- Secure HttpOnly Cookie-based Session Handling

---

# Technology Stack

## Backend

- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Pydantic
- JWT
- Session Middleware

## Frontend

- HTML
- Bootstrap 5
- JavaScript (Fetch API)
- Jinja2 Templates

---
## 📁 Project Structure
```
│
├── app/
│ │
│ ├── core/
│ │ ├── config.py
│ │ ├── auth.py
│ │
│ ├── database/
│ │ ├── connection.py
│ │
│ ├── models/
│ │ ├── user.py
│ │ ├── task.py
│ │ 
│ │
│ ├── schemas/
│ │ ├── user.py
│ │ ├── task.py
│ │ 
│ ├── routes/
│ │ ├── user.py
│ │ ├── admin.py
│ │ 
│ ├── templates/
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── dashboard.html
│ │ ├── admin_dashboard.html
│ │ └── profile.html
│ │
│ └── main.py
│
├── .env
├── requirements.txt
└── README.md  
```
---

# System Architecture Flow

User opens website  
↓  
User registers or logs in  
↓  
Server validates credentials  
↓  
JWT token created  
↓  
JWT stored in server session  
↓  
Session ID stored in HttpOnly cookie  
↓  
Cookie automatically sent with every request  
↓  
Server validates session  
↓  
Access granted  

---

# Authentication Flow

Login Request  
↓  
Validate Email and Password  
↓  
Generate JWT Token  
↓  
Store JWT in Session  
↓  
Return Session Cookie  
↓  
User Authenticated  

---

# Authorization Flow

Request received  
↓  
Session checked  
↓  
JWT extracted from session  
↓  
JWT verified  
↓  
Role checked  
↓  
Access granted or denied  

---

# User Roles

| Role | Permissions |
|------|-------------|
| User | Manage own profile and tasks |
| Sub-Admin | Elevated privileges |
| Admin | Manage users, promote users, delete users |

---

# Database Models

## User

Fields:

- id
- first_name
- last_name
- email
- phone_number
- password (hashed)
- role
- created_at

---

## Task

Fields:

- id
- title
- description
- owner_id
- created_at

---

## Session

Stores:

- JWT Token
---

# Pydantic Models

## Register Model

- first_name
- last_name
- email
- phone_number
- password
- confirm_password

## Login Model

- email
- password

## Profile Update Model

- first_name
- last_name

## Task Model

- title
- description

---

# API Structure

Base Prefix:


---

# Authentication Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | /api/users/register | Register new user | Public |
| POST | /api/users/login | Login user | Public |
| DELETE | /api/users/logout | Logout user | Authenticated |

---

# Profile Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | /api/users/profile | Get profile | Authenticated |
| PUT | /api/users/profile | Update profile | Authenticated |

---

# Task Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | /api/users/tasks | Create task | Authenticated |
| GET | /api/users/tasks | Get tasks | Authenticated |
| PUT | /api/users/tasks/{task_id} | Update task | Authenticated |
| DELETE | /api/users/tasks/{task_id} | Delete task | Authenticated |

---

# Admin Routes

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | /api/users/admin/users | List users | Admin |
| PUT | /api/users/admin/users/{user_id}/promote | Promote user | Admin |
| DELETE | /api/users/admin/users/{user_id} | Delete user | Admin |

---

# Frontend Pages

| Page | Description |
|------|-------------|
| /register | Registration page |
| /login | Login page |
| /dashboard | User dashboard |
| /profile | Profile page |
| /admin-dashboard | Admin dashboard |

---

# Dashboard Flow

User opens dashboard  
↓  
Session validated  
↓  
Tasks fetched from backend  
↓  
Tasks displayed  
↓  
User can create, edit, delete tasks  

---

# Profile Flow

User opens profile page  
↓  
Fetch profile data  
↓  
Display user info  
↓  
User edits profile  
↓  
Save request sent  
↓  
Database updated  

---

# Admin Flow

Admin opens dashboard  
↓  
Fetch users  
↓  
Display users  
↓  
Promote user OR Delete user  

---

# Session Flow

Login successful  
↓  
JWT stored in session  
↓  
Session ID stored in HttpOnly cookie  
↓  
Cookie sent automatically  
↓  
Server verifies session  


---

# Security Features

- Password Hashing
- JWT Authentication
- Session-based Authentication
- HttpOnly Cookies
- Role-based Authorization
- Protected Routes
- Input Validation

---

# Complete Flow

User registers  
↓  
User logs in  
↓  
Session created  
↓  
User accesses dashboard  
↓  
User manages tasks  
↓  
User manages profile  
↓  
Admin manages users  

---

# Author

Abhi Khunt  

GitHub:  
https://github.com/abhi-khunt/Training_FastAPI_User_Management/
