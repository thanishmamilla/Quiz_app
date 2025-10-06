# 🎓 Full-Stack Quiz Application

This is a complete, authenticated, and multi-quiz application built using a modern full-stack architecture. Users can log in, select from a list of available quizzes, track their answers with a timer, submit their scores, and review their past results. Administrators have special access to an Admin Panel for creating and adding new quizzes to the database.

## ✨ Core Features

* **User Authentication:** Secure login/registration with separate roles (`user` and `admin`).
* **Role-Based Access Control (RBAC):** Only administrators can access the "Add Quiz" dashboard via JWT token verification.
* **Multi-Quiz Support:** Backend manages quizzes via separate database tables.
* **Result Persistence:** Stores user scores in local storage, allowing logged-in users to see **"View Results"** instead of "Start Quiz" if they've already completed it.
* **Timer (Bonus):** Quizzes include a countdown timer that forces submission upon reaching zero.
* **Detailed Scoring:** The results page displays the user's score and provides per-question feedback.
* **Modern UI:** Quiz selection is presented using side-by-side cards.

---

## 💻 Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **React** (CRA, Hooks, Context API) | Handles UI, routing, state management, and interaction. |
| **Backend** | **Flask** (Python) | Lightweight API server for handling business logic. |
| **Database** | **SQLite** | Simple, file-based database for persistent storage. |
| **Auth** | **Flask-JWT-Extended** | Secure, token-based authentication. |

---

## 🚀 Setup and Installation

Follow these steps to get the application running locally.

### 2. Backend Setup (Flask)

1.  Navigate into the `backend` directory.
    ```bash
    cd backend
    ```
2.  Install Python dependencies:
    ```bash
    pip install Flask Flask-CORS Flask-JWT-Extended werkzeug
    ```
3.  Run the Flask application:
    ```bash
    python app.py
    ```
    The server should start on **`http://localhost:5000`**. The `quiz.db` file will be created and populated with default users/quizzes.

### 3. Frontend Setup (React)

1.  Navigate into the `frontend` directory.
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the React development server:
    ```bash
    npm start
    ```
    The client should open automatically, usually on **`http://localhost:3000`**.

---

## 🔑 Default Credentials

The backend automatically creates these users for testing:

| Role | Username | Password | Access |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `adminpass` | Full access, including **Admin Dashboard** for adding quizzes. |
| **User** | `testuser` | `userpass` | Quiz access and score tracking. |

### 1. Project Structure

Ensure your file structure separates the backend and frontend components:
