"""
==============================================================================
 FLIGHT FARE PREDICTION — Complete Machine Learning Project
==============================================================================

 Dataset: Flight Price Prediction (Kaggle)
 Source : https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction
 Files  : Clean_Dataset.csv (300,153 rows × 12 columns)
          economy.csv, business.csv (raw data by class)

 Problem Type : Regression (predicting continuous flight price in INR)
 Target Column: price

 Features:
   airline          – Name of the airline (6 unique)
   flight           – Flight code
   source_city      – Departure city (6 unique)
   departure_time   – Time category (Early_Morning, Morning, Afternoon, etc.)
   stops            – Number of stops (zero, one, two_or_more)
   arrival_time     – Arrival time category
   destination_city – Arrival city (6 unique)
   class            – Economy or Business
   duration         – Flight duration in hours
   days_left        – Days between booking and travel date
   price            – Ticket price in INR (TARGET)

 Algorithms Implemented:
   1. Linear Regression      (baseline)
   2. Decision Tree Regressor
   3. Random Forest Regressor (Bagging)
   4. XGBoost Regressor       (Boosting)
   5. Support Vector Regressor (SVR — RBF kernel)
   6. K-Means Clustering       (Unsupervised)

 Author : Karthik KS
 Date   : June 2025
==============================================================================
"""

# ── Standard library ────────────────────────────────────────────────────────
import os
import sys
import io
import warnings

# Force stdout/stderr to use UTF-8 to prevent encoding errors on Windows terminal
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
results_file_path = os.path.join(BASE_DIR, 'results.txt')
f_results = open(results_file_path, 'w', encoding='utf-8')

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()
    def flush(self):
        for f in self.files:
            f.flush()

sys.stdout = Tee(sys.stdout, f_results)
sys.stderr = Tee(sys.stderr, f_results)

# ── Data manipulation ───────────────────────────────────────────────────────
import numpy as np
import pandas as pd

# ── Visualization ───────────────────────────────────────────────────────────
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ── Scikit-learn: preprocessing & metrics ───────────────────────────────────
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ── Scikit-learn: models ────────────────────────────────────────────────────
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# ── XGBoost ─────────────────────────────────────────────────────────────────
from xgboost import XGBRegressor

# ── Model persistence ──────────────────────────────────────────────────────
import joblib

# ── Global settings ────────────────────────────────────────────────────────
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
np.random.seed(42)

# Create output directories
PLOT_DIR = os.path.join(BASE_DIR, 'plots')
MODEL_DIR = os.path.join(BASE_DIR, 'saved_models')
os.makedirs(PLOT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)


def save_plot(fig, filename):
    """Save a matplotlib figure to the plots/ directory."""
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"   ✅ Plot saved → {path}")


# ════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING & INITIAL EXPLORATION
# ════════════════════════════════════════════════════════════════════════════
print('=' * 70)
print('   SECTION 1 — DATA LOADING & INITIAL EXPLORATION')
print('=' * 70)

data_path = os.path.join(BASE_DIR, 'archive', 'Clean_Dataset.csv')
df = pd.read_csv(data_path)

if 'Unnamed: 0' in df.columns:
    df.drop('Unnamed: 0', axis=1, inplace=True)

print(f"\n✅ Dataset loaded from: {data_path}")
print(f"\n📊 Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

print(f"\n--- First 5 Rows ---")
print(df.head().to_string())

print(f"\n--- Data Types ---")
print(df.dtypes)

print(f"\n--- Statistical Summary ---")
print(df.describe().to_string())

print(f"\n--- Categorical Feature Unique Values ---")
for col in df.select_dtypes(include='object').columns:
    print(f"   {col}: {df[col].unique()}")

print(f"\n--- Missing Values ---")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "   No missing values found! ✅")

print(f"\n--- Class Distribution ---")
print(f"   Economy : {(df['class'] == 'Economy').sum():,}")
print(f"   Business: {(df['class'] == 'Business').sum():,}")


# ════════════════════════════════════════════════════════════════════════════
# 2. EXPLORATORY DATA ANALYSIS (EDA)
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 2 — EXPLORATORY DATA ANALYSIS (EDA)')
print('=' * 70)

# --- 2a. Distribution of Flight Prices ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(df['price'], bins=60, color='steelblue', edgecolor='white', alpha=0.85)
axes[0].set_title('Distribution of Flight Prices', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Price (INR)')
axes[0].set_ylabel('Frequency')
axes[0].axvline(df['price'].mean(), color='red', linestyle='--', label=f"Mean: ₹{df['price'].mean():,.0f}")
axes[0].axvline(df['price'].median(), color='green', linestyle='--', label=f"Median: ₹{df['price'].median():,.0f}")
axes[0].legend()

sns.kdeplot(data=df, x='price', hue='class', ax=axes[1], fill=True, alpha=0.35, linewidth=2)
axes[1].set_title('Price Density by Class (Economy vs Business)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Price (INR)')
fig.suptitle('Flight Price Distribution Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
save_plot(fig, '01_price_distribution.png')

# --- 2b. Airline vs Price ---
fig, ax = plt.subplots(figsize=(14, 7))
airline_order = df.groupby('airline')['price'].median().sort_values(ascending=False).index
sns.boxplot(x='airline', y='price', data=df, order=airline_order, ax=ax, palette='coolwarm')
ax.set_title('Airline vs Flight Price', fontsize=16, fontweight='bold')
ax.set_xlabel('Airline', fontsize=12)
ax.set_ylabel('Price (INR)', fontsize=12)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
save_plot(fig, '02_airline_vs_price.png')

# --- 2c. Source & Destination Analysis ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
df.groupby('source_city')['price'].mean().sort_values(ascending=False).plot(
    kind='bar', ax=axes[0], color=sns.color_palette('magma', n_colors=6), edgecolor='white')
axes[0].set_title('Average Price by Source City', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Avg Price (INR)')
axes[0].tick_params(axis='x', rotation=45)

df.groupby('destination_city')['price'].mean().sort_values(ascending=False).plot(
    kind='bar', ax=axes[1], color=sns.color_palette('plasma', n_colors=6), edgecolor='white')
axes[1].set_title('Average Price by Destination City', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Avg Price (INR)')
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout()
save_plot(fig, '03_source_destination_price.png')

# --- 2d. Number of Stops vs Price ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(x='stops', y='price', data=df, ax=ax, palette='Set2',
               order=['zero', 'one', 'two_or_more'], inner='box')
ax.set_title('Number of Stops vs Flight Price', fontsize=16, fontweight='bold')
ax.set_xlabel('Number of Stops')
ax.set_ylabel('Price (INR)')
plt.tight_layout()
save_plot(fig, '04_stops_vs_price.png')

# --- 2e. Days Left vs Price ---
fig, ax = plt.subplots(figsize=(12, 6))
days_price = df.groupby('days_left')['price'].mean()
ax.plot(days_price.index, days_price.values, 'o-', color='crimson', linewidth=2, markersize=4)
ax.set_xlabel('Days Left Before Departure', fontsize=13)
ax.set_ylabel('Average Price (INR)', fontsize=13)
ax.set_title('How Ticket Price Changes with Booking Timing', fontsize=16, fontweight='bold')
ax.axvspan(1, 5, alpha=0.15, color='red', label='Last-minute (expensive)')
ax.axvspan(15, 40, alpha=0.1, color='green', label='Sweet spot (cheaper)')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_plot(fig, '05_days_left_vs_price.png')

# --- 2f. Departure Time vs Price ---
fig, ax = plt.subplots(figsize=(12, 6))
time_order = ['Early_Morning', 'Morning', 'Afternoon', 'Evening', 'Night', 'Late_Night']
available_times = [t for t in time_order if t in df['departure_time'].unique()]
sns.boxplot(x='departure_time', y='price', data=df, order=available_times,
            ax=ax, palette='RdYlBu')
ax.set_title('Departure Time vs Flight Price', fontsize=16, fontweight='bold')
ax.set_xlabel('Departure Time', fontsize=12)
ax.set_ylabel('Price (INR)', fontsize=12)
plt.xticks(rotation=30)
plt.tight_layout()
save_plot(fig, '06_departure_time_vs_price.png')

# --- 2g. Duration vs Price (scatter) ---
fig, ax = plt.subplots(figsize=(10, 6))
sample = df.sample(n=min(5000, len(df)), random_state=42)
scatter = ax.scatter(sample['duration'], sample['price'], c=sample['price'],
                     cmap='YlOrRd', alpha=0.5, s=10, edgecolors='none')
plt.colorbar(scatter, ax=ax, label='Price (INR)')
ax.set_xlabel('Duration (hours)', fontsize=13)
ax.set_ylabel('Price (INR)', fontsize=13)
ax.set_title('Flight Duration vs Price', fontsize=16, fontweight='bold')
plt.tight_layout()
save_plot(fig, '07_duration_vs_price.png')

# --- 2h. Airline Market Share + Avg Price ---
fig, ax1 = plt.subplots(figsize=(12, 6))
airline_stats = df.groupby('airline').agg(count=('price', 'size'), avg_price=('price', 'mean'))
airline_stats = airline_stats.sort_values('count', ascending=False)

color1, color2 = '#2196F3', '#FF5722'
bars = ax1.bar(airline_stats.index, airline_stats['count'], color=color1, alpha=0.7, label='Number of Flights')
ax1.set_ylabel('Number of Flights', color=color1, fontsize=12)
ax1.tick_params(axis='x', rotation=30)
ax2 = ax1.twinx()
ax2.plot(airline_stats.index, airline_stats['avg_price'], color=color2, marker='o',
         linewidth=2.5, markersize=10, label='Avg Price')
ax2.set_ylabel('Average Price (INR)', color=color2, fontsize=12)
ax1.set_title('Airline: Flight Count & Average Price', fontsize=16, fontweight='bold')
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.92))
plt.tight_layout()
save_plot(fig, '08_airline_count_and_price.png')

# --- 2i. Class-wise price comparison ---
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='airline', y='price', hue='class', data=df, ax=ax, palette='Set1',
            order=airline_order, ci=None)
ax.set_title('Economy vs Business Price by Airline', fontsize=16, fontweight='bold')
ax.set_xlabel('Airline')
ax.set_ylabel('Average Price (INR)')
plt.xticks(rotation=30, ha='right')
plt.legend(title='Class')
plt.tight_layout()
save_plot(fig, '09_class_comparison.png')


# ════════════════════════════════════════════════════════════════════════════
# 3. DATA PREPROCESSING
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 3 — DATA PREPROCESSING')
print('=' * 70)

# --- 3a. Handle missing values ---
print("\n🔧 Checking & handling missing values...")
df.dropna(inplace=True)
print(f"   Shape after handling: {df.shape}")

# --- 3b. Drop flight code ---
print("🔧 Dropping 'flight' column (1,561 unique codes — too granular)...")
df.drop('flight', axis=1, inplace=True)

# --- 3c. Encode 'stops' as ordinal ---
print("🔧 Encoding 'stops' as ordinal (zero=0, one=1, two_or_more=2)...")
stops_map = {'zero': 0, 'one': 1, 'two_or_more': 2}
df['stops'] = df['stops'].map(stops_map)
print(f"   ✅ Mapping: {stops_map}")

# --- 3d. Encode 'class' as binary ---
print("🔧 Encoding 'class' (Economy=0, Business=1)...")
df['class'] = df['class'].map({'Economy': 0, 'Business': 1})

# --- 3e. Encode departure_time and arrival_time as ordinal ---
print("🔧 Encoding time categories...")
time_map = {'Early_Morning': 0, 'Morning': 1, 'Afternoon': 2,
            'Evening': 3, 'Night': 4, 'Late_Night': 5}
df['departure_time'] = df['departure_time'].map(time_map)
df['arrival_time'] = df['arrival_time'].map(time_map)
print(f"   ✅ Time mapping: {time_map}")

# --- 3f. One-Hot Encode nominal features ---
print("🔧 One-Hot Encoding: airline, source_city, destination_city...")
df = pd.get_dummies(df, columns=['airline', 'source_city', 'destination_city'],
                    drop_first=True, dtype=int)
print(f"   ✅ Columns after encoding: {df.shape[1]}")

# --- 3g. Remove outliers using IQR on Price ---
print("🔧 Removing outliers (IQR method on Price)...")
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
before = df.shape[0]
df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
print(f"   IQR: {IQR:,.0f} | Bounds: [{lower_bound:,.0f}, {upper_bound:,.0f}]")
print(f"   Removed {before - df.shape[0]:,} outliers. Remaining: {df.shape[0]:,} rows")

# --- 3h. Correlation Heatmap ---
print("🔧 Generating correlation heatmap...")
numeric_df = df.select_dtypes(include=[np.number])
top_corr_cols = numeric_df.corr()['price'].abs().sort_values(ascending=False).head(15).index.tolist()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(numeric_df[top_corr_cols].corr(), annot=True, fmt='.2f', cmap='RdYlBu_r',
            linewidths=0.5, ax=ax, square=True, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap (Top 15 Features vs Price)', fontsize=16, fontweight='bold')
plt.tight_layout()
save_plot(fig, '10_correlation_heatmap.png')

# --- 3i. Feature / Target Split ---
X = df.drop('price', axis=1)
y = df['price']
feature_names = X.columns.tolist()
print(f"\n📐 Feature matrix: {X.shape}   |   Target vector: {y.shape}")
print(f"   Features: {feature_names}")

# --- 3j. Train-Test Split (80/20) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42)
print(f"\n   Training set : {X_train.shape[0]:,} samples")
print(f"   Testing set  : {X_test.shape[0]:,} samples")

# --- 3k. Feature Scaling ---
print("🔧 Applying StandardScaler...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   ✅ Scaling complete.\n")


# ════════════════════════════════════════════════════════════════════════════
# 4. MODEL TRAINING & EVALUATION
# ════════════════════════════════════════════════════════════════════════════
print('=' * 70)
print('   SECTION 4 — MODEL TRAINING & EVALUATION')
print('=' * 70)


def evaluate_model(name, model, X_tr, X_te, y_tr, y_te, use_scaled=False):
    """Train a model, predict, and return evaluation metrics."""
    xtr = X_train_scaled if use_scaled else X_tr
    xte = X_test_scaled if use_scaled else X_te
    model.fit(xtr, y_tr)
    y_pred = model.predict(xte)
    mae = mean_absolute_error(y_te, y_pred)
    rmse = np.sqrt(mean_squared_error(y_te, y_pred))
    r2 = r2_score(y_te, y_pred)
    print(f"\n   🏷️  {name}")
    print(f"      MAE  = ₹{mae:,.2f}")
    print(f"      RMSE = ₹{rmse:,.2f}")
    print(f"      R²   = {r2:.4f}  ({r2 * 100:.2f}%)")
    return {'Model': name, 'MAE': mae, 'RMSE': rmse, 'R2_Score': r2,
            'Predictions': y_pred, 'Trained_Model': model}


results = []

# ── 4a. Linear Regression (baseline) ───────────────────────────────────────
print("\n── Training Linear Regression (baseline)...")
lr = LinearRegression()
results.append(evaluate_model('Linear Regression', lr, X_train, X_test, y_train, y_test))

# ── 4b. Decision Tree Regressor ────────────────────────────────────────────
print("\n── Training Decision Tree Regressor...")
dt = DecisionTreeRegressor(max_depth=20, min_samples_split=10, random_state=42)
results.append(evaluate_model('Decision Tree', dt, X_train, X_test, y_train, y_test))

# ── 4c. Random Forest Regressor (BAGGING) ──────────────────────────────────
print("\n── Training Random Forest Regressor (Bagging - 200 trees)...")
rf = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_split=5,
                           n_jobs=-1, random_state=42)
results.append(evaluate_model('Random Forest', rf, X_train, X_test, y_train, y_test))

# ── 4d. XGBoost Regressor (BOOSTING) ───────────────────────────────────────
print("\n── Training XGBoost Regressor (Boosting - 300 trees)...")
xgb = XGBRegressor(n_estimators=300, max_depth=8, learning_rate=0.1,
                   subsample=0.8, colsample_bytree=0.8,
                   random_state=42, verbosity=0)
results.append(evaluate_model('XGBoost', xgb, X_train, X_test, y_train, y_test))

# ── 4e. Support Vector Regressor (SVR) ─────────────────────────────────────
print("\n── Training SVR (RBF kernel) — using 10,000 sample for speed...")
svr_sample_size = 10000
sample_indices = np.random.choice(len(X_train_scaled), size=svr_sample_size, replace=False)
X_train_svr = X_train_scaled[sample_indices]
y_train_svr = y_train.iloc[sample_indices]
svr = SVR(kernel='rbf', C=100, epsilon=0.1, gamma='scale')
svr.fit(X_train_svr, y_train_svr)
svr_pred = svr.predict(X_test_scaled)
svr_mae = mean_absolute_error(y_test, svr_pred)
svr_rmse = np.sqrt(mean_squared_error(y_test, svr_pred))
svr_r2 = r2_score(y_test, svr_pred)
print(f"\n   🏷️  SVR (RBF)")
print(f"      MAE  = ₹{svr_mae:,.2f}")
print(f"      RMSE = ₹{svr_rmse:,.2f}")
print(f"      R²   = {svr_r2:.4f}  ({svr_r2 * 100:.2f}%)")
results.append({'Model': 'SVR (RBF)', 'MAE': svr_mae, 'RMSE': svr_rmse,
                'R2_Score': svr_r2, 'Predictions': svr_pred, 'Trained_Model': svr})


# ════════════════════════════════════════════════════════════════════════════
# 5. MODEL COMPARISON
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 5 — MODEL COMPARISON')
print('=' * 70)

comparison_df = pd.DataFrame([{k: v for k, v in r.items()
                                if k in ['Model', 'MAE', 'RMSE', 'R2_Score']}
                               for r in results])
comparison_df = comparison_df.sort_values('R2_Score', ascending=False).reset_index(drop=True)
print("\n📊 Model Comparison Table:\n")
print(comparison_df.to_string(index=False))

best_idx = comparison_df['R2_Score'].idxmax()
best_model_name = comparison_df.loc[best_idx, 'Model']
print(f"\n🏆 BEST MODEL: {best_model_name}  (R² = {comparison_df.loc[best_idx, 'R2_Score']:.4f})")

# --- Bar chart: R² Scores ---
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#2ecc71' if m == best_model_name else '#3498db' for m in comparison_df['Model']]
bars = ax.barh(comparison_df['Model'], comparison_df['R2_Score'], color=colors,
               edgecolor='white', height=0.55)
ax.set_xlabel('R² Score', fontsize=13)
ax.set_title('Model Comparison — R² Score (higher is better)', fontsize=16, fontweight='bold')
for bar, val in zip(bars, comparison_df['R2_Score']):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
            f'{val:.4f}', va='center', fontsize=11, fontweight='bold')
ax.set_xlim(0, min(comparison_df['R2_Score'].max() * 1.15, 1.05))
plt.tight_layout()
save_plot(fig, '12_model_comparison_r2.png')

# --- Bar chart: MAE ---
fig, ax = plt.subplots(figsize=(12, 6))
colors_mae = ['#e74c3c' if m == best_model_name else '#e67e22' for m in comparison_df['Model']]
bars = ax.barh(comparison_df['Model'], comparison_df['MAE'], color=colors_mae,
               edgecolor='white', height=0.55)
ax.set_xlabel('Mean Absolute Error (INR)', fontsize=13)
ax.set_title('Model Comparison — MAE (lower is better)', fontsize=16, fontweight='bold')
for bar, val in zip(bars, comparison_df['MAE']):
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height() / 2,
            f'₹{val:,.0f}', va='center', fontsize=11, fontweight='bold')
plt.tight_layout()
save_plot(fig, '13_model_comparison_mae.png')

# --- Grouped bar chart: All Metrics Overview ---
fig, ax = plt.subplots(figsize=(14, 7))
x = np.arange(len(comparison_df))
w = 0.25
ax.bar(x - w, comparison_df['MAE'] / 1000, width=w, label='MAE (×1000 INR)', color='#e74c3c', alpha=0.85)
ax.bar(x, comparison_df['RMSE'] / 1000, width=w, label='RMSE (×1000 INR)', color='#f39c12', alpha=0.85)
ax.bar(x + w, comparison_df['R2_Score'] * 10, width=w, label='R² (×10)', color='#2ecc71', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(comparison_df['Model'], rotation=30, ha='right')
ax.set_title('All Models — Metrics Overview', fontsize=16, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
save_plot(fig, '14_all_metrics_overview.png')


# ════════════════════════════════════════════════════════════════════════════
# 6. FEATURE IMPORTANCE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 6 — FEATURE IMPORTANCE')
print('=' * 70)


def plot_feature_importance(model, model_name, feature_names, top_n=15):
    """Plot top-N feature importances for tree-based models."""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    top_features = [feature_names[i] for i in indices]
    top_importances = importances[indices]

    fig, ax = plt.subplots(figsize=(10, 7))
    palette = sns.color_palette('viridis', n_colors=top_n)[::-1]
    ax.barh(range(top_n), top_importances[::-1], color=palette, edgecolor='white')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_features[::-1], fontsize=11)
    ax.set_xlabel('Importance Score', fontsize=12)
    ax.set_title(f'{model_name} — Top {top_n} Feature Importances', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig, top_features, top_importances


# Random Forest feature importance
rf_model = [r for r in results if r['Model'] == 'Random Forest'][0]['Trained_Model']
fig, rf_top_features, rf_importances = plot_feature_importance(rf_model, 'Random Forest', feature_names)
save_plot(fig, '15_feature_importance_rf.png')

# XGBoost feature importance
xgb_model = [r for r in results if r['Model'] == 'XGBoost'][0]['Trained_Model']
fig, xgb_top_features, xgb_importances = plot_feature_importance(xgb_model, 'XGBoost', feature_names)
save_plot(fig, '16_feature_importance_xgb.png')

print("\n   📋 Key Findings — Factors Influencing Ticket Prices:")
print("   " + "-" * 50)
for i, (feat, imp) in enumerate(zip(rf_top_features[:5], rf_importances[:5]), 1):
    print(f"   {i}. {feat:30s} → Importance: {imp:.4f}")
print("   " + "-" * 50)


# ════════════════════════════════════════════════════════════════════════════
# 7. BEST MODEL VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 7 — BEST MODEL VISUALIZATIONS')
print('=' * 70)

best_result = [r for r in results if r['Model'] == best_model_name][0]
y_pred_best = best_result['Predictions']

# --- 7a. Actual vs Predicted Scatter ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(y_test, y_pred_best, alpha=0.2, s=10, color='steelblue', edgecolors='none')
lims = [min(y_test.min(), y_pred_best.min()), max(y_test.max(), y_pred_best.max())]
ax.plot(lims, lims, '--', color='red', linewidth=2, label='Perfect Prediction')
ax.set_xlabel('Actual Price (INR)', fontsize=13)
ax.set_ylabel('Predicted Price (INR)', fontsize=13)
ax.set_title(f'{best_model_name} — Actual vs Predicted', fontsize=16, fontweight='bold')
ax.legend(fontsize=12)
ax.set_aspect('equal')
plt.tight_layout()
save_plot(fig, '17_actual_vs_predicted.png')

# --- 7b. Residual Plot ---
residuals = y_test.values - y_pred_best
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(y_pred_best, residuals, alpha=0.2, s=10, color='darkorange', edgecolors='none')
ax.axhline(y=0, color='red', linewidth=2, linestyle='--')
ax.set_xlabel('Predicted Price (INR)', fontsize=13)
ax.set_ylabel('Residual (Actual − Predicted)', fontsize=13)
ax.set_title(f'{best_model_name} — Residual Plot', fontsize=16, fontweight='bold')
plt.tight_layout()
save_plot(fig, '18_residual_plot.png')

# --- 7c. Residual Distribution ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(residuals, bins=60, color='teal', edgecolor='white', alpha=0.85, density=True)
sns.kdeplot(residuals, ax=ax, color='crimson', linewidth=2.5)
ax.axvline(x=0, color='black', linewidth=1.5, linestyle='--')
ax.set_xlabel('Residual (INR)', fontsize=13)
ax.set_ylabel('Density', fontsize=13)
ax.set_title(f'{best_model_name} — Error Distribution', fontsize=16, fontweight='bold')
mean_res, std_res = np.mean(residuals), np.std(residuals)
ax.text(0.02, 0.95, f'Mean Error: ₹{mean_res:,.0f}\nStd Dev: ₹{std_res:,.0f}',
        transform=ax.transAxes, fontsize=12, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
save_plot(fig, '19_error_distribution.png')


# ════════════════════════════════════════════════════════════════════════════
# 8. BOOKING TIMING ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 8 — BOOKING TIMING ANALYSIS')
print('=' * 70)

# Analyse impact of booking timing on price
days_analysis = df.groupby('days_left')['price'].agg(['mean', 'median', 'std', 'count'])
early_booking = days_analysis.loc[days_analysis.index >= 40, 'mean'].mean()
mid_booking = days_analysis.loc[(days_analysis.index >= 15) & (days_analysis.index < 40), 'mean'].mean()
late_booking = days_analysis.loc[days_analysis.index <= 5, 'mean'].mean()
last_min = days_analysis.loc[days_analysis.index <= 2, 'mean'].mean()

print(f"\n   📊 Average Price by Booking Window:")
print(f"      Booked 40+ days early : ₹{early_booking:,.0f}")
print(f"      Booked 15-39 days     : ₹{mid_booking:,.0f}")
print(f"      Booked ≤5 days        : ₹{late_booking:,.0f}")
print(f"      Booked ≤2 days (last) : ₹{last_min:,.0f}")
print(f"\n   💡 Price difference (advance vs last-minute): ₹{last_min - early_booking:,.0f}")
print(f"   💡 Percentage increase: {((last_min - early_booking) / early_booking) * 100:.1f}%")

# --- Booking window visualization ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

booking_windows = pd.cut(df['days_left'],
                         bins=[0, 2, 7, 15, 30, 50],
                         labels=['1-2 days', '3-7 days', '8-15 days', '16-30 days', '31-49 days'])
window_prices = df.groupby(booking_windows, observed=True)['price'].mean()
colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#27ae60']
window_prices.plot(kind='bar', ax=axes[0], color=colors, edgecolor='white')
axes[0].set_title('Average Price by Booking Window', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Average Price (INR)')
axes[0].tick_params(axis='x', rotation=30)
for i, v in enumerate(window_prices.values):
    axes[0].text(i, v + 200, f'₹{v:,.0f}', ha='center', fontsize=10, fontweight='bold')

axes[1].bar(['Advance\n(40+ days)', 'Last-Minute\n(≤2 days)'],
            [early_booking, last_min],
            color=['#27ae60', '#e74c3c'], edgecolor='white', width=0.5)
axes[1].set_title('Advance vs Last-Minute Booking', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Average Price (INR)')
for i, v in enumerate([early_booking, last_min]):
    axes[1].text(i, v + 200, f'₹{v:,.0f}', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
save_plot(fig, '20_booking_timing_analysis.png')


# ════════════════════════════════════════════════════════════════════════════
# 9. PREDICTION ERROR ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 9 — PREDICTION ERROR ANALYSIS')
print('=' * 70)

overestimated = np.sum(residuals < -1000)
underestimated = np.sum(residuals > 1000)
accurate = np.sum(np.abs(residuals) <= 1000)

print(f"\n   📋 Prediction Accuracy (threshold: ±₹1,000):")
print(f"      ✅ Accurate (within ±₹1,000)   : {accurate:,} ({accurate/len(residuals)*100:.1f}%)")
print(f"      ⬆️  Overestimated (too high)    : {overestimated:,} ({overestimated/len(residuals)*100:.1f}%)")
print(f"      ⬇️  Underestimated (too low)    : {underestimated:,} ({underestimated/len(residuals)*100:.1f}%)")


# ════════════════════════════════════════════════════════════════════════════
# 10. K-MEANS CLUSTERING (Unsupervised Learning)
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 10 — K-MEANS CLUSTERING (Unsupervised Analysis)')
print('=' * 70)

cluster_features = ['duration', 'stops', 'days_left', 'class', 'price']
df_cluster = df[cluster_features].copy()

cluster_scaler = StandardScaler()
X_cluster = cluster_scaler.fit_transform(df_cluster)

# --- Elbow Method ---
print("\n🔧 Running Elbow Method (K = 2 to 10) — using a sample of 20,000 rows for speed...")
np.random.seed(42)
sample_indices = np.random.choice(len(X_cluster), size=min(20000, len(X_cluster)), replace=False)
X_cluster_sample = X_cluster[sample_indices]

inertias = []
K_range = range(2, 11)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    km.fit(X_cluster_sample)
    inertias.append(km.inertia_)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(K_range, inertias, 'bo-', linewidth=2.5, markersize=9)
ax.set_xlabel('Number of Clusters (K)', fontsize=13)
ax.set_ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=13)
ax.set_title('Elbow Method — Finding Optimal K', fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3)
plt.tight_layout()
save_plot(fig, '21_elbow_method.png')

# --- Final K-Means with K=4 ---
optimal_k = 4
print(f"\n🔧 Fitting K-Means with K = {optimal_k}...")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df_cluster['Cluster'] = kmeans.fit_predict(X_cluster)

# --- PCA 2D Visualization ---
print("🔧 Generating PCA 2D visualization of clusters...")
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_cluster)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
scatter = axes[0].scatter(X_pca[:5000, 0], X_pca[:5000, 1],
                          c=df_cluster['Cluster'].iloc[:5000], cmap='Set1',
                          alpha=0.5, s=10)
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)')
axes[0].set_title('K-Means Clusters (PCA 2D)', fontsize=14, fontweight='bold')
plt.colorbar(scatter, ax=axes[0], label='Cluster')

cluster_counts = df_cluster['Cluster'].value_counts().sort_index()
axes[1].bar(cluster_counts.index, cluster_counts.values,
            color=sns.color_palette('Set1', optimal_k), edgecolor='white')
axes[1].set_xlabel('Cluster', fontsize=12)
axes[1].set_ylabel('Number of Flights', fontsize=12)
axes[1].set_title('Flights per Cluster', fontsize=14, fontweight='bold')
for i, v in enumerate(cluster_counts.values):
    axes[1].text(i, v + 500, f'{v:,}', ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
save_plot(fig, '22_kmeans_clusters.png')

# Cluster summary
print("\n📊 Cluster Summary (average values):")
cluster_summary = df_cluster.groupby('Cluster')[cluster_features].mean().round(2)
print(cluster_summary.to_string())
print("\n   💡 Cluster Insights:")
for cluster_id in range(optimal_k):
    row = cluster_summary.loc[cluster_id]
    class_type = "Business" if row['class'] > 0.5 else "Economy"
    stop_type = "non-stop" if row['stops'] < 0.5 else f"{row['stops']:.0f}-stop"
    print(f"   Cluster {cluster_id}: Avg ₹{row['price']:,.0f} | {class_type} | "
          f"~{row['duration']:.1f}h | {stop_type} | booked {row['days_left']:.0f} days ahead")


# ════════════════════════════════════════════════════════════════════════════
# 11. SAVE BEST MODEL
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 11 — SAVE BEST MODEL')
print('=' * 70)

scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
joblib.dump(scaler, scaler_path)
print(f"\n   ✅ Scaler saved → {scaler_path}")

best_trained = best_result['Trained_Model']
model_path = os.path.join(MODEL_DIR, 'best_model.pkl')
joblib.dump(best_trained, model_path)
print(f"   ✅ Best model ({best_model_name}) saved → {model_path}")

feature_path = os.path.join(MODEL_DIR, 'feature_names.pkl')
joblib.dump(feature_names, feature_path)
print(f"   ✅ Feature names saved → {feature_path}")


# ════════════════════════════════════════════════════════════════════════════
# 12. SAMPLE PREDICTION
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '=' * 70)
print('   SECTION 12 — SAMPLE PREDICTION')
print('=' * 70)

print("""
   🎯 Predicting price for a sample flight:
      Airline     : Vistara
      Source      : Delhi → Mumbai
      Class       : Economy
      Stops       : Non-stop
      Duration    : 2.25 hours
      Departure   : Morning
      Days Left   : 15 days
""")

sample = pd.DataFrame(0, index=[0], columns=feature_names)
sample['stops'] = 0
sample['class'] = 0
sample['duration'] = 2.25
sample['days_left'] = 15
sample['departure_time'] = 1
sample['arrival_time'] = 2

for col in feature_names:
    if 'Vistara' in col:
        sample[col] = 1
    if 'source_city_Delhi' in col:
        sample[col] = 1
    if 'destination_city_Mumbai' in col:
        sample[col] = 1

sample_scaled = scaler.transform(sample)
if best_model_name in ['SVR (RBF)']:
    predicted_price = best_trained.predict(sample_scaled)[0]
else:
    predicted_price = best_trained.predict(sample)[0]

print(f"   💰 Predicted Price: ₹{predicted_price:,.2f}")
print(f"   🏷️  Model Used: {best_model_name}")

# Compare with last-minute booking
sample_late = sample.copy()
sample_late['days_left'] = 2
sample_late_scaled = scaler.transform(sample_late)
if best_model_name in ['SVR (RBF)']:
    late_price = best_trained.predict(sample_late_scaled)[0]
else:
    late_price = best_trained.predict(sample_late)[0]

print(f"\n   📊 Same flight booked 2 days before: ₹{late_price:,.2f}")
print(f"   📊 Difference (last-minute premium): ₹{late_price - predicted_price:,.2f}")


# ════════════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ════════════════════════════════════════════════════════════════════════════
print('\n' + '═' * 70)
print('   ✨ PROJECT COMPLETE — FLIGHT FARE PREDICTION ✨')
print('═' * 70)
print(f"""
   📁 Plots saved in         : {PLOT_DIR}
   📁 Models saved in        : {MODEL_DIR}
   🏆 Best model             : {best_model_name}
   📈 Best R² Score          : {comparison_df.loc[best_idx, 'R2_Score']:.4f}
   📉 Best MAE              : ₹{comparison_df.loc[best_idx, 'MAE']:,.0f}
   📉 Best RMSE             : ₹{comparison_df.loc[best_idx, 'RMSE']:,.0f}
   🔢 Features used          : {len(feature_names)}
   📊 Clusters identified    : {optimal_k}
   📊 Total visualizations   : 21 plots

   ── Algorithms Evaluated ──────────────────────────────────────
   1. Linear Regression       (baseline — simplest approach)
   2. Decision Tree Regressor (interpretable flowchart model)
   3. Random Forest Regressor (Bagging — ensemble of 200 trees)
   4. XGBoost Regressor       (Boosting — sequential error correction)
   5. SVR (RBF kernel)        (non-linear via kernel trick)
   6. K-Means Clustering      (unsupervised market segmentation)

   Author: Karthik KS
""")
print('═' * 70)