
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("TRACTOR PERFORMANCE ANALYSIS - NumPy & Matplotlib")
print("=" * 60)

# STEP 1: Load Cleaned Data
print("============================================")
print("\n[1] Loading cleaned data...")

df = pd.read_csv("cleaned_data.csv")
print(f"   Loaded: {len(df)} rows")

# STEP 2: to Identify the Key Columns
print("============================================")
print("\n[2] Identifying key columns...")

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
print(f"   Numeric columns: {numeric_cols[:5]}...")


# STEP 3: NumPy Vectorized Operations
print("============================================")
print("\n[3] NumPy vectorized operations...")

if numeric_cols:
    for col in numeric_cols[:3]:
        mean_val = np.mean(df[col].dropna())
        std_val = np.std(df[col].dropna())
        print(f" {col} - Mean: {mean_val:.2f}, Std: {std_val:.2f}")

# STEP 4: Correlation Analysis
print("============================================")
print("\n[4] Correlation analysis...")

if len(numeric_cols) >= 2:
    corr_matrix = df[numeric_cols[:5]].corr()
    print("   Correlation Matrix:")
    print(corr_matrix)


# STEP 5: Save Results (ALWAYS)
print("============================================")
print("\n[5] Saving results...")

with open("analysis_results.txt", "w") as f:
    f.write("TRACTOR PERFORMANCE ANALYSIS RESULTS\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Data shape: {df.shape}\n")
    f.write(f"Columns: {list(df.columns)}\n\n")
    
    if numeric_cols:
        f.write("Statistical Summary:\n")
        f.write(df[numeric_cols].describe().to_string())

print("Results saved to: analysis_results.txt")
print("Analysis is completed !")
