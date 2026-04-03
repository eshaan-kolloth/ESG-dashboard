# ============================================================
# STEP 3 — Weighted ESG Scoring Model
# ============================================================


# pandas helps us work with data tables (like Excel in Python)
import pandas as pd




# ============================================================
# PART 1 — Load the cleaned data from Step 2
# ============================================================

# r"..." means raw string — fixes Windows backslash problem
# We are opening the cleaned file we saved in Step 2
df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_cleaned.csv")




# Just printing a nice header line
print("=" * 50)
print("BUILDING WEIGHTED ESG SCORING MODEL")
print("=" * 50)




# ============================================================
# PART 2 — Define Weights
# These numbers decide HOW IMPORTANT each score is
# All three MUST add up to 1.0 (which means 100%)
# ============================================================

ENV_WEIGHT = 0.40   # Environmental is 40% important
SOC_WEIGHT = 0.35   # Social is 35% important
GOV_WEIGHT = 0.25   # Governance is 25% important




# f"..." means we can put variables inside {} directly
# ENV_WEIGHT * 100 converts 0.40 to 40.0 for nicer printing
print(f"\nWeights Used:")
print(f"  Environmental : {ENV_WEIGHT * 100}%")
print(f"  Social        : {SOC_WEIGHT * 100}%")
print(f"  Governance    : {GOV_WEIGHT * 100}%")
print(f"  Total         : {(ENV_WEIGHT + SOC_WEIGHT + GOV_WEIGHT) * 100}%")




# ============================================================
# PART 3 — Normalize Scores to 0-100 scale
#
# WHY? Because original scores have different ranges:
#   Env_Score    = 200 to 719  (big range)
#   Social_Score = 160 to 667  (big range)
#   Gov_Score    =  75 to 475  (smaller range)
#
# If we don't normalize, bigger numbers will always win
# unfairly. So we convert everyone to 0-100 first.
#
# FORMULA:
#   (your score - lowest score)
#   --------------------------- × 100
#   (highest score - lowest score)
#
# EXAMPLE for a company with Env_Score = 500:
#   (500 - 200) / (719 - 200) × 100
#   = 300 / 519 × 100
#   = 57.8 out of 100
# ============================================================



# df["Env_Score"].min() finds the lowest Env_Score in ALL 722 companies
# df["Env_Score"].max() finds the highest Env_Score in ALL 722 companies
# We create a NEW column called Env_Norm to store the normalized score

df["Env_Norm"] = (
    (df["Env_Score"] - df["Env_Score"].min()) /         # your score - lowest score
    (df["Env_Score"].max() - df["Env_Score"].min())      # highest score - lowest score
) * 100                                                  # multiply by 100 to get 0-100



# Same formula for Social Score
df["Social_Norm"] = (
    (df["Social_Score"] - df["Social_Score"].min()) /
    (df["Social_Score"].max() - df["Social_Score"].min())
) * 100



# Same formula for Governance Score
df["Gov_Norm"] = (
    (df["Gov_Score"] - df["Gov_Score"].min()) /
    (df["Gov_Score"].max() - df["Gov_Score"].min())
) * 100

print("\n✅ Scores normalized to 0-100 scale")





# Let's print one example to see what normalization did
print("\nExample — First company before and after normalization:")
print(f"  Company      : {df['Company'][0]}")
print(f"  Env_Score    : {df['Env_Score'][0]}  →  Env_Norm    : {df['Env_Norm'][0].round(2)}")
print(f"  Social_Score : {df['Social_Score'][0]}  →  Social_Norm : {df['Social_Norm'][0].round(2)}")
print(f"  Gov_Score    : {df['Gov_Score'][0]}  →  Gov_Norm    : {df['Gov_Norm'][0].round(2)}")




# ============================================================
# PART 4 — Calculate Weighted ESG Score
#
# Now we multiply each normalized score by its weight
# and add them all together
#
# FORMULA:
#   Weighted_ESG_Score = (Env_Norm × 0.40)
#                      + (Social_Norm × 0.35)
#                      + (Gov_Norm × 0.25)
#
# EXAMPLE:
#   Env_Norm    = 57.8 × 0.40 = 23.12
#   Social_Norm = 65.0 × 0.35 = 22.75
#   Gov_Norm    = 70.0 × 0.25 = 17.50
#   Final Score = 23.12 + 22.75 + 17.50 = 63.37
# ============================================================



# We create a NEW column called Weighted_ESG_Score
df["Weighted_ESG_Score"] = (
    (df["Env_Norm"]    * ENV_WEIGHT) +   # Environment part
    (df["Social_Norm"] * SOC_WEIGHT) +   # Social part
    (df["Gov_Norm"]    * GOV_WEIGHT)     # Governance part
)

# Round to 2 decimal places — 63.3712 becomes 63.37
df["Weighted_ESG_Score"] = df["Weighted_ESG_Score"].round(2)

print("\n✅ Weighted ESG Score calculated")





# ============================================================
# PART 5 — Rank all 722 companies
#
# rank(ascending=False) means:
#   highest score = Rank 1 (best)
#   lowest score  = Rank 722 (worst)
#
# .astype(int) converts 1.0 to 1 (whole number, looks cleaner)
# ============================================================


df["ESG_Rank"] = df["Weighted_ESG_Score"].rank(ascending=False).astype(int)

print("✅ Companies ranked 1 to 722")





# ============================================================
# PART 6 — Show TOP 10 and BOTTOM 10 companies
#
# sort_values() sorts the table by a column
#   ascending=False → highest first (for top 10)
#   ascending=True  → lowest first  (for bottom 10)
# .head(10) picks only the first 10 rows
# ============================================================



# Sort by highest score first, take first 10
top10 = df.sort_values("Weighted_ESG_Score", ascending=False).head(10)



# Sort by lowest score first, take first 10
bot10 = df.sort_values("Weighted_ESG_Score", ascending=True).head(10)

print("\n" + "=" * 50)
print("TOP 10 ESG COMPANIES:")
print("=" * 50)



# We select only these columns to display — cleaner output
print(top10[["Company", "Industry", "Env_Norm", "Social_Norm", "Gov_Norm", "Weighted_ESG_Score", "ESG_Rank"]].to_string(index=False))

print("\n" + "=" * 50)
print("BOTTOM 10 ESG COMPANIES:")
print("=" * 50)
print(bot10[["Company", "Industry", "Env_Norm", "Social_Norm", "Gov_Norm", "Weighted_ESG_Score", "ESG_Rank"]].to_string(index=False))




# ============================================================
# PART 7 — Average ESG Score by Industry
#
# groupby("Industry") → groups all companies by industry
# ["Weighted_ESG_Score"].mean() → average score per industry
# .round(2) → round to 2 decimal places
# .sort_values(ascending=False) → highest industry first
# .head(10) → show only top 10 industries
# ============================================================

print("\n" + "=" * 50)
print("AVERAGE WEIGHTED ESG SCORE BY INDUSTRY (Top 10):")
print("=" * 50)

industry_avg = (
    df.groupby("Industry")["Weighted_ESG_Score"]  # group by industry
    .mean()                                         # calculate average
    .round(2)                                       # round to 2 decimals
    .sort_values(ascending=False)                   # highest first
    .head(10)                                       # top 10 only
)

print(industry_avg.to_string())





# ============================================================
# PART 8 — Save the updated data with new columns
#
# We now have 3 new columns added:
#   Env_Norm, Social_Norm, Gov_Norm
#   Weighted_ESG_Score
#   ESG_Rank
#
# We save this as esg_scored.csv for future steps
# index=False means don't save the row numbers
# ============================================================

df.to_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv", index=False)

print("\n" + "=" * 50)
print("✅ Step 3 Complete!")
print("✅ New file saved: esg_scored.csv")
print("✅ New columns added: Env_Norm, Social_Norm, Gov_Norm, Weighted_ESG_Score, ESG_Rank")
print("=" * 50)