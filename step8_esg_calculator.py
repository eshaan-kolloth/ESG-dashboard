# ============================================================
# STEP 8 — Interactive ESG Calculator
# ============================================================

import pandas as pd

# ---- Load data for comparison ----
df       = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv")
industry = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_industry.csv")

# ============================================================
# WEIGHTS (same as our model)
# ============================================================
ENV_WEIGHT = 0.40
SOC_WEIGHT = 0.35
GOV_WEIGHT = 0.25

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize(value, min_val, max_val):
    """Convert raw score to 0-100 scale"""
    return round((value - min_val) / (max_val - min_val) * 100, 2)

def calculate_esg(env, soc, gov):
    """Calculate weighted ESG score"""
    # Get min/max from dataset for normalization
    env_norm = normalize(env, df["Env_Score"].min(),    df["Env_Score"].max())
    soc_norm = normalize(soc, df["Social_Score"].min(), df["Social_Score"].max())
    gov_norm = normalize(gov, df["Gov_Score"].min(),    df["Gov_Score"].max())

    # Weighted score
    score = round(
        (env_norm * ENV_WEIGHT) +
        (soc_norm * SOC_WEIGHT) +
        (gov_norm * GOV_WEIGHT), 2
    )
    return score, env_norm, soc_norm, gov_norm

def get_grade(score):
    """Return letter grade based on ESG score"""
    if score >= 80:   return "AAA", "🌟 ESG Leader"
    elif score >= 70: return "AA",  "🌟 ESG Leader"
    elif score >= 60: return "A",   "✅ ESG Average"
    elif score >= 50: return "BBB", "✅ ESG Average"
    elif score >= 40: return "BB",  "✅ ESG Average"
    elif score >= 30: return "B",   "⚠️  ESG Laggard"
    else:             return "CCC", "⚠️  ESG Laggard"

def get_recommendations(env_norm, soc_norm, gov_norm):
    """Give improvement recommendations based on weakest pillar"""
    scores = {
        "Environmental" : env_norm,
        "Social"        : soc_norm,
        "Governance"    : gov_norm
    }
    # Sort by lowest score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1])
    recommendations = []

    for pillar, score in sorted_scores:
        if pillar == "Environmental" and score < 60:
            recommendations.append(
                "🌱 ENVIRONMENTAL: Reduce carbon emissions, invest in "
                "renewable energy, improve waste management policies."
            )
        elif pillar == "Social" and score < 60:
            recommendations.append(
                "👥 SOCIAL: Strengthen employee welfare programs, "
                "improve diversity & inclusion, enhance community engagement."
            )
        elif pillar == "Governance" and score < 60:
            recommendations.append(
                "🏛️  GOVERNANCE: Improve board independence, increase "
                "financial transparency, strengthen anti-corruption policies."
            )
    return recommendations

def compare_to_industry(score, industry_name):
    """Compare company score to industry average"""
    # Find industry in dataset
    match = industry[industry["Industry"].str.lower() == industry_name.lower()]
    if len(match) == 0:
        return None, None
    ind_avg  = match["Avg_ESG_Score"].values[0]
    diff     = round(score - ind_avg, 2)
    return ind_avg, diff

def get_percentile(score):
    """Find what percentile this score is in"""
    percentile = round((df["Weighted_ESG_Score"] < score).mean() * 100, 1)
    return percentile

def print_bar(label, score, max_score=100, width=30):
    """Print a visual progress bar"""
    filled = int((score / max_score) * width)
    bar    = "█" * filled + "░" * (width - filled)
    print(f"  {label:<16} |{bar}| {score:.1f}/100")

# ============================================================
# MAIN CALCULATOR LOOP
# ============================================================

def run_calculator():

    print("\n" + "=" * 60)
    print("       ESG SCORE CALCULATOR — INTERACTIVE TOOL")
    print("=" * 60)
    print("  Calculate your company's ESG score, compare to")
    print("  industry benchmarks, and get improvement tips.")
    print("=" * 60)

    while True:

        print("\n" + "-" * 60)
        print("  ENTER YOUR COMPANY DETAILS")
        print("-" * 60)

        # ---- Get company name ----
        company_name = input("\n  Company Name : ").strip()
        if not company_name:
            company_name = "Your Company"

        # ---- Get industry ----
        print("\n  Available Industries (type exactly or press Enter to skip):")
        industries = sorted(industry["Industry"].unique())
        for i, ind in enumerate(industries):
            print(f"    {i+1:>2}. {ind}")

        industry_name = input("\n  Your Industry : ").strip()

        # ---- Get scores ----
        print("\n  Enter raw ESG scores (valid ranges below):")
        print(f"    Environmental Score : {int(df['Env_Score'].min())} — {int(df['Env_Score'].max())}")
        print(f"    Social Score        : {int(df['Social_Score'].min())} — {int(df['Social_Score'].max())}")
        print(f"    Governance Score    : {int(df['Gov_Score'].min())} — {int(df['Gov_Score'].max())}")

        # ---- Input validation ----
        try:
            env_score = float(input("\n  Environmental Score : "))
            soc_score = float(input("  Social Score        : "))
            gov_score = float(input("  Governance Score    : "))
        except ValueError:
            print("\n  ❌ Invalid input! Please enter numbers only.")
            continue

        # ---- Clamp scores to valid range ----
        env_score = max(df["Env_Score"].min(),    min(env_score, df["Env_Score"].max()))
        soc_score = max(df["Social_Score"].min(), min(soc_score, df["Social_Score"].max()))
        gov_score = max(df["Gov_Score"].min(),    min(gov_score, df["Gov_Score"].max()))

        # ============================================================
        # CALCULATE
        # ============================================================
        esg_score, env_norm, soc_norm, gov_norm = calculate_esg(
            env_score, soc_score, gov_score
        )
        grade, category  = get_grade(esg_score)
        percentile       = get_percentile(esg_score)
        recommendations  = get_recommendations(env_norm, soc_norm, gov_norm)

        # ============================================================
        # DISPLAY RESULTS
        # ============================================================
        print("\n")
        print("=" * 60)
        print(f"   ESG SCORECARD — {company_name.upper()}")
        print("=" * 60)

        print(f"\n  {'Weighted ESG Score':<25} : {esg_score} / 100")
        print(f"  {'ESG Grade':<25} : {grade}")
        print(f"  {'ESG Category':<25} : {category}")
        print(f"  {'Percentile Rank':<25} : Top {100 - percentile}% of all companies")

        # ---- Score Breakdown ----
        print("\n  SCORE BREAKDOWN (Normalized 0-100):")
        print("  " + "-" * 50)
        print_bar("Environmental", env_norm)
        print_bar("Social",        soc_norm)
        print_bar("Governance",    gov_norm)
        print_bar("FINAL ESG",     esg_score)

        # ---- Weighted Contribution ----
        print("\n  WEIGHTED CONTRIBUTION TO FINAL SCORE:")
        print("  " + "-" * 50)
        env_contrib = round(env_norm * ENV_WEIGHT, 2)
        soc_contrib = round(soc_norm * SOC_WEIGHT, 2)
        gov_contrib = round(gov_norm * GOV_WEIGHT, 2)
        print(f"  Environmental  : {env_norm:.1f} x 40% = {env_contrib}")
        print(f"  Social         : {soc_norm:.1f} x 35% = {soc_contrib}")
        print(f"  Governance     : {gov_norm:.1f} x 25% = {gov_contrib}")
        print(f"  {'─'*35}")
        print(f"  Final Score    :              = {esg_score}")

        # ---- Industry Comparison ----
        if industry_name:
            ind_avg, diff = compare_to_industry(esg_score, industry_name)
            if ind_avg is not None:
                print(f"\n  INDUSTRY COMPARISON — {industry_name.upper()}:")
                print("  " + "-" * 50)
                print(f"  Your ESG Score     : {esg_score}")
                print(f"  Industry Average   : {ind_avg}")
                if diff > 0:
                    print(f"  Difference         : +{diff} ✅ ABOVE industry average")
                elif diff < 0:
                    print(f"  Difference         : {diff} ⚠️  BELOW industry average")
                else:
                    print(f"  Difference         : {diff} — Exactly at industry average")
            else:
                print(f"\n  ⚠️  Industry '{industry_name}' not found in dataset.")

        # ---- Recommendations ----
        if recommendations:
            print(f"\n  IMPROVEMENT RECOMMENDATIONS:")
            print("  " + "-" * 50)
            for rec in recommendations:
                print(f"  {rec}")
        else:
            print(f"\n  ✅ Excellent! All pillars are performing well.")

        # ---- Find similar companies ----
        print(f"\n  SIMILAR COMPANIES IN DATASET (closest ESG scores):")
        print("  " + "-" * 50)
        df["score_diff"] = abs(df["Weighted_ESG_Score"] - esg_score)
        similar = df.nsmallest(3, "score_diff")[["Company", "Industry", "Weighted_ESG_Score"]]
        for _, row in similar.iterrows():
            print(f"  {row['Company']:<35} | {row['Industry']:<25} | {row['Weighted_ESG_Score']}")

        print("\n" + "=" * 60)

        # ---- Ask to continue ----
        again = input("\n  Calculate another company? (yes / no) : ").strip().lower()
        if again not in ["yes", "y"]:
            print("\n  Thank you for using the ESG Calculator! 👋")
            print("=" * 60)
            break

# ---- Run the calculator ----
run_calculator()