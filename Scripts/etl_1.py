import pandas as pd
from sqlalchemy import create_engine

# --- CONFIGURATION ---
# 1. Database Credentials
db_user = 'root'
db_password = '1234'
db_host = 'localhost'
db_port = '3306'  # Default port
db_name = 'retail_supplydb'

# 2. File Settings
file_path = r"E:\DA_Projects\Retail-data-set\online_retail_II.xlsx"
sheet_name = 'Year 2010-2011'

# --- CONNECT TO DATABASE ---
# We use SQLAlchemy because it plays perfectly with Pandas
connection_str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_str)

try:
    print("Step 1: Reading Excel file... (This takes a moment)")
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    print(f"   -> Loaded {len(df)} rows from Excel.")

    # --- COLUMN MAPPING ---
    # SQL tables use 'snake_case' (lowercase_with_underscores).
    # Excel files use 'TitleCase'. We must rename them to match the SQL table exactly.
    df.rename(columns={
        'Invoice': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'InvoiceDate': 'invoice_date',
        'Price': 'unit_price',
        'Customer ID': 'customer_id',
        'Country': 'country'
    }, inplace=True)

    print("Step 2: Uploading to MariaDB... (This might take 1-2 mins)")

    # 'if_exists="append"' means: Put this data into the table we already created.
    # 'index=False' means: Don't upload the row numbers (0, 1, 2...) as a column.
    df.to_sql('raw_sales_data', con=engine, if_exists='append', index=False)

    print("-" * 30)
    print("SUCCESS! Data has been moved from Excel to SQL.")
    print("Check your 'raw_sales_data' table in HeidiSQL now.")
    print("-" * 30)

except Exception as e:
    print("\n❌ ERROR: Something went wrong.")
    print(e)

    