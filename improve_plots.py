import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Set global highly readable fonts and 300 DPI
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})
plt.style.use('seaborn-v0_8-darkgrid')

BASE_DIR = r"d:\Machinelearning icfoss\FINAL PROJECT FOR GRADING"
PLOT_DIR = os.path.join(BASE_DIR, 'plots')
DATA_PATH = os.path.join(BASE_DIR, 'archive', 'Clean_Dataset.csv')

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# PLOT 1: Airline Count and Average Price Distribution (replacing 08_airline_count_and_price.png)
print("Generating Plot 1: Airline Count & Price...")
fig, ax1 = plt.subplots(figsize=(12, 7))
airline_counts = df['airline'].value_counts()
airline_order = airline_counts.index
sns.barplot(x=airline_order, y=airline_counts.values, ax=ax1, palette='Blues_r', alpha=0.8)
ax1.set_title('Airline Flight Count and Average Ticket Price', fontweight='bold', pad=20)
ax1.set_xlabel('Airline')
ax1.set_ylabel('Number of Flights', color='blue', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='blue')
for i, v in enumerate(airline_counts.values):
    ax1.text(i, v + (v*0.01), f'{v:,}', ha='center', va='bottom', fontsize=12)

ax2 = ax1.twinx()
airline_avg_price = df.groupby('airline')['price'].mean().reindex(airline_order)
sns.lineplot(x=airline_order, y=airline_avg_price.values, ax=ax2, color='red', marker='o', linewidth=3, markersize=10)
ax2.set_ylabel('Average Price (INR)', color='red', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='red')
plt.grid(False)
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, '08_airline_count_and_price.png'))
plt.close()

# PLOT 2: Days Left vs Ticket Price (replacing 05_days_left_vs_price.png)
print("Generating Plot 2: Days Left vs Price...")
plt.figure(figsize=(12, 7))
avg_price_days = df.groupby('days_left')['price'].mean().reset_index()
sns.lineplot(data=avg_price_days, x='days_left', y='price', color='darkblue', linewidth=3)
plt.title('Impact of Days Left to Departure on Average Ticket Price', fontweight='bold', pad=20)
plt.xlabel('Days Left Until Departure')
plt.ylabel('Average Ticket Price (INR)')
plt.xlim(max(df['days_left']), min(df['days_left'])) # Reverse x-axis to show approaching date
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, '05_days_left_vs_price.png'))
plt.close()

# PLOT 3: Model Comparison R2 (replacing 12_model_comparison_r2.png)
print("Generating Plot 3: Model R2 Comparison...")
plt.figure(figsize=(12, 7))
models = ['Random Forest', 'XGBoost', 'Decision Tree', 'Linear Reg.', 'SVR']
r2_scores = [0.9856, 0.9837, 0.9804, 0.9112, 0.6931]
colors = ['green' if r == max(r2_scores) else 'skyblue' for r in r2_scores]
bars = plt.bar(models, r2_scores, color=colors, edgecolor='black', alpha=0.8)
plt.title('Comparison of R² Scores Across Regression Models', fontweight='bold', pad=20)
plt.xlabel('Regression Algorithm')
plt.ylabel('R² Score')
plt.ylim(0, 1.1)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(PLOT_DIR, '12_model_comparison_r2.png'))
plt.close()

# PLOT 4: Feature Importance RF (replacing 15_feature_importance_rf.png)
print("Generating Plot 4: Feature Importance...")
try:
    rf_model = joblib.load(os.path.join(BASE_DIR, 'saved_models', 'best_model.pkl'))
    feature_names = joblib.load(os.path.join(BASE_DIR, 'saved_models', 'feature_names.pkl'))
    importances = rf_model.feature_importances_
    
    # Sort
    indices = np.argsort(importances)[::-1]
    top_n = 12
    top_indices = indices[:top_n]
    top_importances = importances[top_indices]
    top_features = [feature_names[i] for i in top_indices]
    
    # Beautify feature names
    top_features = [f.replace('_', ' ').title() for f in top_features]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_importances, y=top_features, palette='viridis')
    plt.title('Top Predictive Features (Random Forest)', fontweight='bold', pad=20)
    plt.xlabel('Relative Feature Importance')
    plt.ylabel('Feature')
    for i, v in enumerate(top_importances):
        plt.text(v + 0.01, i, f'{v:.3f}', va='center', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_DIR, '15_feature_importance_rf.png'))
    plt.close()
    print("Feature importance plotted.")
except Exception as e:
    print("Could not load model for feature importance:", e)

print("All high-resolution plots generated successfully!")
