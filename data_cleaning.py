# data_cleaning.py
# starting by import all necessary requirements
import pandas as pd
import glob
import os

print("DATA CLEANING AND MERGING SCRIPT")
print("This script will clean and merge all CSV files in the specified directory.")

# CASE 1: To read all CSV files in a directory and merge them into a single DataFrame, you can use the following code:
print("===================================")
print("\n[1] Reading CSV files...")

# by using glob to find all CSV files in the specified directory
csv_files = glob.glob("data/selected/*.csv")  # Adjust the path as needed
print(f"Found {len(csv_files)} CSV files.")
if len(csv_files) >= 10:
   print("it meet the requirement of having at least 10 CSV files.")
else:
   print("it does not meet the requirement of having at least 10 CSV files.")


# CASE 2: To combine and merge all CSV files into a single DataFrame
print("===================================")
print("\n[2] Merging files (Concatenating DataFrames).")

all_data = []
total_rows = 0
for file in csv_files:
    df = pd.read_csv(file)
    
    # Get the operation name from the file name
    name = os.path.basename(file).replace(".csv", "")
    name = name.replace("_Field_1", "").replace("_Field_2", "")
    
    # Add the operation column
    df["operation"] = name
    
    all_data.append(df)
    total_rows += len(df)
    print(f"   Read: {os.path.basename(file)} ({len(df)} rows) -> {name}")

# to concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(all_data, ignore_index=True)
print("All CSV files have been merged into a single DataFrame.")


# CASE 3: To make all date is cleaned and formatted in a consistent way, you can use the following code:
print("===================================")
print("\n[3] Cleaning data...")
# to find for missing values
misssing = merged_df.isnull().sum()
missing_count = misssing.sum()
print(f" missing values before cleaning: {missing_count}")

# Removing rows with missing data 
if missing_count > 0:
   merged_df = merged_df.dropna(thresh=2)
print(f" After cleaning: {len(merged_df)} rows")

# To remove duplication 
duplicates = merged_df.duplicated().sum()
if duplicates > 0:
    merged_df = merged_df.drop_duplicates()
    print(f" Removed {duplicates} duplicate rows")


# CASE 4: The use of groupby() Aggregation for the operation in group
print("============================================")
print("\n[4] Aggregation with groupby()...")
numeric_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if numeric_cols:
    print(f" Numeric columns found: {numeric_cols[:5]}...")
# Finding a categorical column for grouping
    for col in merged_df.columns:
        if col not in numeric_cols and col != 'Timestamp':

# by using groupby() to aggregate the data based on a categorical column
            grouped_df = merged = merged_df.groupby(col)[numeric_cols[0]].mean()
            print(f" grouped by '{col}' and calculated mean of '{numeric_cols[0]}': ")
            break



#CASE 5: To Save the Cleaned Data
print("============================================")
print("\n[5] Saving cleaned data...")

output_file = "cleaned_data.csv"
merged_df.to_csv(output_file, index=False)
print(f" Saved: {output_file}")
print(f" Final shape: {merged_df.shape}")
print("DATA CLEANING COMPLETED BY FULL OF DETAILS THAT IS REQUIRED")
