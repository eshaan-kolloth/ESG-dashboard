# ============================================================
# STEP 5 — ESG Dashboard with Matplotlib & Seaborn
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# ---- Load the scored data ----
df       = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv")
industry = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_industry.csv")

# ---- Set a nice style for all charts ----
sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"

print("=" * 50)
print("BUILDING ESG DASHBOARD...")
print("=" * 50)

# ============================================================
# CHART 1 — Top 10 ESG Companies (Horizontal Bar Chart)
# ============================================================

top10 = df.sort_values("Weighted_ESG_Score", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))

# Create horizontal bar chart
bars = ax.barh(
    top10["Company"],           # y axis = company names
    top10["Weighted_ESG_Score"],# x axis = ESG scores
    color=sns.color_palette("Greens_d", len(top10))  # green colors
)

# Add score labels on each bar
for bar, score in zip(bars, top10["Weighted_ESG_Score"]):
    ax.text(
        bar.get_width() - 1,    # x position
        bar.get_y() + bar.get_height() / 2,  # y position
        f"{score}",             # text to show
        va="center", ha="right",
        color="white", fontweight="bold", fontsize=10
    )

ax.set_title("🏆 Top 10 ESG Companies", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Weighted ESG Score (0-100)", fontsize=12)
ax.invert_yaxis()  # highest score at top
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart1_top10.png", dpi=150)
plt.show()
print("✅ Chart 1 saved — Top 10 ESG Companies")

# ============================================================
# CHART 2 — ESG Category Distribution (Pie Chart)
# ============================================================

category_counts = df["ESG_Category"].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))

colors = ["#2ecc71", "#f39c12", "#e74c3c"]  # green, orange, red

wedges, texts, autotexts = ax.pie(
    category_counts.values,
    labels=category_counts.index,
    autopct="%1.1f%%",          # show percentage on each slice
    colors=colors,
    startangle=90,
    explode=[0.05] * len(category_counts),  # slightly separate each slice
    shadow=True
)

# Make text bigger
for text in texts:
    text.set_fontsize(13)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight("bold")

ax.set_title("📊 ESG Category Distribution\n(722 Companies)", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart2_categories.png", dpi=150)
plt.show()
print("✅ Chart 2 saved — ESG Category Distribution")

# ============================================================
# CHART 3 — Top 10 Industries by ESG Score (Bar Chart)
# ============================================================

top10_industry = industry.head(10)

fig, ax = plt.subplots(figsize=(14, 7))

bars = ax.bar(
    top10_industry["Industry"],
    top10_industry["Avg_ESG_Score"],
    color=sns.color_palette("Blues_d", len(top10_industry))
)

# Add score labels on top of each bar
for bar, score in zip(bars, top10_industry["Avg_ESG_Score"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # x position = center of bar
        bar.get_height() + 0.3,              # y position = top of bar
        f"{score}",
        ha="center", va="bottom",
        fontsize=9, fontweight="bold"
    )

ax.set_title("🏭 Top 10 Industries by ESG Score", fontsize=16, fontweight="bold", pad=15)
ax.set_ylabel("Average Weighted ESG Score", fontsize=12)
ax.set_xlabel("Industry", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=9)  # rotate x labels so they don't overlap
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart3_industries.png", dpi=150)
plt.show()
print("✅ Chart 3 saved — Industry Comparison")

# ============================================================
# CHART 4 — Heatmap of E, S, G Scores by Industry
# ============================================================

# Pick top 15 industries for heatmap
top15_industry = industry.head(15).set_index("Industry")

# Select only E, S, G columns
heatmap_data = top15_industry[["Avg_Env_Score", "Avg_Social_Score", "Avg_Gov_Score"]]

# Rename columns for cleaner display
heatmap_data.columns = ["Environmental", "Social", "Governance"]

fig, ax = plt.subplots(figsize=(10, 10))

sns.heatmap(
    heatmap_data,
    annot=True,         # show numbers inside cells
    fmt=".1f",          # format numbers to 1 decimal
    cmap="YlGn",        # yellow to green color scale
    linewidths=0.5,     # lines between cells
    ax=ax,
    cbar_kws={"label": "Score"}
)

ax.set_title("🔥 ESG Heatmap — E, S, G Scores by Industry", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("ESG Pillar", fontsize=12)
ax.set_ylabel("Industry", fontsize=12)
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart4_heatmap.png", dpi=150)
plt.show()
print("✅ Chart 4 saved — ESG Heatmap")

# ============================================================
# CHART 5 — Box Plot: Score Distribution (E, S, G)
# ============================================================

# We need to reshape data for box plot
# melt() converts wide format to long format
plot_data = df[["Env_Score", "Social_Score", "Gov_Score"]].melt(
    var_name="Pillar",    # column name for E/S/G label
    value_name="Score"    # column name for the score value
)

# Rename for cleaner labels
plot_data["Pillar"] = plot_data["Pillar"].replace({
    "Env_Score"    : "Environmental",
    "Social_Score" : "Social",
    "Gov_Score"    : "Governance"
})

fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(
    data=plot_data,
    x="Pillar",
    y="Score",
    palette=["#27ae60", "#3498db", "#9b59b6"],  # green, blue, purple
    ax=ax,
    width=0.5
)

ax.set_title("📦 ESG Score Distribution by Pillar", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("ESG Pillar", fontsize=12)
ax.set_ylabel("Score", fontsize=12)
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart5_boxplot.png", dpi=150)
plt.show()
print("✅ Chart 5 saved — Score Distribution Box Plot")

# ============================================================
# CHART 6 — Combined Dashboard (all charts in one image)
# ============================================================

fig = plt.figure(figsize=(20, 16))
fig.suptitle("ESG Score Analytics Dashboard", fontsize=22, fontweight="bold", y=0.98)

# Create a grid layout — 2 rows, 3 columns
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

# ---- Mini Chart 1 — Top 10 Companies ----
ax1 = fig.add_subplot(gs[0, 0])
ax1.barh(top10["Company"], top10["Weighted_ESG_Score"],
         color=sns.color_palette("Greens_d", len(top10)))
ax1.set_title("Top 10 ESG Companies", fontweight="bold")
ax1.invert_yaxis()
ax1.tick_params(labelsize=7)

# ---- Mini Chart 2 — Pie Chart ----
ax2 = fig.add_subplot(gs[0, 1])
ax2.pie(category_counts.values, labels=category_counts.index,
        autopct="%1.1f%%", colors=colors, startangle=90)
ax2.set_title("ESG Categories", fontweight="bold")

# ---- Mini Chart 3 — Industry Bar Chart ----
ax3 = fig.add_subplot(gs[0, 2])
ax3.bar(range(len(top10_industry)), top10_industry["Avg_ESG_Score"],
        color=sns.color_palette("Blues_d", len(top10_industry)))
ax3.set_title("Top Industries", fontweight="bold")
ax3.set_xticks(range(len(top10_industry)))
ax3.set_xticklabels(top10_industry["Industry"], rotation=90, fontsize=6)

# ---- Mini Chart 4 — Heatmap ----
ax4 = fig.add_subplot(gs[1, 0:2])
sns.heatmap(heatmap_data, annot=True, fmt=".1f",
            cmap="YlGn", linewidths=0.5, ax=ax4,
            annot_kws={"size": 8})
ax4.set_title("ESG Heatmap by Industry", fontweight="bold")
ax4.tick_params(labelsize=8)

# ---- Mini Chart 5 — Box Plot ----
ax5 = fig.add_subplot(gs[1, 2])
sns.boxplot(data=plot_data, x="Pillar", y="Score",
            palette=["#27ae60", "#3498db", "#9b59b6"], ax=ax5, width=0.5)
ax5.set_title("Score Distribution", fontweight="bold")
ax5.tick_params(labelsize=8)

plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart6_full_dashboard.png",
            dpi=150, bbox_inches="tight")
plt.show()
print("✅ Chart 6 saved — Full Dashboard")

print("\n" + "=" * 50)
print("✅ Step 5 Complete!")
print("✅ All charts saved in your ESG_Dashboard folder!")
print("=" * 50)