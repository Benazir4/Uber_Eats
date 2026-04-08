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
- **Cuisine Performance Analysis** — Uncover high-performing and niche cuisines (both combined and individual)
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
| Database | SQLite (3 tables) |
| Web Application | Streamlit (4 pages) |
| IDE | Visual Studio Code |

---

## 📁 Project Structure

```
uber_eats_project/
│
├── data/
│   ├── raw/                              # Original untouched data files
│   │   ├── Uber_Eats_data.csv               # Restaurant dataset (23,193 raw rows)
│   │   └── orders.json                      # Order dataset (25,000 records)
│   └── cleaned/                          # Cleaned & preprocessed data
│       ├── cleaned_restaurant_data.csv      # Cleaned restaurant data (4,531 unique rows)
│       └── cleaned_orders_data.csv          # Cleaned order data (25,000 rows)
│
├── database/
│   └── uber_eats.db                         # 3 tables: restaurants, orders, cuisine_split
│
├── scripts/
│   ├── step1_data_cleaning.py               # Data cleaning & preprocessing (8 steps)
│   └── step2_database_setup.py              # Database creation & 30 SQL queries
│
├── app/
│   └── streamlit_app.py                     # 4-page interactive dashboard
│
├── Application_Flowchart.png             # Project architecture diagram
├── requirements.txt                      # Python dependencies
├── .gitignore                            # Git ignore rules
└── README.md                             # This file
```

---

## 🔄 Application Flowchart

![Application Flowchart](Application_Flowchart.png)

**Flow:** Raw CSV/JSON → Python cleaning (23,193 → 4,531) → SQLite (3 tables) → 4-page Streamlit app (30 queries) → Business decisions

---

## 📊 Datasets

### 1. Restaurant Data (CSV) — 23,193 raw rows (cleaned to 4,531 unique)
| Column | Description |
|--------|-------------|
| restaurant_name | Name of the restaurant |
| location | Bangalore area (88 unique) |
| cuisines | Cuisine types (combined from all listing entries) |
| rating | Customer rating (1.8 - 4.9) |
| votes | Number of customer votes |
| approx_cost_for_two | Cost for two people (₹) |
| online_order | Online ordering (Yes/No) |
| book_table | Table booking (Yes/No) |
| pricing_segment | Budget / Mid / Premium (engineered) |
| rating_category | Poor / Average / Good / Excellent (engineered) |

### 2. Order Data (JSON) — 25,000 records
| Column | Description |
|--------|-------------|
| order_id | Unique order identifier |
| restaurant_name | Restaurant that received the order |
| order_date | Date of the order (Apr 2025 – Feb 2026) |
| order_value | Order amount in ₹ |
| discount_used | Discount applied (Yes/No) |
| payment_method | Card / Cash / UPI |

### 3. Cuisine Split Table (generated) — 12,606 rows, 98 unique cuisines
Created by splitting combined cuisines (e.g., "North Indian, Chinese, Thai" → 3 separate rows) for granular individual cuisine analysis.

---

## 🚀 Setup & Installation

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/uber-eats-bangalore-intelligence.git
cd uber-eats-bangalore-intelligence

# Virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install
pip install -r requirements.txt

# Run pipeline
python scripts/step1_data_cleaning.py
python scripts/step2_database_setup.py
streamlit run app/streamlit_app.py
```

---

## 📱 Application Pages (4 Pages, 30 Queries)

| Page | Queries | Description |
|------|---------|-------------|
| 🏠 Dashboard | Dynamic | 6 interactive filters with parameterized SQL |
| ❓ Restaurant Q&A | 15 | Location, pricing, cuisine, features, top performers |
| 📦 Order Q&A | 10 | Revenue, trends, discounts, day-of-week, JOIN queries |
| 🍽️ Individual Cuisine Q&A | 5 | Top cuisines, niche opportunities, cuisine × pricing/online |

---

## 📈 Key Findings

| Insight | Finding |
|---------|---------|
| Table booking impact | 4.15 vs 3.78 — **+0.37 uplift** (strongest correlation) |
| Best pricing segment | Premium: **4.03** > Budget: 3.84 > Mid: 3.75 |
| Best locations | **Lavelle Road (4.14)**, Koramangala 5th Block (4.11) |
| Most saturated | **Indiranagar (307)**, Whitefield (295), HSR (271) |
| Problem areas | **Kaggadasapura (3.59)**, Kumaraswamy Layout (3.63), Banaswadi (3.65) |
| Feature combo | Booking Only (**4.18**) > Both (4.12) > Online Only (3.79) |
| Discount effect | ₹1,150 vs ₹822 — **+39.8% larger orders** |
| Payment split | Card/Cash/UPI — **equally distributed (~33% each)** |
| Top individual cuisine | **Modern Indian (4.30)**, Mediterranean (4.28), European (4.28) |
| Niche opportunities | **Malaysian (4.31)**, Japanese (4.27), Korean (4.25) |

---

## 🔧 Approach

### 1. Data Cleaning (8 Steps)
- Removed 35 exact duplicates + 18,627 logical duplicates (same restaurant under multiple listing categories)
- Cuisines combined using `set()` to preserve ALL unique values across entries
- Cleaned ratings: "4.1/5" → 4.1, "NEW" → NaN (23 entries)
- Cleaned costs: "1,000" → 1000, missing filled with median
- Feature engineering: `pricing_segment`, `rating_category` via `pd.cut()`

### 2. Database (SQLite, 3 Tables)
- `restaurants` (4,531 rows) + `orders` (25,000 rows) + `cuisine_split` (12,606 rows)
- 30 SQL queries using GROUP BY, HAVING, CASE WHEN, INNER JOIN, SUBSTR, strftime

### 3. Streamlit App (4 Pages)
- Pure tabular output, SQL-driven, parameterized queries, 30 business questions

---

## 📚 SQL Concepts Used

GROUP BY + HAVING, CASE WHEN, INNER JOIN, AVG/COUNT/SUM/MIN/MAX/ROUND, COUNT(DISTINCT), SUBSTR, strftime, Parameterized queries (?), String split + explode

---

## 👤 Author

**Benazir** — B.E. Computer Science | MBA Project Management | Data Science
