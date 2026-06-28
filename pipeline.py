# ==========================================================
# RetailMart Data Engineering Project
# Author : Satinder Singh
# Description:
# Data Ingestion and Data Cleaning Pipeline
# ==========================================================

# ==========================================================
# Import Required Libraries
# ==========================================================

import pandas as pd
import numpy as np


# ==========================================================
# Data Ingestion
# ==========================================================

print("=" * 60)
print("RETAILMART DATA PIPELINE")
print("=" * 60)

print("\nLoading CSV Files...\n")

sales_df = pd.read_csv("data/sales_data.csv")
products_df = pd.read_csv("data/products.csv")
stores_df = pd.read_csv("data/stores.csv")

print("✅ All CSV files loaded successfully.")

# ==========================================================
# Dataset Information
# ==========================================================

print("\n" + "=" * 60)
print("DATASET SHAPES")
print("=" * 60)

print(f"Sales Data    : {sales_df.shape}")
print(f"Products Data : {products_df.shape}")
print(f"Stores Data   : {stores_df.shape}")

print("\n" + "=" * 60)
print("FIRST 5 ROWS OF SALES DATA")
print("=" * 60)

print(sales_df.head())

# ==========================================================
# Missing Values Summary
# ==========================================================

print("\n" + "=" * 60)
print("MISSING VALUES SUMMARY")
print("=" * 60)

print("\nSales Data")
print(sales_df.isnull().sum())

print("\nProducts Data")
print(products_df.isnull().sum())

print("\nStores Data")
print(stores_df.isnull().sum())

# ==========================================================
# Data Cleaning
# ==========================================================

print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)

# Count duplicate rows
duplicate_count = sales_df.duplicated().sum()

print(f"\nDuplicate Rows Found : {duplicate_count}")

# Remove duplicate rows
sales_df = sales_df.drop_duplicates()

print("Duplicate rows removed successfully.")

# Fill missing quantity with 0
sales_df["quantity"] = sales_df["quantity"].fillna(0)

# Remove rows where amount is NULL
sales_df = sales_df.dropna(subset=["amount"])

print("Missing values handled successfully.")

print(f"\nCleaned Dataset Shape : {sales_df.shape}")

# ==========================================================
# Data Type Conversion
# ==========================================================

print("\n" + "=" * 60)
print("DATA TYPE CONVERSION")
print("=" * 60)

# Convert sale_date to datetime
sales_df["sale_date"] = pd.to_datetime(
    sales_df["sale_date"],
    errors="coerce"
)

# Convert amount to float
sales_df["amount"] = sales_df["amount"].astype(float)

# Convert quantity to integer
sales_df["quantity"] = sales_df["quantity"].astype(int)

print("Data types converted successfully.")

print("\nCurrent Data Types\n")

print(sales_df.dtypes)

print("\n" + "=" * 60)
print("TASK 1 & TASK 2 COMPLETED SUCCESSFULLY")
print("=" * 60)