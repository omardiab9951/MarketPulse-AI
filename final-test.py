import pandas as pd
import numpy as np
import warnings

# Suppress warnings to keep the output clean
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
# We are using the 800MB file you generated previously
INPUT_FILE = 'electronics_full_cleaned.csv'
OUTPUT_FILE = 'electronics_final_analysis_results.csv'

print("--- PHASE 1: LOADING & OPTIMIZATION (STUDENT 1) ---")
df = pd.read_csv(INPUT_FILE)

# 1. Date/Time Processing (Essential for Week 3 Dashboards)
# Removing ' UTC' and converting to datetime for time-of-day analysis
df['event_time'] = pd.to_datetime(df['event_time'].str.replace(' UTC', ''), errors='coerce')
df['hour'] = df['event_time'].dt.hour
df['day_of_week'] = df['event_time'].dt.day_name()

# 2. Memory Optimization (Lead Tech Trick)
# Converting strings to 'category' makes the file smaller and Power BI faster
df['event_type'] = df['event_type'].astype('category')
df['brand'] = df['brand'].astype('category')

print(f"Successfully loaded {len(df):,} records.")

print("\n--- PHASE 2: FEATURE ENGINEERING (STUDENT 4) ---")

# 1. Price Bucketing (Market Research Task)
# We create these groups here so Power BI doesn't have to do the work later
def categorize_price(price):
    if price <= 100: return '$0-100 (Budget)'
    elif price <= 500: return '$100-500 (Mid-Range)'
    else: return '$500+ (Premium)'

df['price_group'] = df['price'].apply(categorize_price)
df['price_group'] = df['price_group'].astype('category')

print("Price groups and time features created.")

print("\n--- PHASE 3: STATISTICAL ANALYSIS (STUDENT 2 & 3) ---")

# 1. Session-Based Purchase Funnel (Fixed Logic)
# Mistake Fix: Counting rows is wrong; we must count UNIQUE SESSIONS (people)
funnel_stats = df.groupby('event_type')['user_session'].nunique()
v = funnel_stats.get('view', 0)
c = funnel_stats.get('cart', 0)
p = funnel_stats.get('purchase', 0)

print("--- Final Funnel Stats (Unique Sessions) ---")
print(f"Views: {v:,} | Carts: {c:,} | Purchases: {p:,}")

# Calculating key ratios for the final report
if v > 0 and c > 0:
    conv_rate = (p / v) * 100
    cart_abandonment = (1 - (p / c)) * 100
    print(f"Overall Conversion Rate: {conv_rate:.2f}%")
    print(f"Cart Abandonment Rate: {cart_abandonment:.2f}%")

# 2. Brand Performance (Detective Math)
brand_analysis = df.groupby(['brand', 'event_type']).size().unstack(fill_value=0)

# Mistake Fix: Handle missing columns if some brands have 0 purchases
for col in ['view', 'purchase']:
    if col not in brand_analysis.columns: brand_analysis[col] = 0

# Calculating which brands actually "close the deal"
brand_analysis['purchase_rate'] = (brand_analysis['purchase'] / brand_analysis['view'] * 100).fillna(0)
top_brands = brand_analysis[brand_analysis['view'] > 500].sort_values('purchase_rate', ascending=False).head(5)

print("\n--- Top 5 Converting Brands ---")
print(top_brands['purchase_rate'])

print("\n--- PHASE 4: EXPORT FOR POWER BI ---")
# This file now contains all the columns (hour, day, price_group) needed for the Dashboard
df.to_csv(OUTPUT_FILE, index=False)
print(f"Done! Final file saved as: {OUTPUT_FILE}")