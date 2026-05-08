# 🛒 MarketPulse AI: eCommerce Behavior Analytics
**Data-Driven Consumer Insights for Electronics Retail**

MarketPulse AI is a professional data engineering and analytics project that transforms raw eCommerce event logs into actionable business intelligence. By analyzing millions of user interactions, we identify patterns in cart abandonment, price sensitivity, and brand loyalty.

---

## 👥 The Team
* **Omar Diab** 
* **Pavllly Sameh** 
* **Khaled Rady** 
* **Anwar Nasr** 
* **Ahmed Zezo** 

---

## 📂 Data & Methodology
The analysis focuses on the Electronics category (February 2020), processing a high-volume dataset that exceeds standard RAM limitations.

* **📥 [Download Cleaned Dataset (800MB CSV)](https://www.mediafire.com/file/k8kc5pdt8nxi1zd/electronics_full_cleaned.csv/file)**
* **Processing:** Handled 20M+ records using Python-based chunking and categorical encoding.

---

## ⚙️ Technical Pipeline
Our unified Python pipeline handles the end-to-end flow from raw data to dashboard-ready CSV:

1. **Extraction & Cleaning:** Filters the 2.2GB raw source, handles missing brand data, and removes pricing anomalies.
2. **Feature Engineering:** Extracts temporal features (Hourly/Weekly trends) and segments products into Price Buckets ($0-100, $100-500, $500+).
3. **Behavioral Analysis:** Implements session-based funnel tracking to accurately measure Conversion and Cart Abandonment rates.

---

## 📊 Business Insights
* **The "Checkout Barrier":** Identified the primary drop-off point between carting and purchasing for high-ticket items.
* **Temporal Patterns:** Discovered peak purchasing windows (8 PM – 11 PM), suggesting optimal timing for marketing push notifications.
* **Brand Strategy:** Classified brands into "Window Shopping" vs. "Closers" based on purchase-per-view ratios.

---

## 🛠️ Tech Stack
- **Python 3.8+** (Pandas, NumPy)
- **Power BI Desktop** (Interactive Dashboards)
- **Jupyter Notebooks** (Exploratory Data Analysis)
