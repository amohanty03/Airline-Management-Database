# Airline Management System

## Live Web Application
The application has been fully deployed to the cloud. You do not need to install any local database software to evaluate this project.

**URL:** https://amohanty03-airline-management-database-app-a7kp6r.streamlit.app/

> **Note:** The database is hosted live on Neon (Serverless PostgreSQL), and the frontend is hosted on Streamlit Community Cloud.

---

## Local Installation & Execution (Optional)
If you wish to run the Python code locally on your own machine, follow these steps:

### Prerequisites
- Ensure Python **3.8+** is installed on your machine.
- Ensure you have the project source code files (`app.py` and `requirements.txt`).

### 1) Install Dependencies
Open your terminal, navigate to the project directory, and run:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit`
- `pandas`
- `psycopg2-binary`
- `SQLAlchemy`

### 2) Database Setup (Local)

#### Generate a Local Database in pgAdmin using `airline_backup.sql`
If you prefer a fully local database, you can restore from the provided SQL backup file.

1. Install PostgreSQL and pgAdmin.
2. Open pgAdmin and create a new database (for example: `airline_db`).
3. Right-click on `airline-db` and click on `Restore`.
4. Open the file `airline_backup.sql` from this project.
5. Click on `Restore`, this should populate all the tables in the schema.
6. Update `.streamlit/secrets.toml` to point to your local PostgreSQL instance, for example:

```toml
DB_HOST = "localhost"
DB_NAME = "airline_db"
DB_USER = "postgres"
DB_PASSWORD = "<your-local-postgres-password>"
DB_PORT = "5432"
```

### 3) Run the Application
In your terminal, execute:

```bash
streamlit run app.py
```

A local web server will start, and the graphical user interface will open in your default web browser at:

- `http://localhost:8501`
