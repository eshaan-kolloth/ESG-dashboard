# ============================================================
# STEP 1 — Load and Explore the ESG Dataset
# ============================================================

import pandas as pd

# ---- Load the CSV file ----
# r"..." means raw string — fixes Windows backslash problem
df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\data.csv")



# ---- See the shape (rows x columns) ----
print("=" * 50)
print("DATASET SHAPE (rows, columns):")
print(df.shape)



# ---- See the first 5 rows ----
print("\nFIRST 5 ROWS OF DATA:")
print(df.head())



# ---- See all column names ----
print("\nCOLUMN NAMES:")
for col in df.columns:
    print(" -", col)



# ---- See data types ----
print("\nDATA TYPES:")
print(df.dtypes)



# ---- Check for missing values ----
print("\nMISSING VALUES PER COLUMN:")
print(df.isnull().sum())



# ---- Basic statistics ----
print("\nBASIC STATISTICS:")
print(df.describe())

print("\n Step 1 Complete! Data loaded successfully.")




