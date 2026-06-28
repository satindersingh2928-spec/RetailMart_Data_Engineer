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

# Display all columns in output
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# ==========================================================
# Configuration
# ==========================================================

DATA_FOLDER = "data"


# ==========================================================
# Load Data
# ==========================================================

def load_data():
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
# Main Function
# ==========================================================

def main():

    sales_df, products_df, stores_df = load_data()

    sales_df = clean_data(sales_df)

    merged_df = merge_data(
        sales_df,
        stores_df,
        products_df
    )

    merged_df = calculate_total_revenue(
        merged_df
    )

    city_wise_revenue(
        merged_df
    )

    print("\n" + "=" * 60)
    print("TASK 1, TASK 2 & TASK 3 COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ==========================================================
# Program Entry Point
# ==========================================================

if __name__ == "__main__":
    main()