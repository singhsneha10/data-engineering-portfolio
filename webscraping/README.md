# 🏗️ Job Scraper Pipeline

An automated **data engineering pipeline** that fetches live job listings from the Himalayas Jobs API, stores them in a **PostgreSQL** database, and runs on a fully automated **daily schedule** using APScheduler.

Built as a production-style project to demonstrate real-world data engineering skills.

---

## 📌 Project Overview

Most job scraper projects just print data to the terminal. This pipeline goes further:

- Fetches **live job data** from a real API
- **Stores it persistently** in a relational database
- **Deduplicates** entries automatically — no dirty data
- **Runs on a schedule** without any manual intervention
- Built with **production-style code structure** — config, database, scraper, and scheduler are all separated cleanly

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| PostgreSQL | Relational database for storing job listings |
| psycopg2 | PostgreSQL adapter for Python |
| APScheduler | Scheduling the scraper to run daily |
| requests | Fetching data from the Himalayas API |
| python-dotenv | Loading credentials securely from `.env` |

---

## 📁 Project Structure

```
job_scraper_pipeline/
├── .env               # Database credentials (never committed to Git)
├── .gitignore         # Ignores .env, venv, pycache
├── config.py          # Loads DB config from .env
├── database.py        # DB connection, table creation, insert logic
├── scraper.py         # Fetches jobs from API and saves to DB
├── scheduler.py       # Runs scraper automatically every day at 8 AM
├── requirements.txt   # All dependencies
└── venv/              # Virtual environment (not committed)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/job-scraper-pipeline.git
cd job-scraper-pipeline
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_listings
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 5. Initialize the Database
```bash
python database.py
```
This creates the `job_listings` table in your PostgreSQL database.

### 6. Run the Scraper Manually (Test)
```bash
python scraper.py
```
You should see jobs being fetched and inserted into the database.

### 7. Start the Scheduler
```bash
python scheduler.py
```
The pipeline will now run automatically every day at **08:00 AM**.

---

## 🗄️ Database Schema

```sql
CREATE TABLE job_listings (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    company     VARCHAR(255),
    location    VARCHAR(255),
    salary      VARCHAR(100),
    job_url     TEXT UNIQUE,
    source      VARCHAR(100),
    scraped_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| Column | Description |
|--------|-------------|
| `id` | Auto-incrementing primary key |
| `title` | Job title |
| `company` | Company name |
| `location` | Location or remote restrictions |
| `salary` | Formatted salary range (e.g. USD 70,000 - 100,000) |
| `job_url` | Application link — also used for deduplication |
| `source` | Data source (Himalayas) |
| `scraped_at` | Timestamp of when the row was inserted |

---

## 🔁 How the Pipeline Works

```
Himalayas Jobs API
       │
       ▼
  scraper.py          ← Fetches jobs, formats data, skips incomplete entries
       │
       ▼
  database.py         ← Inserts into PostgreSQL, skips duplicates automatically
       │
       ▼
  job_listings table  ← Clean, deduplicated, timestamped job data
       ▲
       │
  scheduler.py        ← Triggers the above automatically every day at 8 AM
```

---

## 🧠 Key Engineering Decisions

**Why Himalayas API instead of HTML scraping?**
Other job boards (RemoteOK, Jobicy) returned 403 errors and blocked scrapers. Himalayas provides a clean, reliable public API — a more realistic data engineering approach.

**Why `ON CONFLICT (job_url) DO NOTHING`?**
Running the pipeline daily means the same jobs will appear in the API repeatedly. This constraint ensures we never insert duplicates, keeping the data clean without any extra code.

**Why separate files instead of one script?**
Separating config, database logic, scraper logic, and scheduler logic mirrors how real data pipelines are structured in professional environments. Each module has a single responsibility and can be tested independently.

---

## 📊 Sample Output

```
🔍 Fetching jobs from Himalayas API...
✅ Found 20 jobs!
✅ Inserted: Python Developer at Acme Corp
✅ Inserted: Backend Engineer at StartupXYZ
✅ Inserted: Data Engineer at Remote Co
...
```

---

## 🔮 Potential Future Improvements

- [ ] Add `logging` module to replace `print()` statements
- [ ] Export data to `.csv` for analysis
- [ ] Scrape multiple job categories (python, SQL, data engineer)
- [ ] Add a simple dashboard to visualize job trends
- [ ] Deploy on a cloud VM so it runs 24/7 without keeping laptop open

---

## 👤 Author

**Your Name**
[LinkedIn](https://www.linkedin.com/in/sneha-singh-04a1a6254/) • [GitHub](https://github.com/singhsneha10)