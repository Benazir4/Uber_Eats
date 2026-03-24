# 🍔 Uber Eats Bangalore Restaurant Intelligence & Decision Support System

A data-driven decision support system that analyzes Uber Eats Bangalore restaurant data to answer critical business questions. Built with **Python, Pandas, SQLite, and Streamlit**, this project delivers actionable insights through a clean, tabular Streamlit dashboard — no charts or visualizations, just precise data.

---

## 📌 Problem Statement

Uber Eats operates a large-scale restaurant marketplace where business success depends on factors such as location strategy, pricing, cuisine mix, customer ratings, and platform features like online ordering and table booking.

This project analyzes Uber Eats Bangalore restaurant data and builds a decision support system that answers critical business questions using Python and SQL, presenting results as clean tabular DataFrame outputs in Streamlit.

---

## 🎯 Business Use Cases

- **Location Intelligence** — Identify top-performing and over-saturated areas
- **Partner Onboarding Strategy** — Find ideal locations for new restaurant partners
- **Pricing Optimization** — Discover the price range that maximizes customer satisfaction
- **Cuisine Performance Analysis** — Uncover high-performing and niche cuisines
- **Product Feature Impact** — Evaluate the effect of online ordering and table booking on ratings
- **Market Segmentation** — Segment restaurants by pricing, rating, and features
- **Customer Satisfaction Drivers** — Identify what drives higher ratings
- **Expansion Planning** — Locate areas needing quality improvement

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Database | SQLite (cursor-based SQL) |
| Web Application | Streamlit |
| IDE | Visual Studio Code |

---

## 📁 Project Structure

```
uber_eats_project/
│
├── data/
│   ├── raw/                              # Original untouched data files
│   │   ├── Uber_Eats_data.csv               # Restaurant dataset (23,193 rows)
│   │   └── orders.json                      # Order dataset (25,000 records)
│   │
│   └── cleaned/                          # Cleaned & preprocessed data
│       ├── cleaned_restaurant_data.csv      # Cleaned restaurant data (23,158 rows)
│       └── cleaned_orders_data.csv          # Cleaned order data (25,000 rows)
│
├── database/                             # SQLite database
│   └── uber_eats.db                         # Database with restaurants & orders tables
│
├── scripts/                              # Python scripts
│   ├── step1_data_cleaning.py               # Data cleaning & preprocessing
│   └── step2_database_setup.py              # Database creation & SQL query testing
│
├── app/                                  # Streamlit application
│   └── streamlit_app.py                     # Main app (Dashboard + Q&A pages)
│
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore rules
└── README.md                             # This file
```

---

## 🔄 Application Flowchart

The complete data pipeline and application flow — from raw data to business decisions:

![Application Flowchart](Application_Flowchart.png)

**Flow summary:**
1. **Raw Data** → CSV (23,193 restaurants) + JSON (25,000 orders)
2. **Step 1: Data Cleaning** → Remove duplicates, clean ratings/costs, handle missing values, feature engineering
3. **Step 2: Database Setup** → Load into SQLite with 2 tables (restaurants + orders) linked by `restaurant_name`
4. **Step 3: Streamlit App** → 3-page interactive dashboard:
   - **Dashboard** → 6 dynamic filters → parameterized SQL → metrics + filtered table
   - **Restaurant Q&A** → 15 business questions → SQL execution → result tables
   - **Order Q&A** → 10 order questions (with JOINs) → SQL execution → result tables
5. **Output** → DataFrame results displayed in browser → Business decisions

---

## 📊 Datasets

### 1. Restaurant Data (CSV) — 23,193 rows × 13 columns
| Column | Description |
|--------|-------------|
| restaurant_name | Name of the restaurant |
| location | Bangalore area/neighborhood (88 unique) |
| cuisines | Types of cuisine offered |
| rating | Customer rating (1.8 - 4.9) |
| votes | Number of customer votes |
| approx_cost_for_two | Approximate cost for two people (₹) |
| online_order | Online ordering available (Yes/No) |
| book_table | Table booking available (Yes/No) |
| restaurant_type | Type (Casual Dining, Cafe, Quick Bites, etc.) |

### 2. Order Data (JSON) — 25,000 records
| Column | Description |
|--------|-------------|
| order_id | Unique order identifier |
| restaurant_name | Restaurant that received the order |
| order_date | Date of the order |
| order_value | Order amount in ₹ |
| discount_used | Whether discount was applied (Yes/No) |
| payment_method | Card / Cash / UPI |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Visual Studio Code (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/uber-eats-bangalore-intelligence.git
cd uber-eats-bangalore-intelligence
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Data Cleaning
```bash
python scripts/step1_data_cleaning.py
```

### Step 5: Set Up Database
```bash
python scripts/step2_database_setup.py
```

### Step 6: Launch Streamlit App
```bash
streamlit run app/streamlit_app.py
```
The app will open in your browser at `http://localhost:8501`

---

## 📱 Application Pages

### Page 1: 🏠 Dashboard
Interactive restaurant explorer with dynamic SQL-based filtering:
- Location, Pricing Segment, Restaurant Type
- Online Ordering, Table Booking, Minimum Rating
- Summary metrics and full filtered data table

### Page 2: ❓ Q&A — Restaurant Analysis (15 Questions)
SQL-powered answers to key business questions including:
1. Highest-rated locations in Bangalore
2. Over-saturated restaurant locations
3. Impact of online ordering on ratings
4. Table booking correlation with ratings
5. Best price range for customer satisfaction
6. Performance across pricing tiers
7. Most common cuisines
8. Highest-rated cuisines
9. High-performing niche cuisines
10. Cost vs. rating relationship
11. Ideal locations for premium onboarding
12. High-demand, low-rating locations
13. Impact of combined features (online + booking)
14. Success factor combinations
15. Top performers per pricing segment

### Page 3: 📦 Q&A — Order Analysis (10 Questions)
Order dataset insights including revenue analysis, monthly trends, discount impact, payment patterns, day-of-week trends, and combined restaurant-order analysis using SQL JOINs.

---

## 📈 Key Findings

| Insight | Finding |
|---------|---------|
| Best-rated locations | Lavelle Road (4.19), Koramangala 5th Block (4.15) |
| Most saturated area | Koramangala 5th Block (1,759 restaurants) |
| Table booking impact | 4.16 avg rating (with) vs 3.81 (without) |
| Best pricing segment | Premium restaurants: 4.07 avg rating |
| Most common cuisine | North Indian (1,136 restaurants) |
| Discount effect on orders | ₹1,150 avg (with discount) vs ₹822 (without) |
| Payment distribution | Card, Cash, UPI nearly equally split |
| Higher cost = Higher rating | ₹1500+ restaurants avg 4.23 rating |

---

## 🔧 Approach

### 1. Data Extraction & Transformation
- Loaded CSV and JSON datasets using Pandas
- Removed 35 duplicate rows
- Cleaned rating column: "4.1/5" → 4.1, "NEW" → NaN (146 entries)
- Standardized cost column: "1,000" → 1000
- Feature engineering: `pricing_segment` (Budget/Mid/Premium), `rating_category` (Poor/Average/Good/Excellent)

### 2. Database Layer (SQLite)
- Stored cleaned data in relational database (2 tables)
- Cursor-based SQL queries with GROUP BY, HAVING, CASE WHEN, JOIN
- Parameterized queries for security

### 3. Streamlit Application
- Pure tabular output (no visualizations) as per project requirements
- SQL-driven analytics (no hardcoding)
- Interactive filtering with dynamic query building
- Three-page structure: Dashboard, Restaurant Q&A, Order Q&A

---

## 📚 SQL Concepts Used

- `SELECT`, `FROM`, `WHERE` — Basic querying
- `GROUP BY`, `HAVING` — Grouping & filtering groups
- `ORDER BY`, `LIMIT` — Sorting & limiting
- `AVG()`, `COUNT()`, `SUM()`, `ROUND()` — Aggregate functions
- `CASE WHEN` — Conditional logic / segmentation
- `INNER JOIN` — Combining restaurant + order tables
- `SUBSTR()`, `strftime()` — String and date functions
- Parameterized queries — SQL injection prevention

---
