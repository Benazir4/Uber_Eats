# ============================================================================
# STEP 2: SQLite DATABASE SETUP & SQL QUERIES
# ============================================================================
# Project : Uber Eats Bangalore Restaurant Intelligence & Decision Support
# Purpose : Create SQLite database, load cleaned data, and test SQL queries
# Author  : [Your Name]
#
# HOW TO RUN:
#   1. Make sure Step 1 has been run (cleaned CSVs exist in data/cleaned/)
#   2. Open VS Code Terminal (Ctrl + `)
#   3. Run: python scripts/step2_database_setup.py
#
# WHAT IS SQLite?
#   SQLite is a lightweight database that stores everything in a SINGLE FILE
#   (no server needed!). Perfect for learning SQL and small-to-medium projects.
#   The file will be saved as: database/uber_eats.db
# ============================================================================


# --------------------------------------------------------------------------
# SECTION 1: IMPORT LIBRARIES
# --------------------------------------------------------------------------
# sqlite3 → Python's built-in library to work with SQLite databases
#            (no installation needed - it comes with Python!)
# pandas   → to read our cleaned CSV files
# os       → to work with file paths
# --------------------------------------------------------------------------

import sqlite3
import pandas as pd
import os


# --------------------------------------------------------------------------
# SECTION 2: SET UP FILE PATHS
# --------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Input: cleaned data from Step 1
CLEANED_DIR = os.path.join(PROJECT_ROOT, "data", "cleaned")
RESTAURANT_CSV = os.path.join(CLEANED_DIR, "cleaned_restaurant_data.csv")
ORDERS_CSV = os.path.join(CLEANED_DIR, "cleaned_orders_data.csv")

# Output: SQLite database file
DB_DIR = os.path.join(PROJECT_ROOT, "database")
DB_PATH = os.path.join(DB_DIR, "uber_eats.db")

# Create database folder if it doesn't exist
os.makedirs(DB_DIR, exist_ok=True)

print(f"📂 Project root:    {PROJECT_ROOT}")
print(f"📂 Cleaned data:    {CLEANED_DIR}")
print(f"📂 Database output: {DB_PATH}")


# --------------------------------------------------------------------------
# SECTION 3: CREATE THE DATABASE & LOAD DATA
# --------------------------------------------------------------------------
# How SQLite works in Python:
#
#   1. sqlite3.connect("file.db")  → Opens (or creates) a database file
#      This gives us a "connection" object - like opening a door to the database
#
#   2. connection.cursor()  → Creates a "cursor" object
#      A cursor is like a pointer that executes SQL commands and fetches results
#
#   3. cursor.execute("SQL query here")  → Runs a SQL command
#
#   4. connection.commit()  → Saves changes to the database file
#
#   5. connection.close()  → Closes the connection (always do this when done!)
#
# We also use pandas' to_sql() method to load entire DataFrames into tables
# in one line - much easier than inserting row by row!
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 1: CREATING DATABASE & LOADING DATA")
print("=" * 70)

# --- Load cleaned CSVs ---
print("\n📥 Loading cleaned CSV files...")
df_restaurant = pd.read_csv(RESTAURANT_CSV)
df_orders = pd.read_csv(ORDERS_CSV)
print(f"   Restaurant data: {len(df_restaurant)} rows")
print(f"   Order data:      {len(df_orders)} rows")

# --- Connect to SQLite database ---
# If the file doesn't exist, sqlite3 will CREATE it automatically
# If it already exists, it will OVERWRITE the tables (if_exists='replace')
print(f"\n🔌 Connecting to database: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Load Restaurant data into a table called 'restaurants' ---
# to_sql() does all the heavy lifting:
#   - Creates the table with correct column names and data types
#   - Inserts all rows from the DataFrame
#   - if_exists='replace' means: if the table already exists, drop it and recreate
#   - index=False means: don't add pandas row numbers as a column

print("\n📤 Loading restaurant data into 'restaurants' table...")
df_restaurant.to_sql('restaurants', conn, if_exists='replace', index=False)
print(f"   ✅ 'restaurants' table created with {len(df_restaurant)} rows")

# --- Load Order data into a table called 'orders' ---
print("\n📤 Loading order data into 'orders' table...")
df_orders.to_sql('orders', conn, if_exists='replace', index=False)
print(f"   ✅ 'orders' table created with {len(df_orders)} rows")

# --- Save (commit) the changes ---
conn.commit()
print("\n💾 Database saved successfully!")


# --------------------------------------------------------------------------
# SECTION 4: VERIFY THE DATABASE
# --------------------------------------------------------------------------
# Let's run some basic SQL queries to make sure everything loaded correctly.
#
# SQL BASICS:
#   SELECT   → which columns to show
#   FROM     → which table to read from
#   WHERE    → filter rows (like an "if" condition)
#   LIMIT    → show only first N rows
#   COUNT(*) → count the number of rows
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 2: VERIFYING DATABASE")
print("=" * 70)

# --- Check what tables exist in the database ---
# sqlite_master is a special system table that lists all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"\n📋 Tables in database: {[t[0] for t in tables]}")

# --- Check restaurant table structure ---
# PRAGMA table_info gives us column names and data types
cursor.execute("PRAGMA table_info(restaurants);")
columns = cursor.fetchall()
print(f"\n📊 'restaurants' table columns:")
for col in columns:
    # col format: (index, name, type, notnull, default, primary_key)
    print(f"   {col[1]:25s} → {col[2]}")

# --- Check order table structure ---
cursor.execute("PRAGMA table_info(orders);")
columns = cursor.fetchall()
print(f"\n📦 'orders' table columns:")
for col in columns:
    print(f"   {col[1]:25s} → {col[2]}")

# --- Row counts ---
cursor.execute("SELECT COUNT(*) FROM restaurants;")
rest_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM orders;")
order_count = cursor.fetchone()[0]
print(f"\n📈 Row counts:")
print(f"   restaurants: {rest_count} rows")
print(f"   orders:      {order_count} rows")

# --- Sample data ---
print(f"\n🔍 Sample restaurant data (first 3 rows):")
sample = pd.read_sql_query("SELECT restaurant_name, location, rating, approx_cost_for_two, pricing_segment FROM restaurants LIMIT 3", conn)
print(sample.to_string(index=False))

print(f"\n🔍 Sample order data (first 3 rows):")
sample = pd.read_sql_query("SELECT order_id, restaurant_name, order_date, order_value, payment_method FROM orders LIMIT 3", conn)
print(sample.to_string(index=False))


# --------------------------------------------------------------------------
# SECTION 5: TEST ALL 15 BUSINESS QUESTIONS WITH SQL
# --------------------------------------------------------------------------
# Now we'll write and test each SQL query that will power the Streamlit app.
#
# SQL CONCEPTS WE'LL USE:
#
#   GROUP BY  → Groups rows that have the same value in a column
#              Example: GROUP BY location → groups all restaurants by location
#
#   HAVING    → Like WHERE, but for groups (filters AFTER grouping)
#              Example: HAVING COUNT(*) > 10 → only groups with more than 10
#
#   ORDER BY  → Sorts the results (ASC = ascending, DESC = descending)
#
#   AVG()     → Calculates the average of a column
#   COUNT()   → Counts the number of rows
#   ROUND()   → Rounds a number to N decimal places
#
#   CASE WHEN → Like an if-else statement inside SQL
#              Example: CASE WHEN rating > 4 THEN 'Good' ELSE 'Bad' END
#
#   JOIN      → Combines two tables based on a common column
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 3: TESTING ALL 15 BUSINESS QUESTIONS")
print("=" * 70)


# ========================
# Helper function to run a query and display results
# ========================
def run_query(question_num, title, query):
    """
    Runs a SQL query and prints the result as a formatted table.
    
    Parameters:
        question_num (int)  : Question number (1-15)
        title (str)         : The business question
        query (str)         : The SQL query to execute
    """
    print(f"\n{'─' * 70}")
    print(f"Q{question_num}: {title}")
    print(f"{'─' * 70}")
    print(f"SQL:\n{query.strip()}\n")
    
    result = pd.read_sql_query(query, conn)
    print(f"Result ({len(result)} rows):")
    print(result.to_string(index=False))
    return result


# ========================
# Q1: Which Bangalore locations have the highest average restaurant ratings?
# ========================
# SQL: GROUP BY location → calculate AVG rating → sort by highest rating
# HAVING COUNT(*) >= 10 → only locations with at least 10 restaurants
#                         (so small samples don't skew results)
# ========================

run_query(1,
    "Which locations have the highest average restaurant ratings?",
    """
    SELECT 
        location,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY location
    HAVING COUNT(*) >= 10
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
)


# ========================
# Q2: Which locations are over-saturated with restaurants?
# ========================
# SQL: COUNT restaurants per location → sort by most restaurants
# ========================

run_query(2,
    "Which locations are over-saturated with restaurants?",
    """
    SELECT 
        location,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY location
    ORDER BY restaurant_count DESC
    LIMIT 10;
    """
)


# ========================
# Q3: Does online ordering improve restaurant ratings?
# ========================
# SQL: GROUP BY online_order (Yes/No) → compare average ratings
# This tells us if restaurants with online ordering have better ratings
# ========================

run_query(3,
    "Does online ordering improve restaurant ratings?",
    """
    SELECT 
        online_order,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(votes), 0) AS avg_votes
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY online_order;
    """
)


# ========================
# Q4: Does table booking correlate with higher customer ratings?
# ========================
# SQL: GROUP BY book_table (Yes/No) → compare average ratings
# ========================

run_query(4,
    "Does table booking correlate with higher customer ratings?",
    """
    SELECT 
        book_table,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY book_table;
    """
)


# ========================
# Q5: What price range delivers the best customer satisfaction?
# ========================
# SQL: GROUP BY pricing_segment → compare ratings across Budget/Mid/Premium
# ========================

run_query(5,
    "What price range delivers the best customer satisfaction?",
    """
    SELECT 
        pricing_segment,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
        AND pricing_segment != 'Unknown'
    GROUP BY pricing_segment
    ORDER BY avg_rating DESC;
    """
)


# ========================
# Q6: How do low, mid, and premium-priced restaurants perform?
# ========================
# SQL: Detailed breakdown using CASE WHEN for finer price ranges
# CASE WHEN creates custom categories on-the-fly inside the query
# ========================

run_query(6,
    "How do low, mid, and premium-priced restaurants perform in terms of ratings?",
    """
    SELECT 
        CASE 
            WHEN approx_cost_for_two <= 200 THEN '1. ₹0-200 (Low)'
            WHEN approx_cost_for_two <= 500 THEN '2. ₹201-500 (Budget)'
            WHEN approx_cost_for_two <= 1000 THEN '3. ₹501-1000 (Mid)'
            WHEN approx_cost_for_two <= 1500 THEN '4. ₹1001-1500 (High)'
            ELSE '5. ₹1500+ (Premium)'
        END AS price_range,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(votes), 0) AS avg_votes
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY price_range
    ORDER BY price_range;
    """
)


# ========================
# Q7: Which cuisines are most common in Bangalore?
# ========================
# NOTE: The 'cuisines' column has multiple cuisines separated by commas
#       (e.g., "North Indian, Chinese, Thai")
#       For simplicity, we count the primary cuisine (the full string).
#       A more advanced approach would split and count each cuisine separately.
# ========================

run_query(7,
    "Which cuisines are most common in Bangalore?",
    """
    SELECT 
        cuisines,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY cuisines
    ORDER BY restaurant_count DESC
    LIMIT 15;
    """
)


# ========================
# Q8: Which cuisines receive the highest average ratings?
# ========================
# HAVING COUNT(*) >= 10 → only cuisines with enough restaurants
#                         to make the average meaningful
# ========================

run_query(8,
    "Which cuisines receive the highest average ratings?",
    """
    SELECT 
        cuisines,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY cuisines
    HAVING COUNT(*) >= 10
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
)


# ========================
# Q9: Which cuisines perform well despite having fewer restaurants?
# ========================
# These are "hidden gems" - high rating but not many restaurants
# HAVING COUNT(*) BETWEEN 3 AND 15 → niche cuisines only
# ========================

run_query(9,
    "Which cuisines perform well despite having fewer restaurants?",
    """
    SELECT 
        cuisines,
        ROUND(AVG(rating), 2) AS avg_rating,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY cuisines
    HAVING COUNT(*) BETWEEN 3 AND 15
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
)


# ========================
# Q10: What is the relationship between restaurant cost and rating?
# ========================
# SQL: Group by cost brackets using CASE WHEN → compare ratings
# ========================

run_query(10,
    "What is the relationship between restaurant cost and rating?",
    """
    SELECT 
        CASE 
            WHEN approx_cost_for_two <= 300 THEN 'Budget (≤₹300)'
            WHEN approx_cost_for_two <= 700 THEN 'Mid (₹301-700)'
            ELSE 'Premium (₹700+)'
        END AS cost_category,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(MIN(rating), 1) AS min_rating,
        ROUND(MAX(rating), 1) AS max_rating
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY cost_category
    ORDER BY avg_rating DESC;
    """
)


# ========================
# Q11: Which locations are ideal for premium restaurant onboarding?
# ========================
# SQL: Filter for Premium segment → find locations with high ratings
# These are areas where expensive restaurants do well
# ========================

run_query(11,
    "Which locations are ideal for premium restaurant onboarding?",
    """
    SELECT 
        location,
        COUNT(*) AS premium_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost,
        ROUND(AVG(votes), 0) AS avg_votes
    FROM restaurants
    WHERE rating IS NOT NULL
        AND pricing_segment = 'Premium'
    GROUP BY location
    HAVING COUNT(*) >= 5
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
)


# ========================
# Q12: Which locations show high demand but lower average ratings?
# ========================
# SQL: Find locations with many restaurants (high demand) but low ratings
# These areas NEED quality improvement
# ========================

run_query(12,
    "Which locations show high demand but lower average ratings?",
    """
    SELECT 
        location,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(votes), 0) AS avg_votes,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY location
    HAVING COUNT(*) >= 50 AND AVG(rating) < 3.8
    ORDER BY avg_rating ASC;
    """
)


# ========================
# Q13: Do restaurants offering BOTH online ordering AND table booking perform better?
# ========================
# SQL: Create 4 groups based on combinations of features
# CASE WHEN with AND conditions to create feature combinations
# ========================

run_query(13,
    "Do restaurants offering both online ordering and table booking perform better?",
    """
    SELECT 
        CASE 
            WHEN online_order = 'Yes' AND book_table = 'Yes' THEN 'Both Features'
            WHEN online_order = 'Yes' AND book_table = 'No'  THEN 'Online Only'
            WHEN online_order = 'No'  AND book_table = 'Yes' THEN 'Booking Only'
            ELSE 'Neither'
        END AS feature_combination,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(votes), 0) AS avg_votes,
        ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
    FROM restaurants
    WHERE rating IS NOT NULL
    GROUP BY feature_combination
    ORDER BY avg_rating DESC;
    """
)


# ========================
# Q14: What combination of factors maximizes restaurant success?
# ========================
# SQL: Group by multiple factors (pricing + online + booking)
#      to find the winning combination
# ========================

run_query(14,
    "What combination of factors maximizes restaurant success?",
    """
    SELECT 
        pricing_segment,
        online_order,
        book_table,
        COUNT(*) AS restaurant_count,
        ROUND(AVG(rating), 2) AS avg_rating,
        ROUND(AVG(votes), 0) AS avg_votes
    FROM restaurants
    WHERE rating IS NOT NULL
        AND pricing_segment != 'Unknown'
    GROUP BY pricing_segment, online_order, book_table
    HAVING COUNT(*) >= 10
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
)


# ========================
# Q15: Which restaurants are top performers within each pricing segment?
# ========================
# SQL: Uses a subquery to rank restaurants within each pricing segment
# This finds the "best of the best" in each price category
# ========================

run_query(15,
    "Which restaurants are top performers within each pricing segment?",
    """
    SELECT 
        pricing_segment,
        restaurant_name,
        location,
        rating,
        votes,
        approx_cost_for_two
    FROM restaurants
    WHERE rating IS NOT NULL
        AND pricing_segment != 'Unknown'
        AND rating >= 4.5
        AND votes >= 500
    ORDER BY pricing_segment, rating DESC, votes DESC;
    """
)


# --------------------------------------------------------------------------
# SECTION 6: BONUS - ORDER DATA QUERIES
# --------------------------------------------------------------------------
# These queries analyze the order dataset and will power the
# "Order Data Q&A" page in the Streamlit app.
# --------------------------------------------------------------------------

print("\n" + "=" * 70)
print("STEP 4: ORDER DATA QUERIES")
print("=" * 70)


# Order Q1: Total revenue by payment method
run_query("O1",
    "What is the total revenue by payment method?",
    """
    SELECT 
        payment_method,
        COUNT(*) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_revenue,
        ROUND(AVG(order_value), 2) AS avg_order_value
    FROM orders
    GROUP BY payment_method
    ORDER BY total_revenue DESC;
    """
)


# Order Q2: Monthly order trends
run_query("O2",
    "What are the monthly order trends?",
    """
    SELECT 
        SUBSTR(order_date, 1, 7) AS month,
        COUNT(*) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_revenue,
        ROUND(AVG(order_value), 2) AS avg_order_value
    FROM orders
    GROUP BY month
    ORDER BY month;
    """
)


# Order Q3: Top restaurants by order volume
run_query("O3",
    "Which restaurants receive the most orders?",
    """
    SELECT 
        restaurant_name,
        COUNT(*) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_revenue,
        ROUND(AVG(order_value), 2) AS avg_order_value
    FROM orders
    GROUP BY restaurant_name
    ORDER BY total_orders DESC
    LIMIT 10;
    """
)


# Order Q4: Discount impact on order value
run_query("O4",
    "Does discount usage affect average order value?",
    """
    SELECT 
        discount_used,
        COUNT(*) AS total_orders,
        ROUND(AVG(order_value), 2) AS avg_order_value,
        ROUND(MIN(order_value), 2) AS min_order_value,
        ROUND(MAX(order_value), 2) AS max_order_value
    FROM orders
    GROUP BY discount_used;
    """
)


# Order Q5: Combined - Restaurant ratings vs order performance
run_query("O5",
    "How do restaurant ratings relate to order performance?",
    """
    SELECT 
        r.rating_category,
        COUNT(DISTINCT r.restaurant_name) AS restaurant_count,
        COUNT(o.order_id) AS total_orders,
        ROUND(AVG(o.order_value), 2) AS avg_order_value,
        ROUND(SUM(o.order_value), 2) AS total_revenue
    FROM restaurants r
    INNER JOIN orders o ON r.restaurant_name = o.restaurant_name
    WHERE r.rating_category != 'Unrated'
    GROUP BY r.rating_category
    ORDER BY avg_order_value DESC;
    """
)


# Order Q6: Revenue breakdown by pricing segment
# SQL: JOIN restaurants with orders to get pricing_segment for each order
# GROUP BY pricing_segment to see which tier drives the most revenue
run_query("O6",
    "What is the revenue breakdown by pricing segment?",
    """
    SELECT 
        r.pricing_segment,
        COUNT(DISTINCT r.restaurant_name) AS restaurant_count,
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(o.order_value), 2) AS total_revenue,
        ROUND(AVG(o.order_value), 2) AS avg_order_value
    FROM restaurants r
    INNER JOIN orders o ON r.restaurant_name = o.restaurant_name
    WHERE r.pricing_segment != 'Unknown'
    GROUP BY r.pricing_segment
    ORDER BY total_revenue DESC;
    """
)


# Order Q7: Which locations generate the highest order revenue?
# SQL: JOIN is essential here because orders table has NO location column
# We get location from the restaurants table via restaurant_name match
run_query("O7",
    "Which locations generate the highest order revenue?",
    """
    SELECT 
        r.location,
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(o.order_value), 2) AS total_revenue,
        ROUND(AVG(o.order_value), 2) AS avg_order_value
    FROM restaurants r
    INNER JOIN orders o ON r.restaurant_name = o.restaurant_name
    GROUP BY r.location
    ORDER BY total_revenue DESC
    LIMIT 15;
    """
)


# Order Q8: Discount usage pattern by payment method
# SQL: GROUP BY two columns creates 6 groups (3 methods × 2 discount states)
# This reveals discount usage patterns within each payment method
run_query("O8",
    "What is the discount usage pattern by payment method?",
    """
    SELECT 
        payment_method,
        discount_used,
        COUNT(*) AS total_orders,
        ROUND(AVG(order_value), 2) AS avg_order_value,
        ROUND(SUM(order_value), 2) AS total_revenue
    FROM orders
    GROUP BY payment_method, discount_used
    ORDER BY payment_method, discount_used;
    """
)


# Order Q9: Which day of the week has the most orders?
# SQL: strftime('%w', date) extracts day-of-week (0=Sunday, 6=Saturday)
# CAST converts text to integer for proper sorting
# CASE WHEN maps numbers to readable day names
run_query("O9",
    "Which day of the week has the most orders?",
    """
    SELECT 
        CASE CAST(strftime('%w', order_date) AS INTEGER)
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            WHEN 2 THEN 'Tuesday'
            WHEN 3 THEN 'Wednesday'
            WHEN 4 THEN 'Thursday'
            WHEN 5 THEN 'Friday'
            WHEN 6 THEN 'Saturday'
        END AS day_of_week,
        CAST(strftime('%w', order_date) AS INTEGER) AS day_num,
        COUNT(*) AS total_orders,
        ROUND(AVG(order_value), 2) AS avg_order_value,
        ROUND(SUM(order_value), 2) AS total_revenue
    FROM orders
    GROUP BY day_of_week, day_num
    ORDER BY day_num;
    """
)


# Order Q10: Top restaurant + payment method combinations by revenue
# SQL: GROUP BY two columns (restaurant + payment) for granular analysis
# HAVING COUNT(*) >= 5 filters rare combinations that aren't meaningful
run_query("O10",
    "What are the top restaurant + payment method combinations by revenue?",
    """
    SELECT 
        restaurant_name,
        payment_method,
        COUNT(*) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_revenue,
        ROUND(AVG(order_value), 2) AS avg_order_value
    FROM orders
    GROUP BY restaurant_name, payment_method
    HAVING COUNT(*) >= 5
    ORDER BY total_revenue DESC
    LIMIT 15;
    """
)


# --------------------------------------------------------------------------
# SECTION 7: CLOSE DATABASE & SUMMARY
# --------------------------------------------------------------------------

conn.close()
print(f"\n🔒 Database connection closed.")

print("\n" + "=" * 70)
print("✅ STEP 2 COMPLETE: DATABASE SETUP SUMMARY")
print("=" * 70)

print(f"""
🗄️  DATABASE CREATED:
    File: {DB_PATH}
    Tables: restaurants ({len(df_restaurant)} rows), orders ({len(df_orders)} rows)

📝 SQL QUERIES TESTED:
    ✅ Q1-Q15:  Restaurant business questions (all working)
    ✅ O1-O10:  Order analysis questions (all working)

📚 SQL CONCEPTS USED:
    • SELECT, FROM, WHERE          → Basic querying
    • GROUP BY, HAVING             → Grouping & filtering groups
    • ORDER BY, LIMIT              → Sorting & limiting results
    • AVG(), COUNT(), SUM(), ROUND() → Aggregate functions
    • CASE WHEN                    → Conditional logic
    • INNER JOIN                   → Combining tables
    • SUBSTR()                     → String functions
    • Subqueries                   → Queries within queries

👉 NEXT: Run Step 3 → streamlit run app/streamlit_app.py
""")
