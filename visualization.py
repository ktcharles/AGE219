# visualization.py
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# PROFESSIONAL PLOT SETTINGS 
print("======================================") 
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.figsize'] = (12, 8)


print(" CREATING 3 VISUALIZATIONS GRAPH")
print("====================================")
 
# case 1: by loading the cleaned data 
print("\n[1] loading data")
df = pd.read_csv("cleaned_data.csv")
print(f" loaded: {len(df)} row")

#case 2:  by using the correct column names
fuel_col = 'EngFuelRate_(L/h)'
load_col = 'ActualEngPercentTorque_(%)'
op_col = 'operation'

print(f"fuel: {fuel_col}")
print(f"Load: {load_col}")
print(f"operation: {op_col}")

# to check if the column is exist 
if fuel_col not in df.columns:
    print(f"column '{fuel_col}' not found ")
    print(f"available columns: {df.columns.tolist()[:10]}")
    exit()

   
if op_col not in df.columns:
    print(f"column '{op_col}' not found ")
    print(f" available columns: {df.columns.tolist()[:10]}") 
    exit()


# PLOT 1: Trend Analysis
print("================================================")
print("\n[2] Creating Plot 1: Trend Analysis.")
plt.figure(figsize=(12, 6))

# by Taking a sample of the data for performance
sample_df = df[[fuel_col]].dropna().iloc[::100, :]
x = np.arange(len(sample_df))
y = sample_df[fuel_col].values

# To Calculate trend line
slope, intercept, r, p, _ = stats.linregress(x, y)
trend_line = slope * x + intercept
plt.plot(x, y, 'b-', linewidth=1.5, alpha=0.7, label='Fuel Consumption')
plt.plot(x, trend_line, 'r--', linewidth=2, label=f'Trend (r={r:.3f})')

plt.title('TRACTOR FUEL CONSUMPTION TREND', fontsize=14, fontweight='bold')
plt.xlabel('Data Point Index')
plt.ylabel('Fuel Consumption (L/h)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('1. trend_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 1. trend_analysis.png")


# PLOT 2: Categorical Comparison
print("=========================================================")
print("\n[3] Creating Plot 2: Categorical Comparison...")
# Group by operation and calculate mean fuel consumption
grouped = df.groupby(op_col)[fuel_col].mean().sort_values(ascending=False)
print(f"  Operations found: {len(grouped)}")
print(f"  First 5: {list(grouped.index[:5])}")

plt.figure(figsize=(12, 7))
bars = plt.bar(grouped.index.astype(str), grouped.values, color='steelblue')
plt.xticks(rotation=45, ha='right', fontsize=13)

# Add value labels on bars
for bar, value in zip(bars, grouped.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{value:.2f}', ha='center', va='bottom', fontsize=9)

plt.title('AVERAGE FUEL CONSUMPTION BY OPERATION TYPE', fontsize=13, fontweight='bold')
plt.xlabel('Operation Type')
plt.ylabel('Average Fuel Consumption (L/h)')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('2. categorical_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved: 2. categorical_comparison.png")

# PLOT 3: Correlation Plot (Scatter with Trend)
print("================================================")
print("\n[4] Creating Plot 3: Correlation Plot.")

valid_data = df[[load_col, fuel_col]].dropna()
x = valid_data[load_col].values
y = valid_data[fuel_col].values
slope, intercept, r, p, _ = stats.linregress(x, y)
plt.figure(figsize=(13, 7))

# Sample every 100 point for performance
sample_idx = np.arange(0, len(x), 100)
plt.scatter(x[sample_idx], y[sample_idx], alpha=0.3, s=10, color='green', label='Data points')

# Trend line
x_line = np.linspace(x.min(), x.max(), 100)
y_line = slope * x_line + intercept
plt.plot(x_line, y_line, 'r-', linewidth=2, 
         label=f'Trend: r={r:.3f}, p={p:.3f}')

plt.title(f'ENGINE LOAD Vs FUEL CONSUMPTION (r={r:.3f})', fontsize=14, fontweight='bold')
plt.xlabel('Engine Load (%)')
plt.ylabel('Fuel Consumption (L/h)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.savefig('3.correlation_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print(" Saved: 3.correlation_plot.png")

print(" ALL 3 VISUALIZATIONS COMPLETE SO THat MISSION IS ACCOMPLISHED ")
print("=========================================")
print("\nFiles created:")
print(" 1. trend_analysis.png")
print(" 2. categorical_comparison.png")
print(" 3. correlation_plot.png")