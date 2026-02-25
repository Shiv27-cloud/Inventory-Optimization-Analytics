import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# --- SQL CONFIGURATION ---
db_user = 'root'
db_password = '1234'
db_host = 'localhost'
db_port = '3306'
db_name = 'retail_supplydb'

# Connect to Database
connection_str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_str)


def run_analysis():
    print("INVENTORY ANALYSIS")

    # 1. Fetching raw data
    print("Fetching raw data from SQL...")
    query = "SELECT * FROM raw_sales_data"
    df = pd.read_sql(query, engine)

    # Convert dates to datetime objects
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    print(f"   -> Loaded {len(df)} rows.")

    # 2. Split Data into SALES and RETURNS
    # Sales: Quantity > 0
    df_sales = df[df['quantity'] > 0].copy()




    # Returns: Quantity < 0 (We turn quantity positive for math)
    df_returns = df[df['quantity'] < 0].copy()
    df_returns['quantity'] = df_returns['quantity'].abs()

    print("Step 2: Calculating Product Metrics...")

    # --- AGGREGATION LOGIC ---

    # A. Calculate Sales Metrics (Group by StockCode)
    sales_metrics = df_sales.groupby('stock_code').agg(
        description=('description', 'first'),  # Just take the first name found
        total_units_sold=('quantity', 'sum'),
        total_revenue=('unit_price', lambda x: (x * df_sales.loc[x.index, 'quantity']).sum()),
        transaction_count=('invoice_no', 'nunique'),  # How many invoices?
        unique_customers=('customer_id', 'nunique'),  # How many people?
        last_sale_date=('invoice_date', 'max')
    )

    # Calculate Average Price (Revenue / Units)
    sales_metrics['avg_price'] = sales_metrics['total_revenue'] / sales_metrics['total_units_sold']

    # B. Calculate Returns Metrics
    returns_metrics = df_returns.groupby('stock_code')['quantity'].sum().rename('total_units_returned')

    # C. Merge Sales + Returns
    # We use 'left' join because some items sell but never get returned
    final_df = sales_metrics.merge(returns_metrics, on='stock_code', how='left')

    # Fill NaN returns with 0 (for items that were never returned)
    final_df['total_units_returned'] = final_df['total_units_returned'].fillna(0)

    # --- ADVANCED METRICS ---

    # 1. Return Rate %
    final_df['return_rate'] = (final_df['total_units_returned'] / final_df['total_units_sold']) * 100

    # 2. Recency (Days since last sale)
    # We pick a "Current Date" relative to the dataset (Dec 2011)
    snapshot_date = final_df['last_sale_date'].max()
    final_df['days_since_last_sale'] = (snapshot_date - final_df['last_sale_date']).dt.days

    # --- ABC CLASSIFICATION (The Pareto Logic) ---
    print("Step 3: Performing ABC Analysis...")

    # Sort by Revenue High-to-Low
    final_df = final_df.sort_values(by='total_revenue', ascending=False)

    # Calculate Cumulative Revenue
    final_df['revenue_cumulative'] = final_df['total_revenue'].cumsum()
    total_revenue_grand = final_df['total_revenue'].sum()
    final_df['revenue_cumulative_pct'] = final_df['revenue_cumulative'] / total_revenue_grand

    # Assign Labels
    def assign_abc(pct):
        if pct <= 0.80:
            return 'A'
        elif pct <= 0.95:
            return 'B'
        else:
            return 'C'

    final_df['abc_category'] = final_df['revenue_cumulative_pct'].apply(assign_abc)

    # --- DEAD STOCK LOGIC ---
    # Condition: Class C AND Hasn't sold in 90 days
    final_df['is_dead_stock'] = np.where(
        (final_df['abc_category'] == 'C') & (final_df['days_since_last_sale'] > 90),
        True,
        False
    )

    # --- CLEANUP & UPLOAD ---
    print("Step 4: Uploading findings to SQL...")

    # Prepare columns to match SQL Table exactly
    final_df = final_df.reset_index()  # make stock_code a column again

    # Rename columns to match SQL schema
    output_df = final_df[[
        'stock_code', 'description', 'total_units_sold', 'total_revenue',
        'avg_price', 'return_rate', 'transaction_count', 'unique_customers',
        'last_sale_date', 'days_since_last_sale', 'revenue_cumulative',
        'revenue_cumulative_pct', 'abc_category', 'is_dead_stock'
    ]].copy()

    output_df.rename(columns={'stock_code': 'product_id'}, inplace=True)

    # Handle weird infinite numbers or NaNs before SQL
    output_df.fillna(0, inplace=True)

    # Upload
    output_df.to_sql('inventory_analytics', con=engine, if_exists='replace', index=False)

    print("-" * 30)
    print("SUCCESS! Analysis Complete.")
    print(f"Processed {len(output_df)} unique products.")
    print("-" * 30)


if __name__ == "__main__":
    run_analysis()