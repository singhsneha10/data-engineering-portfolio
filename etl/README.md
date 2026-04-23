# 🔄 CSV to PostgreSQL ETL Pipeline

An end-to-end **ETL (Extract, Transform, Load)** pipeline that extracts data from a SQL Server source database (AdventureWorks), transforms it using Pandas, and loads it into a PostgreSQL data warehouse — built to demonstrate core data engineering fundamentals.

---

## 📌 Project Overview

This pipeline automates the movement of structured data across two relational systems:

- **Extracts** selected dimension and fact tables from a local SQL Server (AdventureWorks)
- **Transforms** the data in-memory using Pandas (type handling, staging prefix)
- **Loads** the cleaned data into PostgreSQL as staging tables, ready for downstream use

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core language |
| SQL Server (ODBC) | Source database |
| PostgreSQL | Destination / data warehouse |
| Pandas | In-memory data transformation |
| SQLAlchemy | PostgreSQL connection engine |
| pyodbc | SQL Server ODBC connector |
| python-dotenv | Secure credential management |

---

## 📁 Project Structure

```
etl/
├── etl.py              # Main ETL script (extract → transform → load)
├── requirements.txt    # Python dependencies
├── .env                # DB credentials (never committed to Git)
├── .gitignore          # Excludes .env, venv, __pycache__
└── README.md           # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/singhsneha10/data-engineering-portfolio.git
cd data-engineering-portfolio/etl
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

Create a `.env` file in the project root:
```
PGUID=your_postgres_username
PGPASS=your_postgres_password
```

> ⚠️ Never commit your `.env` file — it is excluded via `.gitignore`

### 5. Ensure Source Database is Available

This pipeline connects to a local **SQL Server** instance with the **AdventureWorks** database installed. Make sure ODBC Driver 17 for SQL Server is installed on your machine.

### 6. Run the Pipeline
```bash
python etl.py
```

---

## 🗄️ Tables Extracted

The pipeline targets the following AdventureWorks tables:

| Table | Type | Description |
|-------|------|-------------|
| `DimProduct` | Dimension | Product master data |
| `DimProductSubcategory` | Dimension | Product subcategory hierarchy |
| `DimProductCategory` | Dimension | Top-level product categories |
| `DimSalesTerritory` | Dimension | Sales territory geography |
| `FactInternetSales` | Fact | Internet sales transactions |

All tables are loaded into PostgreSQL with the `stg_` prefix (e.g., `stg_DimProduct`) to indicate staging layer.

---

## 🔁 How the Pipeline Works

```
SQL Server (AdventureWorks)
          │
          ▼
      extract()         ← Connects via ODBC, queries selected tables
          │
          ▼
     pd.read_sql()      ← Loads each table into a Pandas DataFrame
          │
          ▼
       load()           ← Writes DataFrame to PostgreSQL via SQLAlchemy
          │
          ▼
  PostgreSQL (stg_*)    ← Staging tables ready for transformation
```

---

## 🧠 Key Engineering Decisions

**Why `if_exists='replace'`?**
Each run fully refreshes the staging tables. This is appropriate for a first-pass ETL where the source is the system of record and idempotency matters more than incremental loading.

**Why staging (`stg_`) prefix?**
Following data warehouse convention — raw ingested data lands in a staging layer before any transformations are applied in downstream layers (silver/gold).

**Why environment variables for credentials?**
Hardcoding database passwords is a security risk. Using `os.environ` keeps credentials out of the codebase and out of version control.

---

## 📊 Sample Output

```
Connected to SQL Server successfully
Tables found: ['DimProduct', 'DimProductCategory', 'DimSalesTerritory', 'FactInternetSales']
Extracting table: DimProduct
  Rows fetched: 606
  Importing rows 0 to 606 for table DimProduct
  DimProduct imported successfully
Extracting table: FactInternetSales
  Rows fetched: 60398
  Importing rows 0 to 60398 for table FactInternetSales
  FactInternetSales imported successfully
```

---

## 🔮 Potential Future Improvements

- [ ] Add logging module (replace `print()` with structured logs)
- [ ] Add incremental loading using watermark / timestamp columns
- [ ] Add data validation checks post-load (row count assertions)
- [ ] Schedule with Apache Airflow for orchestrated runs
- [ ] Containerize with Docker for portability

---

## 👤 Author

**Sneha Singh**
[LinkedIn](https://www.linkedin.com/in/sneha-singh-04a1a6254/) • [GitHub](https://github.com/singhsneha10)
