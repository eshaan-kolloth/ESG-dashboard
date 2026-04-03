# ============================================================
# STEP 4 — Industry Comparison & Business Insights
# ============================================================

import pandas as pd




# ---- Load the scored data from Step 3 ----
df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv")

print("=" * 50)
print("INDUSTRY COMPARISON & BUSINESS INSIGHTS")
print("=" * 50)





# ============================================================
# PART 1 — Average ESG Scores by Industry
# For each industry, calculate average E, S, G and Total
# ============================================================

industry_stats = df.groupby("Industry").agg(
    Avg_Env_Score    = ("Env_Score",           "mean"),
    Avg_Social_Score = ("Social_Score",         "mean"),
    Avg_Gov_Score    = ("Gov_Score",            "mean"),
    Avg_ESG_Score    = ("Weighted_ESG_Score",   "mean"),
    Company_Count    = ("Company",              "count")
).round(2).reset_index()




# Sort by highest ESG score
industry_stats = industry_stats.sort_values("Avg_ESG_Score", ascending=False)

print("\n📊 INDUSTRY ESG SUMMARY:")
print(industry_stats.to_string(index=False))




# ============================================================
# PART 2 — Top 3 and Bottom 3 Industries
# ============================================================

top3    = industry_stats.head(3)
bottom3 = industry_stats.tail(3)

print("\n" + "=" * 50)
print("🏆 TOP 3 MOST SUSTAINABLE INDUSTRIES:")
print("=" * 50)
for i, row in top3.iterrows():
    print(f"  {row['Industry']:<40} ESG Score: {row['Avg_ESG_Score']}")

print("\n" + "=" * 50)
print("⚠️  BOTTOM 3 LEAST SUSTAINABLE INDUSTRIES:")
print("=" * 50)
for i, row in bottom3.iterrows():
    print(f"  {row['Industry']:<40} ESG Score: {row['Avg_ESG_Score']}")




# ============================================================
# PART 3 — ESG Level Distribution per Industry
# How many Leaders, Average, Laggards in each industry?
# ============================================================

print("\n" + "=" * 50)
print("📊 ESG CATEGORY DISTRIBUTION BY INDUSTRY:")
print("=" * 50)

distribution = df.groupby(["Industry", "ESG_Category"]).size().unstack(fill_value=0)
print(distribution.to_string())




# ============================================================
# PART 4 — Business Insights
# ============================================================

print("\n" + "=" * 50)
print("💡 KEY BUSINESS INSIGHTS:")
print("=" * 50)



# Insight 1 — Best industry overall
best_industry = industry_stats.iloc[0]
print(f"\n1. BEST INDUSTRY FOR ESG INVESTMENT:")
print(f"   → {best_industry['Industry']}")
print(f"   → Average ESG Score: {best_industry['Avg_ESG_Score']}")
print(f"   → Number of Companies: {best_industry['Company_Count']}")



# Insight 2 — Worst industry overall
worst_industry = industry_stats.iloc[-1]
print(f"\n2. WORST INDUSTRY FOR ESG INVESTMENT:")
print(f"   → {worst_industry['Industry']}")
print(f"   → Average ESG Score: {worst_industry['Avg_ESG_Score']}")
print(f"   → Number of Companies: {worst_industry['Company_Count']}")



# Insight 3 — Industry with highest Environmental score
best_env = industry_stats.sort_values("Avg_Env_Score", ascending=False).iloc[0]
print(f"\n3. MOST ENVIRONMENTALLY FRIENDLY INDUSTRY:")
print(f"   → {best_env['Industry']}")
print(f"   → Average Env Score: {best_env['Avg_Env_Score']}")



# Insight 4 — Industry with highest Social score
best_soc = industry_stats.sort_values("Avg_Social_Score", ascending=False).iloc[0]
print(f"\n4. BEST INDUSTRY FOR SOCIAL RESPONSIBILITY:")
print(f"   → {best_soc['Industry']}")
print(f"   → Average Social Score: {best_soc['Avg_Social_Score']}")



# Insight 5 — Industry with highest Governance score
best_gov = industry_stats.sort_values("Avg_Gov_Score", ascending=False).iloc[0]
print(f"\n5. BEST INDUSTRY FOR GOVERNANCE:")
print(f"   → {best_gov['Industry']}")
print(f"   → Average Gov Score: {best_gov['Avg_Gov_Score']}")



# Insight 6 — Overall ESG score stats
print(f"\n6. OVERALL ESG SCORE STATISTICS:")
print(f"   → Highest ESG Score : {df['Weighted_ESG_Score'].max()}")
print(f"   → Lowest ESG Score  : {df['Weighted_ESG_Score'].min()}")
print(f"   → Average ESG Score : {df['Weighted_ESG_Score'].mean().round(2)}")




# ============================================================
# PART 5 — Save industry comparison results
# ============================================================

industry_stats.to_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_industry.csv", index=False)

print("\n" + "=" * 50)
print("✅ Step 4 Complete!")
print("✅ Industry comparison saved as esg_industry.csv")
print("=" * 50)