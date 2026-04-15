import psycopg2
from config import DB_CONFIG

def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def create_table():
    """Create the job_listings table if it doesn't exist."""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_listings (
                id          SERIAL PRIMARY KEY,
                title       VARCHAR(255) NOT NULL,
                company     VARCHAR(255),
                location    VARCHAR(255),
                salary      VARCHAR(100),
                job_url     TEXT UNIQUE,
                source      VARCHAR(100),
                scraped_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Table created successfully!")

    except Exception as e:
        print(f"❌ Error creating table: {e}")

    finally:
        cursor.close()
        conn.close()

def insert_job(title, company, location, salary, job_url, source):
    """Insert a single job listing into the database."""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO job_listings (title, company, location, salary, job_url, source)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_url) DO NOTHING;
        """, (title, company, location, salary, job_url, source))
        conn.commit()
        print(f"✅ Inserted: {title} at {company}")

    except Exception as e:
        print(f"❌ Error inserting job: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()