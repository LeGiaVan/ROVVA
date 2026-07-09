# System Overview

**Project Name:** ROVVA Homestay Project
**Core Domain:** Hospitality & Booking Platform (Web Application)
**Primary Function:** A multi-role web platform (Customer, Host, Admin) for booking homestays and managing accommodations. The system handles user authentication, accommodation listings, booking workflows, dispute resolution, and promotional systems using a Server-Side Rendering (SSR) approach with Flask and Jinja2 templates.

---

# Technology Stack

| Category | Technology | Purpose & Context |
| :--- | :--- | :--- |
| **Language** | Python 3.x | Core backend execution environment. |
| **Web Framework** | Flask (>=3.0.0) | Handles HTTP routing, middleware, and request/response lifecycle. |
| **ORM & Database** | Flask-SQLAlchemy (>=3.1.0) | Object-Relational Mapping (ORM) layer abstracting SQL queries. |
| **Authentication** | Flask-Login (>=0.6.3) | Manages user sessions, authentication state, and role-based access. |
| **Storage (Dev)** | SQLite 3 | Relational database used for local development (`instance/rova_host.db`). |
| **Frontend** | HTML5, CSS3, Vanilla JS | User interface, styled with custom CSS (`frontend/static`). |
| **Templating** | Jinja2 | Server-side rendering engine used by Flask (`frontend/templates`). |

---

# Repository Structure

```text
d:\G.VAN\ROVA\
├── backend/                  # Core Python application logic
│   ├── app/                  # Application Factory and Modules
│   │   ├── config.py         # Environment-aware configuration (Dev/Prod)
│   │   ├── extensions.py     # Initialization of Flask extensions (db, login_manager)
│   │   ├── models/           # SQLAlchemy ORM models (Database schema definitions)
│   │   ├── routes/           # Routing controllers organized by Blueprints
│   │   │   ├── auth/         # Authentication and registration logic
│   │   │   ├── customer/     # Customer-facing views (search, booking, account)
│   │   │   └── host/         # Host-facing management dashboard (listings, disputes)
│   │   └── seed.py           # Database seeding logic for local development
│   └── __init__.py           # Flask Application Factory `create_app()`
├── frontend/                 # Presentation layer assets
│   ├── static/               # Static web assets (CSS, Images, Logos)
│   │   ├── customer/         # Customer-specific static files
│   │   ├── host/             # Host-specific static files
│   │   └── shared/           # Cross-role static assets
│   └── templates/            # Jinja2 HTML templates
│       ├── auth/             # Login & Registration pages
│       ├── customer/         # Customer interface templates (Home, Account, Trip)
│       └── host/             # Host dashboard templates (Accommodation, Booking)
├── instance/                 # Instance-specific data (e.g., SQLite DB file)
│   └── rova_host.db          # Development database
├── requirements.txt          # Python package dependencies
└── run.py                    # Application entry point (`if __name__ == '__main__': ...`)
```

---

# Core Components & Modules

### 1. Application Factory (`backend/app/__init__.py`)
- **Responsibility:** Implements the Flask application factory pattern. Instantiates the app, loads configurations from `config.py`, initializes extensions (`SQLAlchemy`, `Flask-Login`), and registers all routing Blueprints.
- **Dependencies:** Imports from `backend.app.config`, `backend.app.extensions`, and `backend.app.routes`.

### 2. Configuration Manager (`backend/app/config.py`)
- **Responsibility:** Defines `Config`, `DevelopmentConfig`, and `ProductionConfig`. Handles environment variable resolution for `SECRET_KEY` and `DATABASE_URL`. Maps the `frontend/templates` and `frontend/static` directories explicitly to bypass Flask's default file structure expectations.

### 3. ORM Models (`backend/app/models/`)
- **Responsibility:** Defines the relational database schema using declarative Python classes inheriting from `db.Model`.
- **Key Entities:** `User` (handles multi-role mapping via `Flask-Login`'s `UserMixin`), Accommodations, Bookings, Reviews, Payments, etc.

### 4. Routing Blueprints (`backend/app/routes/`)
- **`auth/` Blueprint:** Handles `/login`, `/register`, and `/logout`. Manages session cookies and password verification.
- **`customer/` Blueprint:** Handles endpoints for guests to view listings, make bookings, manage their profiles, and view trip history.
- **`host/` Blueprint:** Handles endpoints for property owners to manage their accommodations, view booking requests, handle disputes, and monitor revenue.

### 5. Frontend Templates (`frontend/templates/`)
- **Responsibility:** Defines the UI. Utilizes Jinja2 inheritance (`{% extends 'base.html' %}`) to maintain consistent layouts across `auth`, `customer`, and `host` domains.

---

# Data Flow & Architecture

### Request Lifecycle
1. **Ingestion:** An HTTP request hits the WSGI server (development server via `run.py`).
2. **Routing & Middleware:** The Flask router matches the URL to a specific Blueprint endpoint. Before execution, `Flask-Login` middleware checks session cookies to populate `current_user`.
3. **Controller Logic:** The route handler in `backend/app/routes/` executes. It may require specific roles (e.g., `@login_required`).
4. **Data Access:** If data retrieval or mutation is required, the controller queries the database using SQLAlchemy ORM (e.g., `User.query.filter_by(...)`).
5. **Rendering / Response:** The controller compiles the necessary context dictionary and passes it to `render_template()`. Jinja2 compiles the HTML and returns it to the client with a `200 OK` status code. [TODO: Outline any specific API endpoint JSON serialization flows if Single Page Application (SPA) features are added later].

---

# Deployment & Infrastructure

- **Containerization:** [TODO: Add Dockerfile and docker-compose.yml specifications when available for production].
- **Environment Variables:**
  - `SECRET_KEY`: Cryptographic key for session signing.
  - `DATABASE_URL`: Connection string for SQLAlchemy (defaults to local SQLite if unset).
- **Execution Strategy (Dev):** The system runs via Flask's built-in Werkzeug server (`python run.py` running on `localhost:5000`).
- **Scaling Context:** The application is currently stateful due to server-side session management. For horizontal scaling, sessions must be migrated to a distributed store (e.g., Redis) and the SQLite database must be replaced with a robust RDBMS (e.g., PostgreSQL or MySQL).

---

# Development & Contribution

### Local Setup Instructions

1. **Clone the repository and enter the directory:**
   ```bash
   cd d:\G.VAN\ROVA
   ```

2. **Initialize a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed the Database:**
   The application includes a custom CLI command to reset and seed the database with mock data for local testing.
   ```bash
   flask --app run seed
   ```

5. **Run the Application:**
   ```bash
   python run.py
   ```
   The server will bind to `http://127.0.0.0:5000` with hot-reloading enabled (debug mode).
