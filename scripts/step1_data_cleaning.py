# ============================================================================
# STEP 1: DATA CLEANING & PREPROCESSING
# ============================================================================
# Project : Uber Eats Bangalore Restaurant Intelligence & Decision Support
# Purpose : Load raw data (CSV + JSON), clean it, and prepare it for database
# Author  : [Your Name]
#
# HOW TO RUN THIS SCRIPT:
#   1. Open VS Code Terminal (Ctrl + `)
#   2. Make sure (venv) is active
#   3. Run: python scripts/step1_data_cleaning.py
# ============================================================================


# --------------------------------------------------------------------------
# SECTION 1: IMPORT LIBRARIES
# --------------------------------------------------------------------------
# pandas  → the main library for working with tabular data (like Excel in Python)
# numpy   → for numerical operations and handling missing values (NaN)
# json    → to read JSON files (JavaScript Object Notation)
# os      → to work with file paths on your computer
# --------------------------------------------------------------------------

import pandas as pd
import numpy as np
import json
import os


# --------------------------------------------------------------------------
# SECTION 2: SET UP FILE PATHS
# --------------------------------------------------------------------------
# os.path.dirname(__file__)  → gives the folder where THIS script is saved
# os.path.join()             → safely builds file paths (works on Windows & Mac)
#
# We go one folder UP from "scripts/" to reach the project root,
# then point to "data/raw/" for input and "data/cleaned/" for output.
# --------------------------------------------------------------------------

# Get the project root folder (one level up from scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Define input paths (raw data)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
CSV_PATH = os.path.join(RAW_DATA_DIR, "Uber_Eats_data.csv")
JSON_PATH = os.path.join(RAW_DATA_DIR, "orders.json")

# Define output paths (cleaned data)
CLEANED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")

# Create the cleaned data folder if it doesn't exist
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

print(f"📂 Project root:  {PROJECT_ROOT}")
print(f"📂 Raw data dir:  {RAW_DATA_DIR}")
print(f"📂 Clean data dir: {CLEANED_DATA_DIR}")


# --------------------------------------------------------------------------
# SECTION 3: LOAD THE RAW DATA
# --------------------------------------------------------------------------
# pd.read_csv()  reads a CSV file into a DataFrame (a table in pandas)
# json.load()    reads a JSON file into a Python list/dictionary
# pd.DataFrame() converts that list/dictionary into a pandas DataFrame
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 1: LOADING RAW DATA")
print("=" * 70)

# --- Load Restaurant CSV ---
df_restaurant = pd.read_csv(CSV_PATH)
print(f"\n✅ Restaurant data loaded: {df_restaurant.shape[0]} rows x {df_restaurant.shape[1]} columns")

# --- Load Order JSON ---
with open(JSON_PATH, "r") as f:
    orders_raw = json.load(f)          # This gives us a Python list of dictionaries

df_orders = pd.DataFrame(orders_raw)   # Convert list of dicts → DataFrame
print(f"✅ Order data loaded:      {df_orders.shape[0]} rows x {df_orders.shape[1]} columns")


# --------------------------------------------------------------------------
# SECTION 4: INITIAL DATA EXPLORATION
# --------------------------------------------------------------------------
# Before cleaning, we ALWAYS explore the data first to understand:
#   - What columns exist?
#   - What data types are they?
#   - Are there missing values, duplicates, or strange values?
#
# Key functions:
#   .info()       → shows column names, data types, and non-null counts
#   .head()       → shows the first 5 rows
#   .describe()   → shows statistics (count, mean, min, max, etc.)
#   .isnull()     → checks for missing values
#   .duplicated() → checks for duplicate rows
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 2: DATA EXPLORATION")
print("=" * 70)

print("\n--- Restaurant Data Info ---")
print(f"Columns: {list(df_restaurant.columns)}")
print(f"\nData types:")
for col in df_restaurant.columns:
    print(f"   {col:40s} → {df_restaurant[col].dtype}")

print(f"\nMissing values per column:")
for col in df_restaurant.columns:
    nulls = df_restaurant[col].isnull().sum()
    print(f"   {col:40s} → {nulls} missing")

print(f"\nDuplicate rows: {df_restaurant.duplicated().sum()}")

print(f"\n--- Sample rows (first 3) ---")
print(df_restaurant.head(3).to_string())


# --------------------------------------------------------------------------
# SECTION 5: CLEAN RESTAURANT DATA
# --------------------------------------------------------------------------
# We will perform the following cleaning steps:
#   5a. Remove duplicate rows
#   5b. Clean the 'rate' column (e.g., "4.1/5" → 4.1, "NEW" → NaN)
#   5c. Clean the 'approx_cost(for two people)' column (remove commas → number)
#   5d. Rename columns to be database-friendly (no spaces, no brackets)
#   5e. Handle missing values
#   5f. Feature Engineering: Add pricing_segment and rating_category columns
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 3: CLEANING RESTAURANT DATA")
print("=" * 70)


# ---- 5a. Remove Duplicates ----
# Why? Duplicate rows can skew our analysis (e.g., a restaurant counted twice
# would inflate averages). We use drop_duplicates() to remove exact copies.

before = len(df_restaurant)
df_restaurant = df_restaurant.drop_duplicates()
after = len(df_restaurant)
print(f"\n5a. Removed {before - after} duplicate rows → {after} rows remaining")


# ---- 5b. Clean the 'rate' column ----
# Problem: The rate column has values like "4.1/5", "3.8 /5", and "NEW"
#   - We need to extract just the number (4.1, 3.8)
#   - "NEW" means the restaurant hasn't been rated yet → we'll set it to NaN
#
# How it works step by step:
#   1. Replace "NEW" with NaN (Not a Number - pandas' way of saying "missing")
#   2. Remove the "/5" part using .str.replace()
#   3. Strip whitespace using .str.strip()
#   4. Convert from string to float (decimal number)

print("\n5b. Cleaning 'rate' column...")
print(f"    Before: Sample values = {list(df_restaurant['rate'].unique()[:5])}")

df_restaurant['rate'] = df_restaurant['rate'].replace('NEW', np.nan)   # NEW → NaN
df_restaurant['rate'] = df_restaurant['rate'].str.replace('/5', '')     # Remove /5
df_restaurant['rate'] = df_restaurant['rate'].str.strip()               # Remove spaces
df_restaurant['rate'] = pd.to_numeric(df_restaurant['rate'], errors='coerce')  # → Float

print(f"    After:  Sample values = {list(df_restaurant['rate'].dropna().unique()[:5])}")
print(f"    Restaurants with no rating (NEW): {df_restaurant['rate'].isnull().sum()}")


# ---- 5c. Clean the 'approx_cost(for two people)' column ----
# Problem: Values like "800", "1,000", "1,500" are strings with commas
# Solution: Remove commas, then convert to integer
#
# .str.replace(',', '') → removes all commas from the string
# pd.to_numeric()       → converts string to number

print("\n5c. Cleaning 'approx_cost(for two people)' column...")
print(f"    Before: Sample values = {list(df_restaurant['approx_cost(for two people)'].unique()[:5])}")

df_restaurant['approx_cost(for two people)'] = (
    df_restaurant['approx_cost(for two people)']
    .str.replace(',', '')                           # Remove commas: "1,000" → "1000"
    .pipe(pd.to_numeric, errors='coerce')           # Convert to number
)

print(f"    After:  Sample values = {list(df_restaurant['approx_cost(for two people)'].dropna().unique()[:5])}")


# ---- 5d. Rename Columns ----
# Why? Column names like "approx_cost(for two people)" and "listed_in(type)"
# have spaces and brackets, which cause problems in SQL databases.
# We rename them to clean, database-friendly names using snake_case.

print("\n5d. Renaming columns to database-friendly names...")

df_restaurant = df_restaurant.rename(columns={
    'name':                        'restaurant_name',
    'online_order':                'online_order',
    'book_table':                  'book_table',
    'rate':                        'rating',
    'votes':                       'votes',
    'phone':                       'phone',
    'location':                    'location',
    'rest_type':                   'restaurant_type',
    'dish_liked':                  'dish_liked',
    'cuisines':                    'cuisines',
    'approx_cost(for two people)': 'approx_cost_for_two',
    'listed_in(type)':             'listed_in_type',
    'listed_in(city)':             'listed_in_city'
})

print(f"    New column names: {list(df_restaurant.columns)}")


# ---- 5e. Handle Missing Values ----
# Strategy:
#   - 'rating': Keep NaN (these are NEW restaurants, we'll filter as needed)
#   - 'approx_cost_for_two': Fill with median (middle value) - better than mean
#     because it's not affected by extreme values
#   - Text columns: Replace NaN with "Unknown"
#
# Why median over mean?
#   If costs are [200, 300, 300, 400, 5000], mean = 1240 (skewed by 5000)
#   but median = 300 (the actual middle value - more representative)

print("\n5e. Handling missing values...")

# Fill cost with median
cost_median = df_restaurant['approx_cost_for_two'].median()
cost_missing = df_restaurant['approx_cost_for_two'].isnull().sum()
df_restaurant['approx_cost_for_two'] = df_restaurant['approx_cost_for_two'].fillna(cost_median)
print(f"    approx_cost_for_two: {cost_missing} missing → filled with median ({cost_median})")

# Fill text columns with "Unknown"
text_columns = ['restaurant_name', 'phone', 'restaurant_type', 'dish_liked', 'cuisines']
for col in text_columns:
    missing = df_restaurant[col].isnull().sum()
    if missing > 0:
        df_restaurant[col] = df_restaurant[col].fillna('Unknown')
        print(f"    {col}: {missing} missing → filled with 'Unknown'")

# Rating: we keep NaN intentionally
rating_missing = df_restaurant['rating'].isnull().sum()
print(f"    rating: {rating_missing} missing → kept as NaN (these are 'NEW' restaurants)")


# ---- 5f. Feature Engineering ----
# This is where we CREATE NEW COLUMNS from existing data to add more value.
#
# 1. pricing_segment: Categorize restaurants by cost
#    - Budget:  ₹0 - ₹300
#    - Mid:     ₹301 - ₹700
#    - Premium: ₹701+
#
# 2. rating_category: Categorize restaurants by rating
#    - Poor:      0 - 2.5
#    - Average:   2.6 - 3.5
#    - Good:      3.6 - 4.0
#    - Excellent:  4.1 - 5.0
#
# pd.cut() splits continuous numbers into categories (like bins/buckets)
# We provide the bin edges and the labels for each bin.

print("\n5f. Feature Engineering - Creating new columns...")

# Pricing Segment
df_restaurant['pricing_segment'] = pd.cut(
    df_restaurant['approx_cost_for_two'],
    bins=[0, 300, 700, float('inf')],        # Bin edges: 0-300, 301-700, 701+
    labels=['Budget', 'Mid', 'Premium'],      # Labels for each bin
    include_lowest=True                        # Include the lowest edge (0)
)
print(f"    pricing_segment distribution:")
for segment, count in df_restaurant['pricing_segment'].value_counts().items():
    print(f"      {segment:10s} → {count} restaurants")

# Rating Category
df_restaurant['rating_category'] = pd.cut(
    df_restaurant['rating'],
    bins=[0, 2.5, 3.5, 4.0, 5.0],
    labels=['Poor', 'Average', 'Good', 'Excellent'],
    include_lowest=True
)
print(f"\n    rating_category distribution:")
for category, count in df_restaurant['rating_category'].value_counts().items():
    print(f"      {category:10s} → {count} restaurants")

# Convert category columns to string for SQLite compatibility
df_restaurant['pricing_segment'] = df_restaurant['pricing_segment'].astype(str)
df_restaurant['rating_category'] = df_restaurant['rating_category'].astype(str)

# Replace 'nan' strings with meaningful labels
df_restaurant['pricing_segment'] = df_restaurant['pricing_segment'].replace('nan', 'Unknown')
df_restaurant['rating_category'] = df_restaurant['rating_category'].replace('nan', 'Unrated')


# ---- 5g. Remove Logical Duplicates ----
# Problem: The same restaurant appears MULTIPLE times because of two columns:
#   - listed_in_type: A restaurant is listed under Delivery, Dine-out, Cafes, etc.
#   - listed_in_city: A restaurant near area borders is listed in multiple areas
#
# Example: 'Hammered' in Cunningham Road appeared 34 times because
#          6 listing types × multiple nearby cities = 34 entries
#
# These are NOT data errors — they're how the platform categorizes restaurants.
# But for ANALYSIS, we must count each restaurant ONCE to avoid inflating averages.
#
# Solution: Group by restaurant_name + location, keep the best values:
#   - rating: keep MAX (highest/latest rating)
#   - votes: keep MAX (most recent vote count)
#   - listed_in_type: combine all types into one comma-separated string
#   - listed_in_city: combine all cities into one comma-separated string
#   - other columns: keep FIRST value (they're the same across duplicates)

print("\n5g. Removing logical duplicates...")
before_logical = len(df_restaurant)

df_restaurant = df_restaurant.groupby(['restaurant_name', 'location']).agg({
    'online_order': 'first',
    'book_table': 'first',
    'rating': 'max',                                                # Keep highest rating
    'votes': 'max',                                                 # Keep highest votes
    'phone': 'first',
    'restaurant_type': 'first',
    'dish_liked': 'first',
    'cuisines': 'first',
    'approx_cost_for_two': 'first',
    'listed_in_type': lambda x: ', '.join(sorted(x.unique())),      # Combine all listing types
    'listed_in_city': lambda x: ', '.join(sorted(x.unique())),      # Combine all listed cities
    'pricing_segment': 'first',
    'rating_category': 'first',
}).reset_index()

# Recalculate rating_category based on the max rating we kept
df_restaurant['rating_category'] = pd.cut(
    df_restaurant['rating'],
    bins=[0, 2.5, 3.5, 4.0, 5.0],
    labels=['Poor', 'Average', 'Good', 'Excellent'],
    include_lowest=True
).astype(str).replace('nan', 'Unrated')

after_logical = len(df_restaurant)
print(f"    Before: {before_logical} rows")
print(f"    After:  {after_logical} rows")
print(f"    Removed {before_logical - after_logical} logical duplicates ({((before_logical - after_logical) / before_logical * 100):.1f}%)")
print(f"    Each restaurant now appears exactly ONCE per location")


# --------------------------------------------------------------------------
# SECTION 6: CLEAN ORDER DATA
# --------------------------------------------------------------------------
# The order data (from JSON) is already quite clean, but we'll:
#   6a. Convert order_date from string to proper date format
#   6b. Round order_value to 2 decimal places
#   6c. Verify everything looks good
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 4: CLEANING ORDER DATA")
print("=" * 70)

# 6a. Convert date column
print("\n6a. Converting order_date to datetime...")
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
print(f"    Date range: {df_orders['order_date'].min().date()} to {df_orders['order_date'].max().date()}")

# 6b. Round order_value to 2 decimal places
df_orders['order_value'] = df_orders['order_value'].round(2)

# 6c. Quick summary
print(f"\n6b. Order data summary:")
print(f"    Total orders:         {len(df_orders)}")
print(f"    Unique restaurants:   {df_orders['restaurant_name'].nunique()}")
print(f"    Payment methods:      {list(df_orders['payment_method'].unique())}")
print(f"    Discount usage:       Yes={len(df_orders[df_orders['discount_used']=='Yes'])}, No={len(df_orders[df_orders['discount_used']=='No'])}")
print(f"    Avg order value:      ₹{df_orders['order_value'].mean():.2f}")


# --------------------------------------------------------------------------
# SECTION 7: SAVE CLEANED DATA
# --------------------------------------------------------------------------
# We save the cleaned DataFrames as new CSV files in data/cleaned/.
# These files will be used in Step 2 to load into the SQLite database.
#
# index=False → don't save the row numbers as a column
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 5: SAVING CLEANED DATA")
print("=" * 70)

# Save cleaned restaurant data
restaurant_output = os.path.join(CLEANED_DATA_DIR, "cleaned_restaurant_data.csv")
df_restaurant.to_csv(restaurant_output, index=False)
print(f"\n✅ Saved: {restaurant_output}")
print(f"   ({len(df_restaurant)} rows x {len(df_restaurant.columns)} columns)")

# Save cleaned order data
orders_output = os.path.join(CLEANED_DATA_DIR, "cleaned_orders_data.csv")
df_orders.to_csv(orders_output, index=False)
print(f"\n✅ Saved: {orders_output}")
print(f"   ({len(df_orders)} rows x {len(df_orders.columns)} columns)")


# --------------------------------------------------------------------------
# SECTION 8: FINAL SUMMARY
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("✅ STEP 1 COMPLETE: DATA CLEANING SUMMARY")
print("=" * 70)

print(f"""
📊 RESTAURANT DATA:
   Rows:               {len(df_restaurant)}
   Columns:            {len(df_restaurant.columns)}
   Duplicates removed: {before - after}
   Rate cleaned:       "4.1/5" → 4.1  ({rating_missing} 'NEW' entries → NaN)
   Cost cleaned:       "1,000" → 1000
   New columns added:  pricing_segment, rating_category

📦 ORDER DATA:
   Rows:               {len(df_orders)}
   Columns:            {len(df_orders.columns)}
   Dates converted:    String → DateTime
   Values rounded:     To 2 decimal places

📁 OUTPUT FILES:
   1. {restaurant_output}
   2. {orders_output}

👉 NEXT: Run Step 2 → python scripts/step2_database_setup.py
""")
