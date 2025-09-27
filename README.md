# 💬 Django Q&A / Social Media Platform

## 🌐 Project Overview

This project is a fully-featured **Question and Answer (Q&A)** or social discussion platform, built entirely using the robust **Django** framework. The core structure and user interactions are designed to resemble platforms like **Stack Overflow** or simplified social networks, focusing on user-generated content and discussions.

The primary objective of this project was to implement the **full backend logic** for a complete interactive system, ranging from user authentication to complex data modeling for linking posts and comments.

---

## ✨ Key Features

This application provides the fundamental features required for a community-driven platform:

* **Complete Authentication:** Full system for user registration, login, and session management (implemented in the `account` app).
* **Content Creation:** Users can create, publish, and manage **Posts or Questions**.
* **Social Interaction:** Functionality to add **Comments** under posts, facilitating discussion and feedback.
* **Modular Architecture:** Organized into separate Django apps (`account`, `home`) for clean code separation and scalability.
* **Server-Side Rendering (SSR):** Frontend presentation is handled through **Django Templates** (HTML/CSS).

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | **Django** | The core framework for server-side logic (Python). |
| **Language** | **Python** | Primary development language. |
| **Database** | **SQLite** (Default) | Simple, file-based database used for initial development and testing. |
| **Frontend** | **HTML / Django Templates** | Used for structuring and rendering the user interface. |

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

First, clone the repository and navigate into the project directory:

### 2. Install Dependencies

It's highly recommended to set up and activate a Virtual Environment first. Then, install the required packages listed in `requirements.txt`:

```bash
# Install dependencies
pip install -r requirements.txt
```
### 3. Database Setup

Apply database migrations to initialize the schema (including user and post tables):

```bash
python manage.py makemigrations
python manage.py migrate
```
### 4. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```
The application will be accessible in your web browser at http://127.0.0.1:8000/.

## 🔒 User & Admin Access

* **User Accounts:** Use the `/account/` URLs (e.g., `/account/signup/` or `/account/login/`) to access the sign-up and login pages.
* **Superuser Creation:** To access the **Django Admin Panel** (`http://127.0.0.1:8000/admin`), you must first create an administrative user:

```bash
python manage.py createsuperuser

```bash
git clone [https://github.com/Denesepro/django-social-media.git](https://github.com/Denesepro/django-social-media.git)
cd django-social-media
