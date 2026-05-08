
# 🛒 MarketPulse AI: eCommerce Behavior Analysis
**Industrial Safety & Consumer Analytics Project**

MarketPulse AI is a data-driven investigation into consumer behavior within the Electronics sector. This project analyzes a large-scale dataset to identify patterns in cart abandonment, price sensitivity, and brand performance to provide actionable business recommendations.

---

## 📂 Dataset Information
Due to the large scale of the processed data (2M+ records), the "Gold Standard" cleaned dataset is hosted externally.

* **Dataset Name:** `electronics_full_cleaned.csv`
* **Focus:** Electronics Category (February 2020)
* **Download Link:** [Download Dataset via Mediafire](https://www.mediafire.com/file/k8kc5pdt8nxi1zd/electronics_full_cleaned.csv/file)

---

## 👥 Project Team
* **Omar Diab (Student 1):** Lead Technician – Data Extraction, Cleaning, & Optimization.
* **Ahmed Baher:** Conversion Analyst.
* **Shaza Alaa:** Market Research Specialist.
* **Haneen Ahmed:** Dashboard Designer & Reporting.

---

## 🛠️ Technical Pipeline (Student 1)

### 1. Data Extraction (`extractfinal.py`)
Processes the raw 2.2GB `.csv.gz` file using a **Memory-Safe Chunking Algorithm**. 
- Filters 20M+ rows down to the Electronics category.
- Handles initial missing values and removes price anomalies.

### 2. Optimization (`data_cleaning.ipynb`)
Prepares the data for high-speed analysis.
- **Type Casting:** Converts timestamps to datetime and optimizes event types to categorical data to reduce memory usage.
- **Validation:** Ensures 100% data integrity for brand and price columns before team hand-off.

---

## 📊 Analysis Roadmap
* **Week 1:** Data Procurement and Cleaning (Lead Technician).
* **Week 2:** Behavior Analysis (Purchase Funnels) and Market Research (Price Bucketing).
* **Week 3:** Final Dashboard construction in **Power BI** and Strategic Business Recommendations.

---

## 💻 Tech Stack
- **Python 3.8+** (Pandas, NumPy)
- **Power BI Desktop**
- **Jupyter Notebooks**

---

## 📝 Instructions for Team Members
1. Download the dataset from the link above.
2. Place the `.csv` file in the root directory of this project.
3. Open `Project-Work.pbix` to view the latest visualizations.
