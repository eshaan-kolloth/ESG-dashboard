# ============================================================
# STEP 2 — Cleaning the ESG Dataset
# ============================================================

import pandas as pd

# ---- Load the raw data ----
df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\data.csv")

print("=" * 50)
print(f"BEFORE CLEANING: {df.shape[0]} rows, {df.shape[1]} columns")


# ============================================================
#  DROP columns we don't need for our project
# ============================================================


# logo, weburl, cik are not useful for ESG analysis
columns_to_drop = ["logo", "weburl", "cik", "currency"]
df = df.drop(columns=columns_to_drop)
print(f"\n Dropped unnecessary columns: {columns_to_drop}")



# ============================================================
#  RENAME columns to be cleaner and easier to read
# ============================================================
df = df.rename(columns={
    "ticker"              : "Ticker",
    "name"                : "Company",
    "exchange"            : "Exchange",
    "industry"            : "Industry",
    "environment_grade"   : "Env_Grade",
    "environment_level"   : "Env_Level",
    "social_grade"        : "Social_Grade",
    "social_level"        : "Social_Level",
    "governance_grade"    : "Gov_Grade",
    "governance_level"    : "Gov_Level",
    "environment_score"   : "Env_Score",
    "social_score"        : "Social_Score",
    "governance_score"    : "Gov_Score",
    "total_score"         : "Total_Score",
    "last_processing_date": "Date",
    "total_grade"         : "Total_Grade",
    "total_level"         : "Total_Level"
})

print("✅ Columns renamed successfully")



# ============================================================
# FIX MISSING VALUES
# ============================================================
print(f"\nMissing values BEFORE fix:")
print(df.isnull().sum()[df.isnull().sum() > 0])  # only show columns with missing values




# Fill missing Industry with "Unknown"
df["Industry"] = df["Industry"].fillna("Unknown")

print(f"\nMissing values AFTER fix:")
missing = df.isnull().sum()[df.isnull().sum() > 0]
if len(missing) == 0:
    print("  No missing values! ✅")
else:
    print(missing)




# ============================================================
# 4. FIX the Date column
# ============================================================
# Convert date from string "19-04-2022" to proper date format
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

print(f"\n Date column fixed")





# ============================================================
# 5. ADD a new column — ESG Category based on Total_Score
# ============================================================
# This labels each company as Leader, Average, or Laggard

def esg_category(score):
    if score >= 1100:
        return " Leader"
    elif score >= 800:
        return " Average"
    else:
        return "Laggard"

df["ESG_Category"] = df["Total_Score"].apply(esg_category)

print("\n✅ ESG Category column added")
print(df["ESG_Category"].value_counts())





# ============================================================
# 6. RESET index (just good practice after cleaning)
# ============================================================
df = df.reset_index(drop=True)




print("\n✅ Step 2 Complete! Cleaned data saved ")



# ============================================================
# 7. SAVE the cleaned data
# ============================================================
df.to_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_cleaned.csv", index=False)

print("\n" + "=" * 50)
print(f"AFTER CLEANING: {df.shape[0]} rows, {df.shape[1]} columns")
print("✅ Step 2 Complete! Cleaned data saved as esg_cleaned.csv")