# ==========================================================
# RetailMart Data Engineering Project
# Author : Satinder Singh
# Description:
# Data Ingestion, Data Cleaning and Data Transformation
# ==========================================================

# ==========================================================
# Import Required Libraries
# ==========================================================

import pandas as pd
import numpy as np
import sqlite3
import os

# Display all columns in output
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# ==========================================================
# Configuration
# ==========================================================

DATA_FOLDER = "data"
DATABASE_PATH = "database/retailmart.db"

# ==========================================================
# Load Data
# ==========================================================

def load_data():
    files = [
    f"{DATA_FOLDER}/sales_data.csv",
    f"{DATA_FOLDER}/products.csv",
    f"{DATA_FOLDER}/stores.csv"
]

    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} not found!")
    """
    Load all CSV files into Pandas DataFrames.
    """

    print("=" * 60)
    print("LOADING DATA")
    print("=" * 60)

    sales_df = pd.read_csv(f"{DATA_FOLDER}/sales_data.csv")
    products_df = pd.read_csv(f"{DATA_FOLDER}/products.csv")
    stores_df = pd.read_csv(f"{DATA_FOLDER}/stores.csv")

    print("All CSV files loaded successfully.\n")

    print("Dataset Shapes")
    print("-" * 60)
    print(f"Sales Data    : {sales_df.shape}")
    print(f"Products Data : {products_df.shape}")
    print(f"Stores Data   : {stores_df.shape}")
    
    print("="*60)
    print("First 5 Rows")
    print("="*60)
    print(f"Sales\n{sales_df.head(5)}")
    print(f"Products\n{products_df.head(5)}")
    print(f"Stores\n{stores_df.head(5)}")

    return sales_df, products_df, stores_df


# ==========================================================
# Data Cleaning
# ==========================================================

def clean_data(sales_df):

    print("\n" + "=" * 60)
    print("DATA CLEANING")
    print("=" * 60)

    # Duplicate rows
    duplicate_count = sales_df.duplicated().sum()

    print(f"Duplicate Rows Found : {duplicate_count}")

    sales_df = sales_df.drop_duplicates()

    # Missing values summary
    print("\nMissing Values")

    print(sales_df.isnull().sum())

    # Fill missing quantity
    sales_df["quantity"] = sales_df["quantity"].fillna(0)

    # Drop missing amount
    sales_df = sales_df.dropna(subset=["amount"])

    # Convert datatypes
    sales_df["sale_date"] = pd.to_datetime(
        sales_df["sale_date"],
        errors="coerce"
    )
    
    # Remove invalid dates (VERY IMPORTANT)
    sales_df = sales_df.dropna(subset=["sale_date"])

    sales_df["quantity"] = sales_df["quantity"].astype(int)

    sales_df["amount"] = sales_df["amount"].astype(float)

    print("\nCleaning Completed Successfully.")

    print(f"Final Shape : {sales_df.shape}")

    print("\nData Types\n")

    print(sales_df.dtypes)

    return sales_df


# ==========================================================
# Data Transformation
# ==========================================================

def merge_data(sales_df, stores_df, products_df):

    print("\n" + "=" * 60)
    print("DATA TRANSFORMATION")
    print("=" * 60)

    # Merge Sales + Stores

    sales_store_df = pd.merge(
        sales_df,
        stores_df,
        on="store_id",
        how="left"
    )

    print("\nSales + Stores Merge Successful")

    print(f"Shape : {sales_store_df.shape}")

    # Merge Products

    merged_df = pd.merge(
        sales_store_df,
        products_df,
        on="product_id",
        how="left"
    )

    print("\nProducts Merge Successful")

    print(f"Final Shape : {merged_df.shape}")

    print("\nFirst 5 Rows\n")

    print(merged_df.head())
    
    print("\n❌ Missing store_name rows:")
    print(merged_df[merged_df["store_name"].isnull()].head())

    print("\n❌ Missing product_name rows:")
    print(merged_df[merged_df["product_name"].isnull()].head())

    return merged_df


# ==========================================================
# Total Revenue Calculation
# ==========================================================

def calculate_total_revenue(merged_df):

    print("\n" + "=" * 60)
    print("TOTAL REVENUE")
    print("=" * 60)

    merged_df["total_revenue"] = (
        merged_df["quantity"] *
        merged_df["price"]
    )

    print("\nTotal Revenue Column Added Successfully\n")

    print(merged_df.head())

    revenue = merged_df["total_revenue"]

    print("\nRevenue Statistics")

    print(f"Average Revenue : {np.mean(revenue):.2f}")
    print(f"Maximum Revenue : {np.max(revenue):.2f}")
    print(f"Minimum Revenue : {np.min(revenue):.2f}")

    return merged_df


# ==========================================================
# City Wise Revenue
# ==========================================================

def city_wise_revenue(merged_df):

    print("\n" + "=" * 60)
    print("CITY WISE REVENUE")
    print("=" * 60)

    city_revenue = (
        merged_df
        .groupby("city", as_index=False)["total_revenue"]
        .sum()
        .sort_values(
            by="total_revenue",
            ascending=False
        )
    )

    print(city_revenue)

    return city_revenue

# ==========================================================
# Final Data Validation
# ==========================================================

def validate_data(merged_df):

    print("\n" + "=" * 60)
    print("FINAL DATA VALIDATION")
    print("=" * 60)

    initial_rows = len(merged_df)

    # Remove nulls
    merged_df = merged_df.dropna(
        subset=[
            "product_name",
            "price",
            "store_name",
            "sale_date"
        ]
    )

    # Remove negative values
    merged_df = merged_df[
        (merged_df["quantity"] >= 0) &
        (merged_df["price"] >= 0) &
        (merged_df["total_revenue"] >= 0)
    ]

    final_rows = len(merged_df)

    print(f"Rows Before : {initial_rows}")
    print(f"Rows After  : {final_rows}")
    print(f"Removed     : {initial_rows - final_rows}")

    return merged_df

# ==========================================================
# Load Data into SQLite Database
# ==========================================================

def load_to_database(merged_df):

    print("\n" + "=" * 60)
    print("LOADING DATA TO SQLITE DATABASE")
    print("=" * 60)

    # Create Database Connection
    connection = sqlite3.connect(DATABASE_PATH)
    
    print("Database Connected Successfully.")
    
    # Save DataFrame into SQLite Table
    merged_df.to_sql(
        "retail_sales",
        connection,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into SQLite database.")
    
    # Close Database Connection
    connection.close()

    print("Database Connection Closed.")
    
# ==========================================================
# Top 3 Best Selling Products
# ==========================================================

def top_selling_products():

    print("\n" + "=" * 60)
    print("TOP 3 BEST SELLING PRODUCTS")
    print("=" * 60)

    # Connect to Database
    connection = sqlite3.connect(DATABASE_PATH)

    # SQL Query
    query = """
    SELECT
        product_name,
        SUM(quantity) AS total_quantity
    FROM retail_sales
    GROUP BY product_name
    ORDER BY total_quantity DESC
    LIMIT 3;
    """

    # Execute Query
    top_products = pd.read_sql_query(query, connection)

    print(top_products)

    # Close Connection
    connection.close()
    
# ==========================================================
# Revenue Per Store Per Day
# ==========================================================

def revenue_per_store_per_day():

    print("\n" + "=" * 60)
    print("TOTAL REVENUE PER STORE PER DAY")
    print("=" * 60)

    # Connect to Database
    connection = sqlite3.connect(DATABASE_PATH)

    # SQL Query
    query = """
    SELECT
        store_name,
        DATE(sale_date) as sale_date,
        SUM(total_revenue) AS total_revenue
    FROM retail_sales
    GROUP BY
        store_name,
        DATE(sale_date)
    ORDER BY
        store_name,
        sale_date;
    """

    # Execute Query
    revenue_df = pd.read_sql_query(query, connection)

    print(revenue_df)

    # Close Connection
    connection.close()
    
# ==========================================================
# SUMMARY_REPORT
# ==========================================================
    
def summary_report():

    print("\n" + "=" * 60)
    print("SUMMARY REPORT")
    print("=" * 60)

    # Connect DB
    connection = sqlite3.connect(DATABASE_PATH)

    # 1. Total Transactions
    total_transactions_query = "SELECT COUNT(*) AS total_transactions FROM retail_sales;"
    total_transactions = pd.read_sql_query(total_transactions_query, connection)

    # 2. Total Revenue
    total_revenue_query = "SELECT SUM(total_revenue) AS total_revenue FROM retail_sales;"
    total_revenue = pd.read_sql_query(total_revenue_query, connection)

    # 3. Top Selling City
    top_city_query = """
    SELECT city, SUM(total_revenue) AS revenue
    FROM retail_sales
    GROUP BY city
    ORDER BY revenue DESC
    LIMIT 1;
    """
    top_city = pd.read_sql_query(top_city_query, connection)

    # 4. Top Selling Product
    top_product_query = """
    SELECT product_name, SUM(quantity) AS total_quantity
    FROM retail_sales
    GROUP BY product_name
    ORDER BY total_quantity DESC
    LIMIT 1;
    """
    top_product = pd.read_sql_query(top_product_query, connection)

    # Print nicely
    print(f"Total Transactions : {total_transactions.iloc[0,0]}")
    print(f"Total Revenue      : {total_revenue.iloc[0,0]:.2f}")
    print(f"Top Selling City   : {top_city.iloc[0,0]}")
    print(f"Top Selling Product: {top_product.iloc[0,0]}")

    # Close DB
    connection.close()


# ==========================================================
# Main Function
# ==========================================================

def run_pipeline():

    print("\n" + "=" * 60)
    print("RUNNING FULL DATA PIPELINE")
    print("=" * 60)

    try:
        # Step 1: Load Data
        sales_df, products_df, stores_df = load_data()

        # Step 2: Clean Data
        sales_df = clean_data(sales_df)

        # Step 3: Merge Data
        merged_df = merge_data(sales_df, stores_df, products_df)
        
        # Step 4: Revenue Calculation
        merged_df = calculate_total_revenue(merged_df)

        # Step 5: Validate Data
        merged_df = validate_data(merged_df)

        # Step 6: City Revenue
        city_wise_revenue(merged_df)
        
        print("\nFinal Null Check:")
        print(merged_df.isnull().sum())
        print("Final Shape:", merged_df.shape)

        # Step 7: Load to Database
        load_to_database(merged_df)

        # Step 8: SQL Reports
        top_selling_products()
        revenue_per_store_per_day()

        # Step 9: Summary Report
        summary_report()

        print("\n" + "=" * 60)
        print("✅ PIPELINE EXECUTED SUCCESSFULLY")
        print("=" * 60)

    except FileNotFoundError as e:
        print("❌ ERROR: File not found.")
        print(e)

    except pd.errors.EmptyDataError:
        print("❌ ERROR: One of the CSV files is empty.")

    except KeyError as e:
        print("❌ ERROR: Missing column in dataset.")
        print(e)
        
    except sqlite3.Error as e:
        print("Database Error:", e)

    except Exception as e:
        print("❌ UNEXPECTED ERROR OCCURRED:")
        print(e)
        
def main():
    run_pipeline()

# ==========================================================
# Program Entry Point
# ==========================================================

if __name__ == "__main__":
    main()