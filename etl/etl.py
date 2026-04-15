from sqlalchemy import create_engine
import pyodbc
import pandas as pd
import os

pg_pwd = os.environ['PGPASS']
pg_uid = os.environ['PGUID']

# sql db details
driver = "{ODBC Driver 17 for SQL Server}"
server = "localhost\\SQLEXPRESS"
database = "AdventureWorks"

# extract data from sql server
def extract():
    src_conn = None
    try:
        src_conn = pyodbc.connect(
            'DRIVER=' + driver +
            ';SERVER=' + server +
            ';DATABASE=' + database +
            ';Trusted_Connection=yes'
        )
        print("Connected to SQL Server successfully")
        src_cursor = src_conn.cursor()
        src_cursor.execute("""
            SELECT t.name AS table_name
            FROM sys.tables t
            WHERE t.name IN (
                'DimProduct', 'DimProductSubcategory', 'DimProductSubCategory',
                'DimProductCategory', 'DimSalesTerritory', 'FactInternetSales'
            )
        """)
        src_tables = src_cursor.fetchall()
        print(f"Tables found: {[t[0] for t in src_tables]}")

        if not src_tables:
            print("No matching tables found - check your database and table names")
            return

        for tbl in src_tables:
            print(f"Extracting table: {tbl[0]}")
            df = pd.read_sql_query(f'SELECT * FROM {tbl[0]}', src_conn)
            print(f"  Rows fetched: {len(df)}")
            load(df, tbl[0])

    except Exception as e:
        print("Data extract error: " + str(e))
    finally:
        if src_conn:
            src_conn.close()

# load data to postgres
def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{pg_uid}:{pg_pwd}@localhost:5432/AdventureWorks')
        print(f'  Importing rows {rows_imported} to {rows_imported + len(df)} for table {tbl}')
        df.to_sql(f'stg_{tbl}', engine, if_exists='replace', index=False)
        rows_imported += len(df)
        print(f"  {tbl} imported successfully")
    except Exception as e:
        print("Data load error: " + str(e))

try:
    extract()
except Exception as e:
    print("Error while extracting data: " + str(e))