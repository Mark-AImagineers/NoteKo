# 📝 NoteKo

**NoteKo** is my personal note-taking app — built as a sandbox to sharpen my full-stack dev skills while creating a tool that actually helps me think, remember, and grow.

This isn’t meant to be a commercial product (at least for now). It’s a personal system I’m building to level up my skills in:

- Frontend development with **React**
- Backend development with **FastAPI** and **Python**
- Containerization and deployment using **Docker**
- Working with both **structured (PostgreSQL)** and **unstructured (MongoDB)** data
- Exploring how to deploy it like a standard Windows app (EXE-style), or a portable local app
- Building a **mobile app** version for cross-device sync
- Hosting everything through a **home server setup**

The big picture: to create a digital companion that grows with me — something like Tony Stark’s personal tools, but practical, minimal, and mine.

---

## 🔧 Tech Stack (Planned)

- **Frontend**: React + JavaScript
- **Backend**: FastAPI + Python
- **Database (Structured)**: PostgreSQL
- **Database (Unstructured)**: MongoDB
- **Containerization**: Docker + Docker Compose
- **Mobile App**: Possibly React Native or Flutter
- **Sync & Hosting**: Self-hosted home server (future phase)

---

## 🚀 Future Trajectory

- Build local-only MVP, containerized via Docker
- Implement dual-database setup (Postgres + MongoDB)
- Add sync support across devices
- Build mobile app for on-the-go access
- Deploy and manage via home server
- Explore app bundling for desktop (EXE, AppImage, etc.)
- Long-term: experiment with AI features (summarization, Q&A, smart tagging)

---

## 📌 Changelog

### [0.3.0] - 2025-03-28
#### Added
- Authentication System:
  - JWT-based authentication with access and refresh tokens
  - User registration and login endpoints
  - Token refresh mechanism
  - Password hashing with bcrypt
  - Comprehensive test suite for auth endpoints
- Testing Infrastructure:
  - Test configuration with separate test schema
  - Reusable test fixtures in conftest.py
  - Authentication endpoint tests in test_auth.py

### [0.2.0] - 2025-03-28
#### Added
- Metadata Manager for dynamic configuration management
  - Centralized metadata storage in JSON format
  - Dynamic application information retrieval
- Enhanced startup banner
  - ASCII art logo
  - Real-time system status display
  - Live database connection monitoring
  - Dynamic middleware status checks
  - Environment and version information

### [0.1.0] - 2025-03-28
#### Added
- Frontend:
    - Set up React with Vite and Docker
    - Implemented basic login page UI using Chakra UI
    - Added routing with react-router-dom
- Backend:
    - Set up FastAPI with PostgreSQL and Docker
    - Configured SQLAlchemy ORM with async support
    - Created user model and database migrations
    - Set up pgAdmin for database management
- Infrastructure:
    - Docker Compose setup for both frontend and backend
    - Configured development environment with hot-reload
    - Set up proper CORS for frontend-backend communication

### [0.4.0] - YYYY-MM-DD
#### Planned
- Add PostgreSQL integration for structured notes
- Setup MongoDB for unstructured / freeform notes
- Create Docker Compose file for full stack

---

## ✅ Things To Do

- setup react frontend, login feature

---

## ⚙️ Work In Progress (WIP)

- auth endpoints
- jwt setup
- security utils

---

## 🧪 Tests

### Available Test Suites
1. Authentication Tests (`test_auth.py`)
   - User Registration (4 tests)
   - User Login (3 tests)
   - Token Management (3 tests)
   - User Info (3 tests)

### Running Tests
```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_auth.py::test_login_success
```

### Planned Test Suites
1. Notes CRUD Operations
2. Note Categories/Tags
3. Search Functionality
4. User Preferences
5. Data Export/Import
6. MongoDB Integration
7. API Rate Limiting
8. File Attachments

---

## 🧠 Developer's Journal

> A raw log of decisions, ideas, frustrations, and wins. Helps me track progress and thought processes.

- `[2025-03-28]`
    - I will start with the login feature, the idea is not a SaaS app but the user is able to create users. I will do this as well so i learn how to build a secure app.
    - react framework setup done, built a front end only login page
    - fastapi framework setup done, built a placeholder api
    - these are all running in docker

> This isn’t just an app — it’s my lab. My sandbox. My system. Built to grow with me.
