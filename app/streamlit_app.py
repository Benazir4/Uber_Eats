# ============================================================================
# STEP 3: STREAMLIT APPLICATION
# ============================================================================
# Project : Uber Eats Bangalore Restaurant Intelligence & Decision Support
# Purpose : Interactive web app with Dashboard, Q&A, and Order Analysis pages
# Author  : [Your Name]
#
# HOW TO RUN:
#   1. Make sure Step 1 & Step 2 have been run (database exists)
#   2. Open VS Code Terminal (Ctrl + `)
#   3. Run: streamlit run app/streamlit_app.py
#   4. A browser window will open automatically at http://localhost:8501
#
# WHAT IS STREAMLIT?
#   Streamlit is a Python library that turns your Python scripts into
#   interactive web applications. No HTML/CSS/JavaScript needed!
#   You write Python → Streamlit creates the web interface.
# ============================================================================


# --------------------------------------------------------------------------
# SECTION 1: IMPORT LIBRARIES
# --------------------------------------------------------------------------
# streamlit  → the web app framework (imported as "st" for short)
# pandas     → for working with DataFrames (tables)
# sqlite3    → to connect to our SQLite database
# os         → for file paths
# --------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import sqlite3
import os


# --------------------------------------------------------------------------
# SECTION 2: PAGE CONFIGURATION
# --------------------------------------------------------------------------
# st.set_page_config() MUST be the first Streamlit command in the script.
# It sets the browser tab title, icon, and layout width.
#
# layout="wide" → uses the full width of the browser
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="Uber Eats Bangalore Intelligence",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------------------------------
# SECTION 3: DATABASE CONNECTION
# --------------------------------------------------------------------------
# We create a helper function to connect to SQLite and run queries.
#
# @st.cache_resource → Streamlit caches this so we don't reconnect every time
#                      the user interacts with the app. Makes it faster!
#
# get_connection()   → Returns a database connection
# run_query(query)   → Runs a SQL query and returns results as a DataFrame
# --------------------------------------------------------------------------

# Find the database file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "database", "uber_eats.db")


@st.cache_resource
def get_connection():
    """
    Create and cache a database connection.
    check_same_thread=False allows Streamlit to use it across interactions.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def run_query(query, params=None):
    """
    Run a SQL query and return results as a pandas DataFrame.

    Parameters:
        query (str)   : SQL query string
        params (tuple) : Optional parameters for parameterized queries

    Returns:
        pandas DataFrame with the query results
    """
    conn = get_connection()
    if params:
        return pd.read_sql_query(query, conn, params=params)
    return pd.read_sql_query(query, conn)


# --------------------------------------------------------------------------
# SECTION 4: SIDEBAR NAVIGATION
# --------------------------------------------------------------------------
# The sidebar lets users switch between the 3 pages.
# st.sidebar creates elements in the left panel.
# --------------------------------------------------------------------------

st.sidebar.title("🍔 Uber Eats Bangalore")
st.sidebar.markdown("### Restaurant Intelligence System")
st.sidebar.markdown("---")

# Page selection
page = st.sidebar.radio(
    "📄 Navigate to:",
    ["🏠 Dashboard", "❓ Q&A - Restaurant Analysis", "📦 Q&A - Order Analysis", "🍽️ Q&A - Individual Cuisine Analysis"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Tech Stack:**")
st.sidebar.markdown("Python • Pandas • SQLite • Streamlit")
st.sidebar.markdown("---")
st.sidebar.caption("Uber Eats Bangalore Intelligence & Decision Support System")


# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================
# This page provides interactive filters for users to explore the data.
# All filtering is done through SQL queries (not pandas filtering).
# Users can filter by location, cuisine, pricing, online ordering, etc.
# ============================================================================

if page == "🏠 Dashboard":

    st.title("🏠 Dashboard - Restaurant Explorer")
    st.markdown("Use the filters below to explore Uber Eats Bangalore restaurant data. "
                "All results are fetched dynamically using **SQL queries**.")
    st.markdown("---")

    # ---- Get unique values for filter dropdowns ----
    # We query the database to get all unique locations, cuisines, etc.
    locations = run_query("SELECT DISTINCT location FROM restaurants ORDER BY location;")
    pricing_segments = run_query("SELECT DISTINCT pricing_segment FROM restaurants WHERE pricing_segment != 'Unknown' ORDER BY pricing_segment;")
    restaurant_types = run_query("SELECT DISTINCT restaurant_type FROM restaurants ORDER BY restaurant_type;")

    # ---- Filter Controls ----
    # st.columns() creates side-by-side columns for a cleaner layout
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_location = st.selectbox(
            "📍 Location",
            options=["All"] + locations['location'].tolist(),
            index=0
        )

    with col2:
        selected_pricing = st.selectbox(
            "💰 Pricing Segment",
            options=["All"] + pricing_segments['pricing_segment'].tolist(),
            index=0
        )

    with col3:
        selected_rest_type = st.selectbox(
            "🍽️ Restaurant Type",
            options=["All"] + restaurant_types['restaurant_type'].tolist(),
            index=0
        )

    # Second row of filters
    col4, col5, col6 = st.columns(3)

    with col4:
        selected_online = st.selectbox(
            "🛒 Online Order",
            options=["All", "Yes", "No"],
            index=0
        )

    with col5:
        selected_booking = st.selectbox(
            "📅 Table Booking",
            options=["All", "Yes", "No"],
            index=0
        )

    with col6:
        min_rating = st.slider(
            "⭐ Minimum Rating",
            min_value=1.0,
            max_value=5.0,
            value=1.0,
            step=0.1
        )

    # ---- Build SQL Query Dynamically ----
    # We start with a base query and add WHERE conditions based on filters.
    # This is called "dynamic query building" - very common in real applications.
    #
    # We use parameterized queries (? placeholders) to prevent SQL injection,
    # which is a security best practice.

    query = """
        SELECT
            restaurant_name,
            location,
            cuisines,
            rating,
            votes,
            approx_cost_for_two,
            online_order,
            book_table,
            pricing_segment,
            rating_category,
            restaurant_type
        FROM restaurants
        WHERE rating IS NOT NULL
    """

    params = []

    if selected_location != "All":
        query += " AND location = ?"
        params.append(selected_location)

    if selected_pricing != "All":
        query += " AND pricing_segment = ?"
        params.append(selected_pricing)

    if selected_rest_type != "All":
        query += " AND restaurant_type = ?"
        params.append(selected_rest_type)

    if selected_online != "All":
        query += " AND online_order = ?"
        params.append(selected_online)

    if selected_booking != "All":
        query += " AND book_table = ?"
        params.append(selected_booking)

    query += " AND rating >= ?"
    params.append(min_rating)

    query += " ORDER BY rating DESC, votes DESC"

    # ---- Execute Query and Display Results ----
    results = run_query(query, tuple(params))

    # Summary metrics
    st.markdown("---")
    st.subheader("📊 Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Restaurants", f"{len(results):,}")
    m2.metric("Avg Rating", f"{results['rating'].mean():.2f}" if len(results) > 0 else "N/A")
    m3.metric("Avg Cost for Two", f"₹{results['approx_cost_for_two'].mean():.0f}" if len(results) > 0 else "N/A")
    m4.metric("Avg Votes", f"{results['votes'].mean():.0f}" if len(results) > 0 else "N/A")

    # Display the data table
    st.markdown("---")
    st.subheader(f"📋 Restaurant Data ({len(results)} results)")

    if len(results) > 0:
        st.dataframe(
            results,
            use_container_width=True,
            height=500
        )
    else:
        st.warning("No restaurants match your filter criteria. Try adjusting the filters.")

    # ---- Location-wise Summary ----
    if len(results) > 0 and selected_location == "All":
        st.markdown("---")
        st.subheader("📍 Location-wise Summary")
        location_summary = run_query("""
            SELECT
                location,
                COUNT(*) AS restaurant_count,
                ROUND(AVG(rating), 2) AS avg_rating,
                ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
            FROM restaurants
            WHERE rating IS NOT NULL
            GROUP BY location
            ORDER BY restaurant_count DESC
            LIMIT 15;
        """)
        st.dataframe(location_summary, use_container_width=True)


# ============================================================================
# PAGE 2: Q&A - RESTAURANT ANALYSIS (15 Business Questions)
# ============================================================================
# Displays pre-built SQL queries answering 15 business questions.
# Each question shows the SQL query used and the result table.
# ============================================================================

elif page == "❓ Q&A - Restaurant Analysis":

    st.title("❓ Q&A - Restaurant Business Analysis")
    st.markdown("Explore answers to **15 key business questions** about Uber Eats Bangalore restaurants. "
                "Each answer is generated through **SQL-based computation** and displayed as a table.")
    st.markdown("---")

    # ---- Define all 15 questions with their SQL queries ----
    # Each question is a dictionary with: number, title, business_value, and sql

    questions = [
        {
            "num": 1,
            "title": "Which Bangalore locations have the highest average restaurant ratings?",
            "business_value": "Identifies premium-performing areas suitable for brand positioning and new partner onboarding.",
            "sql": """
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
        },
        {
            "num": 2,
            "title": "Which locations are over-saturated with restaurants?",
            "business_value": "Helps avoid overcrowded markets and guides smarter expansion decisions.",
            "sql": """
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
        },
        {
            "num": 3,
            "title": "Does online ordering improve restaurant ratings?",
            "business_value": "Evaluates the ROI of Uber Eats' online ordering feature for partners.",
            "sql": """
                SELECT
                    online_order,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(votes), 0) AS avg_votes
                FROM restaurants
                WHERE rating IS NOT NULL
                GROUP BY online_order;
            """
        },
        {
            "num": 4,
            "title": "Does table booking correlate with higher customer ratings?",
            "business_value": "Measures the effectiveness of table booking as a premium feature.",
            "sql": """
                SELECT
                    book_table,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM restaurants
                WHERE rating IS NOT NULL
                GROUP BY book_table;
            """
        },
        {
            "num": 5,
            "title": "What price range delivers the best customer satisfaction?",
            "business_value": "Helps define the optimal pricing segment for partner success.",
            "sql": """
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
        },
        {
            "num": 6,
            "title": "How do low, mid, and premium-priced restaurants perform in terms of ratings?",
            "business_value": "Supports pricing-based market segmentation strategies.",
            "sql": """
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
        },
        {
            "num": 7,
            "title": "Which cuisines are most common in Bangalore?",
            "business_value": "Reveals market demand and cuisine saturation levels.",
            "sql": """
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
        },
        {
            "num": 8,
            "title": "Which cuisines receive the highest average ratings?",
            "business_value": "Identifies high-quality cuisine categories suitable for promotion.",
            "sql": """
                SELECT
                    cuisines,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM restaurants
                WHERE rating IS NOT NULL
                GROUP BY cuisines
                HAVING COUNT(*) >= 20
                ORDER BY avg_rating DESC
                LIMIT 10;
            """
        },
        {
            "num": 9,
            "title": "Which cuisines perform well despite having fewer restaurants?",
            "business_value": "Highlights niche opportunities for differentiation.",
            "sql": """
                SELECT
                    cuisines,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM restaurants
                WHERE rating IS NOT NULL
                GROUP BY cuisines
                HAVING COUNT(*) BETWEEN 5 AND 30
                ORDER BY avg_rating DESC
                LIMIT 10;
            """
        },
        {
            "num": 10,
            "title": "What is the relationship between restaurant cost and rating?",
            "business_value": "Determines whether higher pricing translates to better customer perception.",
            "sql": """
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
        },
        {
            "num": 11,
            "title": "Which locations are ideal for premium restaurant onboarding?",
            "business_value": "Combines cost, rating, and location insights to guide premium expansion.",
            "sql": """
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
        },
        {
            "num": 12,
            "title": "Which locations show high demand but lower average ratings?",
            "business_value": "Indicates areas where quality improvement initiatives are needed.",
            "sql": """
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
        },
        {
            "num": 13,
            "title": "Do restaurants offering both online ordering and table booking perform better?",
            "business_value": "Validates bundled feature adoption for partners.",
            "sql": """
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
        },
        {
            "num": 14,
            "title": "What combination of factors maximizes restaurant success?",
            "business_value": "Supports strategic partner recommendations (Pricing + Location + Features).",
            "sql": """
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
        },
        {
            "num": 15,
            "title": "Which restaurants are top performers within each pricing segment?",
            "business_value": "Helps identify benchmark partners and best practices.",
            "sql": """
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
                    AND votes >= 1000
                ORDER BY pricing_segment, rating DESC, votes DESC;
            """
        }
    ]

    # ---- Question Selector ----
    # Let user pick which question to view, or show all at once
    view_mode = st.radio(
        "View mode:",
        ["Select a question", "Show all questions"],
        horizontal=True
    )

    if view_mode == "Select a question":
        # Dropdown to select a specific question
        question_options = [f"Q{q['num']}: {q['title']}" for q in questions]
        selected = st.selectbox("Select a business question:", question_options)
        selected_idx = question_options.index(selected)
        questions_to_show = [questions[selected_idx]]
    else:
        questions_to_show = questions

    # ---- Display Questions and Results ----
    for q in questions_to_show:
        st.markdown("---")
        st.subheader(f"Q{q['num']}: {q['title']}")
        st.markdown(f"**💼 Business Value:** {q['business_value']}")

        # Show/hide SQL query with an expander
        with st.expander("🔍 View SQL Query"):
            st.code(q['sql'].strip(), language="sql")

        # Run query and display results
        result = run_query(q['sql'])
        st.dataframe(result, use_container_width=True)
        st.caption(f"📊 {len(result)} rows returned")


# ============================================================================
# PAGE 3: Q&A - ORDER ANALYSIS
# ============================================================================
# Analyzes the order dataset with SQL queries.
# Includes both predefined questions and a combined restaurant+order analysis.
# ============================================================================

elif page == "📦 Q&A - Order Analysis":

    st.title("📦 Q&A - Order Data Analysis")
    st.markdown("Explore insights from the **order dataset** (25,000 orders). "
                "Includes revenue analysis, payment trends, and combined restaurant-order insights.")
    st.markdown("---")

    # ---- Quick Metrics ----
    st.subheader("📊 Order Overview")
    metrics = run_query("""
        SELECT
            COUNT(*) AS total_orders,
            COUNT(DISTINCT restaurant_name) AS unique_restaurants,
            ROUND(SUM(order_value), 2) AS total_revenue,
            ROUND(AVG(order_value), 2) AS avg_order_value,
            MIN(order_date) AS first_order,
            MAX(order_date) AS last_order
        FROM orders;
    """)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Orders", f"{metrics['total_orders'].iloc[0]:,}")
    m2.metric("Unique Restaurants", f"{metrics['unique_restaurants'].iloc[0]:,}")
    m3.metric("Total Revenue", f"₹{metrics['total_revenue'].iloc[0]:,.0f}")
    m4.metric("Avg Order Value", f"₹{metrics['avg_order_value'].iloc[0]:,.2f}")

    st.markdown("---")

    # ---- Define Order Questions ----
    order_questions = [
        {
            "num": 1,
            "title": "What is the total revenue by payment method?",
            "business_value": "Understand payment preferences to optimize checkout experience.",
            "sql": """
                SELECT
                    payment_method,
                    COUNT(*) AS total_orders,
                    ROUND(SUM(order_value), 2) AS total_revenue,
                    ROUND(AVG(order_value), 2) AS avg_order_value
                FROM orders
                GROUP BY payment_method
                ORDER BY total_revenue DESC;
            """
        },
        {
            "num": 2,
            "title": "What are the monthly order trends?",
            "business_value": "Identify seasonal patterns and growth trends for strategic planning.",
            "sql": """
                SELECT
                    SUBSTR(order_date, 1, 7) AS month,
                    COUNT(*) AS total_orders,
                    ROUND(SUM(order_value), 2) AS total_revenue,
                    ROUND(AVG(order_value), 2) AS avg_order_value
                FROM orders
                GROUP BY month
                ORDER BY month;
            """
        },
        {
            "num": 3,
            "title": "Which restaurants receive the most orders?",
            "business_value": "Identify top-performing partners for rewards and case studies.",
            "sql": """
                SELECT
                    restaurant_name,
                    COUNT(*) AS total_orders,
                    ROUND(SUM(order_value), 2) AS total_revenue,
                    ROUND(AVG(order_value), 2) AS avg_order_value
                FROM orders
                GROUP BY restaurant_name
                ORDER BY total_orders DESC
                LIMIT 15;
            """
        },
        {
            "num": 4,
            "title": "Does discount usage affect average order value?",
            "business_value": "Evaluate discount strategy effectiveness and ROI.",
            "sql": """
                SELECT
                    discount_used,
                    COUNT(*) AS total_orders,
                    ROUND(AVG(order_value), 2) AS avg_order_value,
                    ROUND(MIN(order_value), 2) AS min_order_value,
                    ROUND(MAX(order_value), 2) AS max_order_value
                FROM orders
                GROUP BY discount_used;
            """
        },
        {
            "num": 5,
            "title": "How do restaurant ratings relate to order performance?",
            "business_value": "Understand if higher-rated restaurants generate more revenue.",
            "sql": """
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
        },
        {
            "num": 6,
            "title": "What is the revenue breakdown by pricing segment?",
            "business_value": "Understand which pricing tiers drive the most order revenue.",
            "sql": """
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
        },
        {
            "num": 7,
            "title": "Which locations generate the highest order revenue?",
            "business_value": "Identify high-revenue areas for marketing and operations focus.",
            "sql": """
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
        },
        {
            "num": 8,
            "title": "What is the discount usage pattern by payment method?",
            "business_value": "Optimize payment-specific promotional strategies.",
            "sql": """
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
        },
        {
            "num": 9,
            "title": "Which day of the week has the most orders?",
            "business_value": "Plan staffing and promotions around peak ordering days.",
            "sql": """
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
        },
        {
            "num": 10,
            "title": "What are the top restaurant + payment method combinations by revenue?",
            "business_value": "Identify key revenue drivers for partnership and payment optimization.",
            "sql": """
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
        }
    ]

    # ---- Question Selector ----
    view_mode = st.radio(
        "View mode:",
        ["Select a question", "Show all questions"],
        horizontal=True,
        key="order_view_mode"
    )

    if view_mode == "Select a question":
        question_options = [f"Q{q['num']}: {q['title']}" for q in order_questions]
        selected = st.selectbox("Select an order analysis question:", question_options)
        selected_idx = question_options.index(selected)
        questions_to_show = [order_questions[selected_idx]]
    else:
        questions_to_show = order_questions

    # ---- Display Questions and Results ----
    for q in questions_to_show:
        st.markdown("---")
        st.subheader(f"Q{q['num']}: {q['title']}")
        st.markdown(f"**💼 Business Value:** {q['business_value']}")

        with st.expander("🔍 View SQL Query"):
            st.code(q['sql'].strip(), language="sql")

        result = run_query(q['sql'])
        st.dataframe(result, use_container_width=True)
        st.caption(f"📊 {len(result)} rows returned")


# ============================================================================
# PAGE 4: Q&A - INDIVIDUAL CUISINE ANALYSIS
# ============================================================================
# The cuisines column has combined values like "North Indian, Chinese, Thai".
# The cuisine_split table splits these into individual rows, enabling
# analysis of each cuisine independently (e.g., just "Chinese" across all
# restaurants that serve Chinese food, regardless of what else they serve).
# ============================================================================

elif page == "🍽️ Q&A - Individual Cuisine Analysis":

    st.title("🍽️ Q&A - Individual Cuisine Analysis")
    st.markdown("Analyze **individual cuisines** independently. The original data has combined cuisines "
                "like 'North Indian, Chinese, Thai'. Here, each cuisine is split into its own row — "
                "so we can see how 'Chinese' performs across ALL restaurants that serve it.")
    st.markdown("---")

    # ---- Quick Metrics ----
    st.subheader("📊 Cuisine Overview")
    metrics = run_query("""
        SELECT
            COUNT(DISTINCT cuisine_individual) AS unique_cuisines,
            COUNT(DISTINCT restaurant_name) AS total_restaurants,
            COUNT(*) AS total_rows,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM cuisine_split
        WHERE rating IS NOT NULL;
    """)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Unique Cuisines", f"{metrics['unique_cuisines'].iloc[0]:,}")
    m2.metric("Restaurants", f"{metrics['total_restaurants'].iloc[0]:,}")
    m3.metric("Cuisine-Restaurant Pairs", f"{metrics['total_rows'].iloc[0]:,}")
    m4.metric("Overall Avg Rating", f"{metrics['avg_rating'].iloc[0]}")

    st.markdown("---")

    # ---- Define Cuisine Questions ----
    cuisine_questions = [
        {
            "num": 1,
            "title": "Which individual cuisines have the highest average ratings?",
            "business_value": "Identifies the best-performing cuisines for promotion and partner strategy — independent of what other cuisines the restaurant also serves.",
            "sql": """
                SELECT
                    cuisine_individual,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM cuisine_split
                WHERE rating IS NOT NULL
                GROUP BY cuisine_individual
                HAVING COUNT(*) >= 20
                ORDER BY avg_rating DESC
                LIMIT 10;
            """
        },
        {
            "num": 2,
            "title": "Which individual cuisines are most common in Bangalore?",
            "business_value": "Shows market saturation per cuisine — helps identify over-served and under-served categories.",
            "sql": """
                SELECT
                    cuisine_individual,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM cuisine_split
                WHERE rating IS NOT NULL
                GROUP BY cuisine_individual
                ORDER BY restaurant_count DESC
                LIMIT 15;
            """
        },
        {
            "num": 3,
            "title": "Which niche cuisines perform well despite having few restaurants?",
            "business_value": "Highlights untapped opportunities — cuisines with high customer satisfaction but low availability on the platform.",
            "sql": """
                SELECT
                    cuisine_individual,
                    ROUND(AVG(rating), 2) AS avg_rating,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(approx_cost_for_two), 0) AS avg_cost
                FROM cuisine_split
                WHERE rating IS NOT NULL
                GROUP BY cuisine_individual
                HAVING COUNT(*) BETWEEN 10 AND 50
                ORDER BY avg_rating DESC
                LIMIT 10;
            """
        },
        {
            "num": 4,
            "title": "How do individual cuisines perform across pricing segments?",
            "business_value": "Shows which cuisines excel at different price points — guiding pricing strategy per cuisine type.",
            "sql": """
                SELECT
                    cuisine_individual,
                    pricing_segment,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(rating), 2) AS avg_rating
                FROM cuisine_split
                WHERE rating IS NOT NULL
                    AND pricing_segment != 'Unknown'
                GROUP BY cuisine_individual, pricing_segment
                HAVING COUNT(*) >= 10
                ORDER BY avg_rating DESC
                LIMIT 15;
            """
        },
        {
            "num": 5,
            "title": "Does online ordering affect ratings differently for each cuisine?",
            "business_value": "Reveals which cuisines benefit from or are hurt by online ordering — guiding feature recommendations per cuisine.",
            "sql": """
                SELECT
                    cuisine_individual,
                    online_order,
                    COUNT(*) AS restaurant_count,
                    ROUND(AVG(rating), 2) AS avg_rating
                FROM cuisine_split
                WHERE rating IS NOT NULL
                GROUP BY cuisine_individual, online_order
                HAVING COUNT(*) >= 20
                ORDER BY cuisine_individual, online_order;
            """
        }
    ]

    # ---- Question Selector ----
    view_mode = st.radio(
        "View mode:",
        ["Select a question", "Show all questions"],
        horizontal=True,
        key="cuisine_view_mode"
    )

    if view_mode == "Select a question":
        question_options = [f"Q{q['num']}: {q['title']}" for q in cuisine_questions]
        selected = st.selectbox("Select a cuisine analysis question:", question_options)
        selected_idx = question_options.index(selected)
        questions_to_show = [cuisine_questions[selected_idx]]
    else:
        questions_to_show = cuisine_questions

    # ---- Display Questions and Results ----
    for q in questions_to_show:
        st.markdown("---")
        st.subheader(f"Q{q['num']}: {q['title']}")
        st.markdown(f"**💼 Business Value:** {q['business_value']}")

        with st.expander("🔍 View SQL Query"):
            st.code(q['sql'].strip(), language="sql")

        result = run_query(q['sql'])
        st.dataframe(result, use_container_width=True)
        st.caption(f"📊 {len(result)} rows returned")


# --------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Uber Eats Bangalore Restaurant Intelligence & Decision Support System | "
    "Built with Python, Pandas, SQLite & Streamlit"
    "</div>",
    unsafe_allow_html=True
)
