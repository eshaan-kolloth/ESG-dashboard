# ============================================================
# STEP 9 — Real Company Case Study
# Tesla vs Apple vs Microsoft
# ============================================================

# We need these libraries
import pandas as pd                  # for working with data tables
import matplotlib.pyplot as plt      # for creating charts
import numpy as np                   # for math calculations (radar chart)
import seaborn as sns                # for nice chart styling

# ============================================================
# LOAD DATA
# We load the scored data we created in Step 3
# ============================================================

df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv")

print("=" * 60)
print("   CASE STUDY — TESLA vs APPLE vs MICROSOFT")
print("=" * 60)

# ============================================================
# STEP 1 — FIND THE 3 COMPANIES IN OUR DATASET
# We search by ticker symbol (short name like AAPL, MSFT, TSLA)
# ============================================================

# List of tickers we want to find
tickers_we_want = ["tsla", "aapl", "msft"]

# Filter the dataframe to only keep these 3 companies
companies = df[df["Ticker"].str.lower().isin(tickers_we_want)].copy()

# Reset the index so rows are numbered 0, 1, 2
companies = companies.reset_index(drop=True)

print(f"\n We found {len(companies)} companies in the dataset")
print(companies[["Ticker", "Company", "Env_Score",
                  "Social_Score", "Gov_Score",
                  "Weighted_ESG_Score", "ESG_Rank"]])

# ============================================================
# STEP 2 — PRINT DETAILED SCORECARD FOR EACH COMPANY
# Loop through each company and print its scores
# ============================================================

print("\n" + "=" * 60)
print("   DETAILED SCORECARDS")
print("=" * 60)

# Loop means: do this for each company one by one
for i, row in companies.iterrows():

    print(f"\n  Company    : {row['Company']}")
    print(f"  Ticker     : {row['Ticker'].upper()}")
    print(f"  Industry   : {row['Industry']}")
    print(f"  " + "-" * 40)

    # Raw scores (original numbers from dataset)
    print(f"  Env Score      : {row['Env_Score']}")
    print(f"  Social Score   : {row['Social_Score']}")
    print(f"  Gov Score      : {row['Gov_Score']}")
    print(f"  " + "-" * 40)

    # Normalized scores (converted to 0-100 scale)
    print(f"  Env Normalized    : {row['Env_Norm']:.1f} / 100")
    print(f"  Social Normalized : {row['Social_Norm']:.1f} / 100")
    print(f"  Gov Normalized    : {row['Gov_Norm']:.1f} / 100")
    print(f"  " + "-" * 40)

    # Final results
    print(f"  Weighted ESG Score : {row['Weighted_ESG_Score']}")
    print(f"  ESG Grade          : {row['Total_Grade']}")
    print(f"  ESG Category       : {row['ESG_Category']}")
    print(f"  ESG Rank           : #{row['ESG_Rank']} out of 722 companies")

# ============================================================
# STEP 3 — HEAD TO HEAD COMPARISON
# Compare the 3 companies on each pillar
# Show who wins each category
# ============================================================

print("\n" + "=" * 60)
print("   HEAD TO HEAD COMPARISON")
print("=" * 60)

# We compare these 4 things
pillars = ["Env_Score", "Social_Score", "Gov_Score", "Weighted_ESG_Score"]
labels  = ["Environmental", "Social", "Governance", "Overall ESG"]

for pillar, label in zip(pillars, labels):

    # Find which company has the highest score in this pillar
    winner_name = companies.loc[companies[pillar].idxmax(), "Company"]

    # Sort companies highest to lowest for this pillar
    sorted_companies = companies[["Company", pillar]].sort_values(
        pillar, ascending=False
    )

    print(f"\n  {label}:")

    for _, row in sorted_companies.iterrows():
        # Create a simple bar using block characters
        bar_length = int(row[pillar] / 10)
        bar        = "█" * bar_length

        # Add trophy if this company is the winner
        if row["Company"] == winner_name:
            trophy = "  🏆 WINNER"
        else:
            trophy = ""

        print(f"    {row['Company']:<30} {row[pillar]:>8}  {bar}{trophy}")

# ============================================================
# STEP 4 — BUSINESS INSIGHTS
# Written insights about each company's ESG performance
# ============================================================

print("\n" + "=" * 60)
print("   BUSINESS INSIGHTS")
print("=" * 60)

# We store insights in a dictionary
# Key = ticker symbol, Value = list of insight points
insights = {

    "tsla" : [
        "Tesla leads in Environmental score due to its core EV business model.",
        "Social score is the lowest — impacted by workplace safety concerns and labor disputes.",
        "Governance score is moderate — faces criticism for board independence issues.",
        "Despite lower overall ESG rank, Tesla's green energy mission is overwhelmingly positive.",
        "Investors focused purely on environmental impact see Tesla as a strong pick.",
    ],

    "aapl" : [
        "Apple scores moderately across all three ESG pillars.",
        "Governance score is the strongest pillar for Apple.",
        "Apple has committed to 100% carbon neutrality across its supply chain by 2030.",
        "Social score reflects supplier responsibility programs and labor standards.",
        "Considered a balanced and stable ESG investment with low controversy exposure.",
    ],

    "msft" : [
        "Microsoft ranks #2 out of 722 companies — exceptional ESG performance.",
        "Leads all three pillars — Environmental, Social, AND Governance.",
        "Microsoft has pledged to be carbon NEGATIVE by 2030 — a rare commitment.",
        "Strong social score from diversity programs and employee wellbeing initiatives.",
        "Widely regarded as the gold standard for ESG in the technology sector.",
    ],
}

# Loop through each company and print its insights
for i, row in companies.iterrows():

    # Get the ticker in lowercase (e.g. "aapl")
    ticker  = row["Ticker"].lower()
    company = row["Company"]

    # Check if we have insights for this ticker
    if ticker in insights:
        print(f"\n  {company.upper()} ({ticker.upper()}):")
        print(f"  " + "-" * 45)

        # Print each insight point
        for point in insights[ticker]:
            print(f"    • {point}")

# ============================================================
# STEP 5 — WINNER SUMMARY
# One line summary of who wins each category
# ============================================================

print("\n" + "=" * 60)
print("   WINNER SUMMARY")
print("=" * 60)

# Find the winner for each category
best_env  = companies.loc[companies["Env_Score"].idxmax(),          "Company"]
best_soc  = companies.loc[companies["Social_Score"].idxmax(),       "Company"]
best_gov  = companies.loc[companies["Gov_Score"].idxmax(),          "Company"]
best_esg  = companies.loc[companies["Weighted_ESG_Score"].idxmax(), "Company"]
best_rank = companies.loc[companies["ESG_Rank"].idxmin(),           "Company"]

print(f"\n  🌱 Best Environmental Score : {best_env}")
print(f"  👥 Best Social Score        : {best_soc}")
print(f"  🏛️  Best Governance Score    : {best_gov}")
print(f"  🏆 Best Overall ESG Score   : {best_esg}")
print(f"  📊 Best Dataset Rank        : {best_rank}")

# ============================================================
# STEP 6 — CREATE CHARTS
# Chart 1 = Grouped Bar Chart (E, S, G side by side)
# Chart 2 = Radar Chart (spider chart)
# Chart 3 = Overall ESG Score Bar Chart
# ============================================================

# Set a nice style for all charts
sns.set_theme(style="whitegrid")

# Colors for each company
# Blue = Apple, Green = Microsoft, Red = Tesla
apple_color     = "#3498DB"
microsoft_color = "#27AE60"
tesla_color     = "#E74C3C"

# ---- Get individual company rows ----
apple     = companies[companies["Ticker"] == "aapl"].iloc[0]
microsoft = companies[companies["Ticker"] == "msft"].iloc[0]
tesla     = companies[companies["Ticker"] == "tsla"].iloc[0]

# ============================================================
# CHART 1 — Grouped Bar Chart
# Shows E, S, G scores for all 3 companies side by side
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

# x positions for the 3 groups (Environmental, Social, Governance)
x     = np.arange(3)
width = 0.25   # width of each bar

# Create 3 sets of bars — one for each company
apple_bars     = ax.bar(x - width, [apple["Env_Score"],     apple["Social_Score"],     apple["Gov_Score"]],     width, label="Apple Inc",      color=apple_color)
microsoft_bars = ax.bar(x,         [microsoft["Env_Score"], microsoft["Social_Score"], microsoft["Gov_Score"]], width, label="Microsoft Corp", color=microsoft_color)
tesla_bars     = ax.bar(x + width, [tesla["Env_Score"],     tesla["Social_Score"],     tesla["Gov_Score"]],     width, label="Tesla Inc",      color=tesla_color)

# Add score numbers on top of each bar
for all_bars in [apple_bars, microsoft_bars, tesla_bars]:
    for bar in all_bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x position = center of bar
            bar.get_height() + 5,                # y position = just above bar
            str(int(bar.get_height())),          # text = score number
            ha="center", va="bottom",
            fontsize=9, fontweight="bold"
        )

# Labels and title
ax.set_xticks(x)
ax.set_xticklabels(["Environmental", "Social", "Governance"], fontsize=12)
ax.set_ylabel("Raw Score", fontsize=12)
ax.set_title("Tesla vs Apple vs Microsoft — ESG Pillar Comparison",
             fontsize=14, fontweight="bold", pad=15)
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart9_casestudy_bars.png", dpi=150)
plt.show()
print("\n✅ Chart 9 saved — Grouped Bar Chart")

# ============================================================
# CHART 2 — Radar Chart (Spider Chart)
# Shows normalized scores (0-100) in a circular shape
# ============================================================

# Radar chart needs angles for each pillar
categories  = ["Environmental", "Social", "Governance"]
num_pillars = len(categories)   # = 3

# Calculate angle for each pillar (evenly spaced around a circle)
angles  = [n / float(num_pillars) * 2 * np.pi for n in range(num_pillars)]
angles += angles[:1]   # add first angle again to close the circle

# Create the polar (circular) plot
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

# Data for each company (normalized 0-100 scores)
radar_data = [
    ("Apple Inc",      apple["Env_Norm"],     apple["Social_Norm"],     apple["Gov_Norm"],     apple_color),
    ("Microsoft Corp", microsoft["Env_Norm"], microsoft["Social_Norm"], microsoft["Gov_Norm"], microsoft_color),
    ("Tesla Inc",      tesla["Env_Norm"],     tesla["Social_Norm"],     tesla["Gov_Norm"],     tesla_color),
]

# Draw each company's radar shape
for name, env, soc, gov, color in radar_data:
    values  = [env, soc, gov]
    values += values[:1]   # close the shape by repeating first value
    ax.plot(angles, values, linewidth=2, label=name, color=color)
    ax.fill(angles, values, alpha=0.15, color=color)   # fill with transparent color

# Set labels and style
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_title("ESG Radar Chart — Tesla vs Apple vs Microsoft",
             fontsize=14, fontweight="bold", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=10)

plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart10_radar.png", dpi=150)
plt.show()
print("✅ Chart 10 saved — Radar Chart")

# ============================================================
# CHART 3 — Overall ESG Score Bar Chart
# Simple bar chart showing final weighted ESG score
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Sort companies by ESG score (highest first)
sorted_companies = companies.sort_values("Weighted_ESG_Score", ascending=False)

# Assign colors based on ticker
bar_colors = []
for ticker in sorted_companies["Ticker"]:
    if ticker == "aapl":
        bar_colors.append(apple_color)
    elif ticker == "msft":
        bar_colors.append(microsoft_color)
    else:
        bar_colors.append(tesla_color)

# Draw bars
bars = ax.bar(
    sorted_companies["Company"].values,       # x axis = company names
    sorted_companies["Weighted_ESG_Score"].values,  # y axis = ESG score
    color=bar_colors,
    width=0.4,
    edgecolor="white",
    linewidth=1.5
)

# Add score labels on top of each bar
for bar, score in zip(bars, sorted_companies["Weighted_ESG_Score"].values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{score}",
        ha="center", va="bottom",
        fontsize=12, fontweight="bold"
    )

ax.set_ylabel("Weighted ESG Score (0-100)", fontsize=11)
ax.set_title("Overall Weighted ESG Score Comparison",
             fontsize=14, fontweight="bold", pad=15)
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart11_overall.png", dpi=150)
plt.show()
print("✅ Chart 11 saved — Overall ESG Comparison")

# ============================================================
# ALL DONE!
# ============================================================

print("\n" + "=" * 60)
print("✅ Step 9 Complete!")
print("✅ Case Study: Tesla vs Apple vs Microsoft")
print("✅ Charts 9, 10, 11 saved in your ESG_Dashboard folder")
print("=" * 60)