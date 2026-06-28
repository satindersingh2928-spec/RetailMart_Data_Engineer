# 🛒 RetailMart Data Engineering Pipeline

## 📌 Project Overview

This project simulates a real-world data engineering pipeline for a retail company. The pipeline ingests raw sales data, cleans and transforms it, and loads it into a database for reporting and analysis.

---

## ⚙️ Tech Stack

* Python (Pandas, NumPy)
* SQLite
* SQL
* CSV Data Files

---

## 📂 Data Sources

* **sales_data.csv** → Transaction-level data (messy, duplicates, missing values)
* **products.csv** → Product details
* **stores.csv** → Store details

---

## 🔄 Pipeline Workflow

1. Data Ingestion
2. Data Cleaning
3. Data Transformation (Merging)
4. Revenue Calculation
5. Data Validation
6. Data Loading (SQLite)
7. SQL Reporting
8. Summary Insights

---

## 📊 Key Features

* Removed duplicate records
* Handled missing values
* Ensured data type consistency
* Performed referential integrity checks
* Added derived column: `total_revenue`
* Implemented SQL-based reporting

---

## 📈 Insights Generated

* Top 3 best-selling products
* Revenue per store per day
* City-wise revenue
* Business summary report

---

## 🛡️ Error Handling

* File not found handling
* Empty data checks
* Missing column detection
* Database error handling

---

## ▶️ How to Run

```bash
python pipeline.py
```

---

## 💡 Future Improvements

* Use PySpark for large-scale data
* Replace SQLite with cloud data warehouse
* Add logging instead of print statements
* Schedule pipeline using Airflow

---

## 👨‍💻 Author

Satinder Singh
