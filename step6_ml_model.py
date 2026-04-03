# ============================================================
# STEP 6 — ML Prediction Model using Scikit-learn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score




# ---- Load the scored data ----
df = pd.read_csv(r"C:\Users\eshaa\Desktop\ESG_Dashboard\esg_scored.csv")

print("=" * 50)
print("ML PREDICTION MODEL — ESG SCORE PREDICTOR")
print("=" * 50)




# ============================================================
# PART 1 — Prepare the Data
# X = input features (what we give the model)
# y = output target (what we want to predict)
# ============================================================

X = df[["Env_Score", "Social_Score", "Gov_Score"]]
y = df["Weighted_ESG_Score"]

print(f"\n✅ Features (X): {list(X.columns)}")
print(f"✅ Target  (y): Weighted_ESG_Score")
print(f"✅ Total samples: {len(X)}")





# ============================================================
# PART 2 — Split data into Training and Testing sets
# 80% for training, 20% for testing
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print(f"\n✅ Training samples : {len(X_train)} (80%)")
print(f"✅ Testing samples  : {len(X_test)} (20%)")




# ============================================================
# PART 3 — Scale the features using StandardScaler
# ============================================================

scaler         = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("\n✅ Features scaled using StandardScaler")




# ============================================================
# PART 4 — Train TWO models
# Model 1 = Linear Regression
# Model 2 = Random Forest
# ============================================================

# --- Model 1: Linear Regression ---
lr_model      = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
lr_predictions = lr_model.predict(X_test_scaled)

# --- Model 2: Random Forest ---
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X_train_scaled, y_train)
rf_predictions = rf_model.predict(X_test_scaled)

print("\n✅ Both models trained successfully")





# ============================================================
# PART 5 — Evaluate both models
# MAE = Mean Absolute Error (lower is better)
# R2  = Accuracy score (higher is better, max = 1.0)
# ============================================================

lr_mae = round(mean_absolute_error(y_test, lr_predictions), 4)
lr_r2  = round(r2_score(y_test, lr_predictions), 4)

rf_mae = round(mean_absolute_error(y_test, rf_predictions), 4)
rf_r2  = round(r2_score(y_test, rf_predictions), 4)

print("\n" + "=" * 50)
print("📊 MODEL PERFORMANCE COMPARISON:")
print("=" * 50)
print(f"\n  Linear Regression:")
print(f"    MAE (error)    : {lr_mae}  (lower = better)")
print(f"    R2  (accuracy) : {lr_r2}   (higher = better, max=1)")

print(f"\n  Random Forest:")
print(f"    MAE (error)    : {rf_mae}  (lower = better)")
print(f"    R2  (accuracy) : {rf_r2}   (higher = better, max=1)")

# Pick the better model
if rf_r2 > lr_r2:
    print(f"\n🏆 WINNER: Random Forest is more accurate!")
    best_model       = rf_model
    best_predictions = rf_predictions
    best_name        = "Random Forest"
else:
    print(f"\n🏆 WINNER: Linear Regression is more accurate!")
    best_model       = lr_model
    best_predictions = lr_predictions
    best_name        = "Linear Regression"





# ============================================================
# PART 6 — Feature Importance
# Which score matters most for prediction?
# ============================================================

feature_importance = pd.Series(
    rf_model.feature_importances_,
    index=["Env_Score", "Social_Score", "Gov_Score"]
).sort_values(ascending=False)

print("\n" + "=" * 50)
print("🔍 FEATURE IMPORTANCE (Random Forest):")
print("=" * 50)
for feature, importance in feature_importance.items():
    print(f"  {feature:<20} : {round(importance * 100, 2)}%")





# ============================================================
# PART 7 — Predict ESG score for a NEW company
# ============================================================

print("\n" + "=" * 50)
print("🔮 PREDICTING ESG SCORE FOR A NEW COMPANY:")
print("=" * 50)

new_company = pd.DataFrame({
    "Env_Score"    : [450],
    "Social_Score" : [320],
    "Gov_Score"    : [280]
})

new_scaled    = scaler.transform(new_company)
predicted_esg = round(best_model.predict(new_scaled)[0], 2)

print(f"\n  Input:")
print(f"    Env_Score    : 450")
print(f"    Social_Score : 320")
print(f"    Gov_Score    : 280")
print(f"\n  Predicted Weighted ESG Score : {predicted_esg}")

if predicted_esg >= 60:
    print(f"  Category : 🌟 ESG Leader")
elif predicted_esg >= 40:
    print(f"  Category : ✅ ESG Average")
else:
    print(f"  Category : ⚠️ ESG Laggard")





# ============================================================
# PART 8 — Plot Actual vs Predicted
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("ML Model — Actual vs Predicted ESG Scores",
             fontsize=16, fontweight="bold")



# Chart 1 — Linear Regression
axes[0].scatter(y_test, lr_predictions, alpha=0.5, color="#3498db")
axes[0].plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--", linewidth=2, label="Perfect Prediction"
)
axes[0].set_title(f"Linear Regression\nR² = {lr_r2}", fontsize=13)
axes[0].set_xlabel("Actual ESG Score")
axes[0].set_ylabel("Predicted ESG Score")
axes[0].legend()




# Chart 2 — Random Forest
axes[1].scatter(y_test, rf_predictions, alpha=0.5, color="#27ae60")
axes[1].plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--", linewidth=2, label="Perfect Prediction"
)
axes[1].set_title(f"Random Forest\nR² = {rf_r2}", fontsize=13)
axes[1].set_xlabel("Actual ESG Score")
axes[1].set_ylabel("Predicted ESG Score")
axes[1].legend()

plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart7_ml_predictions.png", dpi=150)
plt.show()
print("\n✅ Chart 7 saved — ML Predictions")






# ============================================================
# PART 9 — Feature Importance Chart
# ============================================================

fig, ax = plt.subplots(figsize=(8, 5))
colors  = ["#27ae60", "#3498db", "#9b59b6"]
bars    = ax.bar(
    feature_importance.index,
    feature_importance.values * 100,
    color=colors
)

for bar, val in zip(bars, feature_importance.values * 100):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{val:.1f}%",
        ha="center", fontweight="bold"
    )

ax.set_title("🔍 Feature Importance — Which Score Matters Most?",
             fontsize=14, fontweight="bold")
ax.set_ylabel("Importance (%)")
ax.set_xlabel("ESG Pillar")
plt.tight_layout()
plt.savefig(r"C:\Users\eshaa\Desktop\ESG_Dashboard\chart8_feature_importance.png", dpi=150)
plt.show()
print("✅ Chart 8 saved — Feature Importance")

print("\n" + "=" * 50)
print("✅ Step 6 Complete!")
print(f"✅ Best Model: {best_name}")
print("✅ Charts saved in ESG_Dashboard folder")
print("=" * 50)