<div align="center">

#  Expense Tracker — Personal Finance Dashboard

**A full-stack expense management system built with Streamlit, FastAPI, and MySQL**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Postman](https://img.shields.io/badge/Postman-API%20Tested-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://postman.com)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Running the App](#running-the-app)
- [API Reference](#-api-reference)
- [Postman Testing](#-postman-testing)
- [Running Tests](#-running-tests)
- [Contributing](#-contributing)

---

## 🌟 Overview

**Expense Tracker** is a full-stack personal finance dashboard that helps you log, categorize, and visualize your daily expenses. It features a clean **Streamlit** frontend for interactive data visualization and a robust **FastAPI** backend connected to a **MySQL** database — all testable via **Postman**.

---

## ✨ Features

- 📊 **Interactive Dashboard** — Visualize spending trends with charts and summaries
- ➕ **Add / Update Expenses** — Log and edit expense entries easily
- 🗂️ **Analytics by Category** — Break down spending across categories
- 📅 **Analytics by Month** — Track how your spending changes over time
- 🔌 **RESTful API** — Clean FastAPI backend with auto-generated Swagger docs
- 🗄️ **MySQL Database** — Persistent storage with a structured SQL schema
- 🧪 **Postman Ready** — All endpoints tested and documented

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Frontend     | Streamlit 1.35                    |
| Backend      | FastAPI 0.112 + Uvicorn 0.30      |
| Database     | MySQL 8.0                         |
| Data Layer   | Pydantic 1.10 + Pandas 2.0        |
| DB Driver    | mysql-connector-python 8.0        |
| HTTP Client  | Requests 2.31                     |
| Testing      | Pytest 8.3 + Postman              |

---

## 📁 Project Structure

```
Expense-Tracker-Personal-Finance-Dashboard/
│
├── frontend/
│   ├── app.py                      # Main Streamlit app — dashboard entry point
│   ├── add_update.py               # UI for adding and updating expenses
│   ├── analytics_by_category.py    # Category-wise spending analytics
│   └── analytics_by_months.py      # Month-wise spending analytics
│
├── backend/
│   ├── server.py                   # FastAPI app — all API routes and handlers
│   ├── db_helper.py                # MySQL queries and database operations
│   └── logging_setup.py            # Logging configuration
│
├── database/
│   └── expense_db_creation.sql     # SQL script to create the database and tables
│
├── tests/
│   ├── conftest.py                 # Shared Pytest fixtures
│   └── backend/
│       └── test_db_helper.py       # Unit tests for database helper functions
│
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9 or higher
- MySQL Server 8.0
- pip (Python package manager)
- Postman *(optional, for API testing)*

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/godwin-stanes/Expense-Tracker-Personal-Finance-Dashboard.git
cd Expense-Tracker-Personal-Finance-Dashboard
```

**2. Create and activate a virtual environment** *(recommended)*

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

### Database Setup

**1. Start your MySQL server and log in**

```bash
mysql -u root -p
```

**2. Run the SQL creation script**

```bash
mysql -u root -p < database/expense_db_creation.sql
```

> This will create the database and all required tables automatically.

**3. Update your database credentials in `backend/db_helper.py`**

```python
DB_CONFIG = {
    "host":     "localhost",
    "user":     "your_mysql_username",
    "password": "your_mysql_password",
    "database": "expense_tracker"
}
```

---

### Running the App

**1. Start the FastAPI backend server**

```bash
uvicorn backend.server:app --reload
```

> API live at: `http://127.0.0.1:8000`  
> Swagger docs at: `http://127.0.0.1:8000/docs`

**2. Start the Streamlit frontend** *(open a new terminal)*

```bash
streamlit run frontend/app.py
```

> Dashboard opens at: `http://localhost:8501`

---

## 📡 API Reference

All endpoints are served from `http://127.0.0.1:8000`

| Method   | Endpoint            | Description                  |
|----------|---------------------|------------------------------|
| `GET`    | `/expenses`         | Fetch all expenses           |
| `GET`    | `/expenses/{id}`    | Fetch a single expense by ID |
| `POST`   | `/expenses`         | Add a new expense            |
| `PUT`    | `/expenses/{id}`    | Update an existing expense   |
| `DELETE` | `/expenses/{id}`    | Delete an expense            |

**Example — Add an Expense**

```json
POST /expenses
Content-Type: application/json

{
  "title": "Grocery Shopping",
  "amount": 850.00,
  "category": "Food",
  "date": "2024-12-01"
}
```

> 📘 Full interactive docs are auto-generated by FastAPI at `http://127.0.0.1:8000/docs`

---

## 🧪 Postman Testing

All API endpoints have been tested using Postman.

**To test:**

1. Open Postman
2. Set the base URL to `http://127.0.0.1:8000`
3. Use the endpoints from the API Reference table above
4. Set `Content-Type: application/json` for POST and PUT requests

---

## ✅ Running Tests

```bash
pytest tests/
```

Tests are located in `tests/backend/test_db_helper.py` and use shared fixtures from `tests/conftest.py`.

---

## 🤝 Starting the APP

Running the App
1. Start the FastAPI backend server
bash cd backend
uvicorn server:app --reload

API live at: http://127.0.0.1:8000
Swagger docs at: http://127.0.0.1:8000/docs

2. Start the Streamlit frontend (open a new terminal)
bash cd frontend
streamlit run app.py

Dashboard opens at: http://localhost:8501

---

<div align="center">

Made with ❤️ by [Godwin Stanes](https://github.com/godwin-stanes)

⭐ If you found this project helpful, please give it a star!

</div>
