import sqlite3

DB_NAME = "jobs.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            score INTEGER
        )
    """)

    conn.commit()
    conn.close()


def job_exists(job_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM jobs WHERE id = ?",
        (job_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_job(job_id, title, company, location, score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (id, title, company, location, score)
        VALUES (?, ?, ?, ?, ?)
        """,
        (job_id, title, company, location, score)
    )

    conn.commit()
    conn.close()