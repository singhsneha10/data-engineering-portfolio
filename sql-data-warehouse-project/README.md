# 🏛️ SQL Data Warehouse — Medallion Architecture

A production-style **data warehouse** built on SQL Server implementing a full **Bronze → Silver → Gold** medallion architecture. Raw data from two source systems (CRM and ERP) is ingested, cleaned, transformed, and modelled into a **Star Schema** optimised for business analytics.

---

## 📌 Project Overview

This project demonstrates end-to-end data warehouse engineering — from raw CSV ingestion to a clean, analytics-ready data model:

- **Ingests** raw CRM and ERP data via SQL Server `BULK INSERT` stored procedures
- **Cleans** and **standardises** data across a dedicated Silver layer (deduplication, null handling, type casting, date validation)
- **Models** business-ready dimension and fact tables in a Gold layer (Star Schema)
- **Validates** data quality at each layer with dedicated test scripts

---

## 🏗️ Architecture

```
Data Sources
  ├── CRM System  (cust_info.csv, prd_info.csv, sales_details.csv)
  └── ERP System  (CUST_AZ12.csv, LOC_A101.csv, PX_CAT_G1V2.csv)
         │
         ▼
  ┌─────────────┐
  │   BRONZE    │  Raw ingestion — no transformations, exact copy of source
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │   SILVER    │  Cleaned & standardised — nulls handled, types cast, deduped
  └─────────────┘
         │
         ▼
  ┌─────────────┐
  │    GOLD     │  Star schema views — dim_customers, dim_products, fact_sales
  └─────────────┘
         │
         ▼
  Analytics / Reporting
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| SQL Server | Database engine |
| T-SQL | DDL, stored procedures, views, quality checks |
| BULK INSERT | CSV ingestion into Bronze layer |
| Star Schema | Gold layer data modelling |
| Draw.io | Architecture and data flow diagrams |

---

## 📁 Project Structure

```
sql-data-warehouse-project/
├── datasets/
│   ├── source_crm/
│   │   ├── cust_info.csv          # Customer master data
│   │   ├── prd_info.csv           # Product master data
│   │   └── sales_details.csv      # Sales transactions
│   └── source_erp/
│       ├── CUST_AZ12.csv          # Customer demographics (birthdate, gender)
│       ├── LOC_A101.csv           # Customer location / country
│       └── PX_CAT_G1V2.csv        # Product category hierarchy
│
├── scripts/
│   ├── bronze/
│   │   ├── ddl_bronze.sql         # Creates raw ingestion tables
│   │   └── proc_load_bronze.sql   # Stored procedure: BULK INSERT from CSVs
│   ├── silver/
│   │   ├── ddl_silver.sql         # Creates cleaned/typed silver tables
│   │   └── proc_load_silver.sql   # Stored procedure: transforms bronze → silver
│   └── golden/
│       └── ddl_gold.sql           # Creates Gold layer views (Star Schema)
│
├── tests/
│   ├── quality_checks_silver.sql  # Null, duplicate, format checks on silver
│   └── quality_checks_gold.sql    # Referential integrity checks on gold
│
├── docs/
│   └── data_catalogue.md          # Column-level data dictionary for Gold layer
│
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- SQL Server (Express or Developer edition)
- SSMS (SQL Server Management Studio)

### 1. Clone the Repository
```bash
git clone https://github.com/singhsneha10/data-engineering-portfolio.git
cd data-engineering-portfolio/sql-data-warehouse-project
```

### 2. Create the Database and Schemas
Open SSMS and run:
```sql
CREATE DATABASE DataWarehouse;
GO
USE DataWarehouse;
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;
```

### 3. Load the Bronze Layer
Update the file paths in `scripts/bronze/proc_load_bronze.sql` to match your local dataset location, then run:
```sql
-- Step 1: Create tables
-- Run: scripts/bronze/ddl_bronze.sql

-- Step 2: Load data via stored procedure
EXEC bronze.load_bronze;
```

### 4. Load the Silver Layer
```sql
-- Step 1: Create tables
-- Run: scripts/silver/ddl_silver.sql

-- Step 2: Transform and load
EXEC silver.load_silver;
```

### 5. Create the Gold Layer
```sql
-- Run: scripts/golden/ddl_gold.sql
-- This creates views: gold.dim_customers, gold.dim_products, gold.fact_sales
```

### 6. Run Quality Checks
```sql
-- After each layer load, validate with:
-- tests/quality_checks_silver.sql
-- tests/quality_checks_gold.sql
```

---

## 📊 Data Model — Star Schema (Gold Layer)

```
                    ┌──────────────────┐
                    │  dim_customers   │
                    │───────────────── │
                    │ customer_key  PK │◄──┐
                    │ customer_id      │   │
                    │ first_name       │   │
                    │ last_name        │   │
                    │ country          │   │
                    │ gender           │   │
                    │ birthdate        │   │
                    └──────────────────┘   │
                                           │
┌──────────────────┐       ┌───────────────┴──────┐
│  dim_products    │       │      fact_sales       │
│──────────────────│       │──────────────────────-│
│ product_key   PK │◄──────│ order_number          │
│ product_name     │       │ product_key       FK  │
│ category         │       │ customer_key      FK  │
│ subcategory      │       │ order_date            │
│ product_line     │       │ shipping_date         │
│ cost             │       │ sales_amount          │
└──────────────────┘       │ quantity              │
                           │ price                 │
                           └───────────────────────┘
```

---

## 🔍 Data Quality Checks

Quality validation scripts run after each layer load to ensure:

**Silver Layer checks:**
- No NULL or duplicate primary keys
- No unwanted whitespace in string columns
- Data standardisation (gender, marital status values are consistent)
- No invalid date ranges (e.g. end date before start date)
- Sales amount = quantity × price consistency

**Gold Layer checks:**
- Surrogate key uniqueness in `dim_customers` and `dim_products`
- No orphaned records in `fact_sales` (all FKs resolve to a dimension row)

---

## 🧠 Key Engineering Decisions

**Why a medallion architecture (Bronze → Silver → Gold)?**
Separating raw ingestion, cleaning, and modelling into distinct layers means errors can be traced and fixed at the right level without re-ingesting from source. It also mirrors how production data platforms (Databricks, Delta Lake) are structured.

**Why stored procedures for loading?**
Stored procedures encapsulate the ETL logic in the database, making loads repeatable, transactional, and easy to schedule. Each procedure includes timing instrumentation and structured error handling.

**Why views for the Gold layer instead of physical tables?**
Gold views always reflect the latest Silver data without needing a separate load step. This keeps the serving layer lightweight and ensures analytical queries always read clean, current data.

**Why surrogate keys in dimensions?**
Natural keys from source systems (like `cst_id`) can be reused or change meaning over time. Surrogate keys (`customer_key` via `ROW_NUMBER()`) provide stable, system-independent identifiers for joining fact and dimension tables.

---

## 📂 Documentation

See [`docs/data_catalogue.md`](docs/data_catalogue.md) for a full column-level data dictionary of all Gold layer tables.

---

## 🔮 Potential Future Improvements

- [ ] Orchestrate loads with Apache Airflow DAGs
- [ ] Add incremental loading (watermark-based) to replace full truncate-and-load
- [ ] Connect Gold layer to a BI tool (Power BI / Metabase) for dashboards
- [ ] Migrate to a cloud data warehouse (Snowflake / BigQuery)
- [ ] Add SCD Type 2 (Slowly Changing Dimensions) to track historical changes

---

## 👤 Author

**Sneha Singh**
[LinkedIn](https://www.linkedin.com/in/sneha-singh-04a1a6254/) • [GitHub](https://github.com/singhsneha10)