import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
INPUT_FILE  = 'electronics_full_cleaned.csv'

print("=" * 60)
print("   MARKETPULSE AI — ELECTRONICS CART ABANDONMENT ANALYSIS")
print("=" * 60)

# ==============================================================
# PHASE 1: LOADING & OPTIMIZATION (STUDENT 1)
# ==============================================================
print("\n--- PHASE 1: LOADING & OPTIMIZATION (STUDENT 1) ---")

df = pd.read_csv(INPUT_FILE)

# Date/Time Processing
df['event_time'] = pd.to_datetime(
    df['event_time'].str.replace(' UTC', ''), errors='coerce'
)
df['hour']        = df['event_time'].dt.hour
df['day_of_week'] = df['event_time'].dt.day_name()

# Memory Optimization
df['event_type'] = df['event_type'].astype('category')
df['brand']      = df['brand'].astype('category')

print(f"Successfully loaded {len(df):,} records.")

# ==============================================================
# PHASE 1.5: DATA UNDERSTANDING (STUDENT 2 — STEP 3)
# ==============================================================
print("\n--- PHASE 1.5: DATA UNDERSTANDING (STUDENT 2 — STEP 3) ---")

print("\n[1] Dataset Shape:")
print(f"    Rows: {df.shape[0]:,}  |  Columns: {df.shape[1]}")

print("\n[2] Column Data Types:")
print(df.dtypes)

print("\n[3] Missing Values Per Column:")
missing = df.isnull().sum()
print(missing)

print("\n[4] Price Column — Descriptive Statistics:")
print(df['price'].describe())

print("\n[5] Unique Event Types & Counts:")
print(df['event_type'].value_counts())

# ==============================================================
# PHASE 2: FEATURE ENGINEERING (STUDENT 4)
# ==============================================================
print("\n--- PHASE 2: FEATURE ENGINEERING (STUDENT 4) ---")

# Price Bucketing
def categorize_price(price):
    if price <= 100:
        return '$0-100 (Budget)'
    elif price <= 500:
        return '$100-500 (Mid-Range)'
    else:
        return '$500+ (Premium)'

df['price_group'] = df['price'].apply(categorize_price).astype('category')

# Abandoned Cart Flag
# Logic: a session is "abandoned" if it reached cart but never purchased
cart_sessions     = set(df[df['event_type'] == 'cart']['user_session'])
purchase_sessions = set(df[df['event_type'] == 'purchase']['user_session'])
abandoned_sessions = cart_sessions - purchase_sessions

df['is_abandoned'] = df['user_session'].isin(abandoned_sessions)

print("Price groups, abandoned-cart flag, and time features created.")
print(f"Total abandoned cart sessions: {len(abandoned_sessions):,}")

# ==============================================================
# PHASE 3: STATISTICAL ANALYSIS (STUDENT 2 & 3)
# ==============================================================
print("\n--- PHASE 3: STATISTICAL ANALYSIS (STUDENT 2 & 3) ---")

# ------ Purchase Funnel ----------------------------------------
funnel_stats = df.groupby('event_type')['user_session'].nunique()
v = funnel_stats.get('view',     0)
c = funnel_stats.get('cart',     0)
p = funnel_stats.get('purchase', 0)

print("\n--- Final Funnel Stats (Unique Sessions) ---")
print(f"    Views     : {v:,}")
print(f"    Carts     : {c:,}")
print(f"    Purchases : {p:,}")

conv_rate         = (p / v * 100) if v > 0 else 0
cart_abandonment  = ((c - p) / c * 100) if c > 0 else 0

print(f"\n    Overall Conversion Rate  : {conv_rate:.2f}%")
print(f"    Cart Abandonment Rate    : {cart_abandonment:.2f}%")

# ------ Brand Performance --------------------------------------
brand_analysis = (
    df.groupby(['brand', 'event_type'])
      .size()
      .unstack(fill_value=0)
)

for col in ['view', 'cart', 'purchase']:
    if col not in brand_analysis.columns:
        brand_analysis[col] = 0

brand_analysis['purchase_rate'] = (
    brand_analysis['purchase'] / brand_analysis['view'] * 100
).fillna(0)

top_brands = (
    brand_analysis[brand_analysis['view'] > 500]
    .sort_values('purchase_rate', ascending=False)
    .head(5)
)

print("\n--- Top 5 Converting Brands ---")
print(top_brands['purchase_rate'])

best_brand      = top_brands['purchase_rate'].idxmax()
best_brand_rate = top_brands['purchase_rate'].max()

# ==============================================================
# PHASE 3.5: KPI SUMMARY (STEP 4)
# ==============================================================
print("\n--- PHASE 3.5: KPI SUMMARY (STEP 4) ---")

# KPI 4 — Peak Abandonment Hour
hourly_carts     = df[df['event_type'] == 'cart'].groupby('hour')['user_session'].nunique()
hourly_purchases = df[df['event_type'] == 'purchase'].groupby('hour')['user_session'].nunique()

hourly_abandonment = (
    (hourly_carts - hourly_purchases.reindex(hourly_carts.index, fill_value=0))
    / hourly_carts * 100
).fillna(0)

peak_abandon_hour = hourly_abandonment.idxmax()
peak_abandon_rate = hourly_abandonment.max()

# KPI 5 — Premium Price Abandonment
premium_df        = df[df['price_group'] == '$500+ (Premium)']
premium_carts     = premium_df[premium_df['event_type'] == 'cart']['user_session'].nunique()
premium_purchases = premium_df[premium_df['event_type'] == 'purchase']['user_session'].nunique()
premium_abandonment = (
    ((premium_carts - premium_purchases) / premium_carts * 100)
    if premium_carts > 0 else 0
)

print("\n" + "=" * 50)
print(f"  KPI 1 — Overall Conversion Rate    : {conv_rate:.2f}%")
print(f"  KPI 2 — Cart Abandonment Rate      : {cart_abandonment:.2f}%")
print(f"  KPI 3 — Best Brand Purchase Rate   : {best_brand} at {best_brand_rate:.2f}%")
print(f"  KPI 4 — Peak Abandonment Hour      : {peak_abandon_hour}:00  ({peak_abandon_rate:.2f}% abandoned)")
print(f"  KPI 5 — Premium Item Abandonment   : {premium_abandonment:.2f}%")
print("=" * 50)

# ==============================================================
# PHASE 4: HYPOTHESIS TESTING (STEP 5)
# ==============================================================
print("\n--- PHASE 4: HYPOTHESIS TESTING (STEP 5) ---")

# ------ H1: Higher price → higher abandonment -----------------
print("\n[H1] Do $500+ items have higher cart abandonment than budget items?")

price_group_analysis = (
    df.groupby(['price_group', 'event_type'])['user_session']
      .nunique()
      .unstack(fill_value=0)
)
for col in ['cart', 'purchase']:
    if col not in price_group_analysis.columns:
        price_group_analysis[col] = 0

price_group_analysis['abandonment_rate'] = (
    (price_group_analysis['cart'] - price_group_analysis['purchase'])
    / price_group_analysis['cart'] * 100
).fillna(0)

print(price_group_analysis[['cart', 'purchase', 'abandonment_rate']])

budget_rate  = price_group_analysis['abandonment_rate'].get('$0-100 (Budget)',  0)
premium_rate = price_group_analysis['abandonment_rate'].get('$500+ (Premium)', 0)

if premium_rate > budget_rate:
    print(f"\n  H1 RESULT → ACCEPTED")
    print(f"  Premium abandonment ({premium_rate:.1f}%) > Budget abandonment ({budget_rate:.1f}%)")
    print("  Evidence supports that price is a barrier to purchase.")
else:
    print(f"\n  H1 RESULT → REJECTED")
    print(f"  Premium ({premium_rate:.1f}%) is NOT higher than Budget ({budget_rate:.1f}%).")

# ------ H2: Abandonment peaks at night (after 9 PM) -----------
print("\n[H2] Is cart abandonment higher after 9 PM than during the day?")

print("\n  Abandonment Rate by Hour:")
print(hourly_abandonment.sort_index().to_string())

night_avg = hourly_abandonment[hourly_abandonment.index >= 21].mean()
day_avg   = hourly_abandonment[hourly_abandonment.index  < 21].mean()

if night_avg > day_avg:
    print(f"\n  H2 RESULT → ACCEPTED")
    print(f"  Night avg ({night_avg:.1f}%) > Day avg ({day_avg:.1f}%)")
    print("  Evidence supports that late-night sessions abandon more carts.")
else:
    print(f"\n  H2 RESULT → REJECTED")
    print(f"  Night avg ({night_avg:.1f}%) is NOT higher than Day avg ({day_avg:.1f}%).")

# ------ H3: Some brands convert significantly better ----------
print("\n[H3] Do certain brands convert significantly better than others?")

print("\n  Top 5 Brand Purchase Rates:")
print(top_brands['purchase_rate'].to_string())

rate_range = top_brands['purchase_rate'].max() - top_brands['purchase_rate'].min()

if rate_range > 5:
    print(f"\n  H3 RESULT → ACCEPTED")
    print(f"  Purchase rates vary by {rate_range:.1f}% across top brands.")
    print("  Brand trust significantly affects conversion.")
else:
    print(f"\n  H3 RESULT → REJECTED")
    print(f"  Brand purchase rates are similar (only {rate_range:.1f}% difference).")

# ==============================================================
# PHASE 5: EXPLORATORY DATA ANALYSIS — EDA (STEP 6)
# ==============================================================
print("\n--- PHASE 5: EXPLORATORY DATA ANALYSIS (STEP 6) ---")

# ------ Abandonment by Hour ------------------------------------
print("\n[1] Abandonment Rate by Hour of Day:")
hourly_df = pd.DataFrame({
    'hour'             : hourly_abandonment.index,
    'abandonment_rate' : hourly_abandonment.values,
    'cart_sessions'    : hourly_carts.reindex(hourly_abandonment.index, fill_value=0).values,
    'purchase_sessions': hourly_purchases.reindex(hourly_abandonment.index, fill_value=0).values,
})
print(hourly_df.to_string(index=False))

# ------ Abandonment by Day of Week ----------------------------
print("\n[2] Abandonment Rate by Day of Week:")
day_carts     = df[df['event_type'] == 'cart'].groupby('day_of_week')['user_session'].nunique()
day_purchases = df[df['event_type'] == 'purchase'].groupby('day_of_week')['user_session'].nunique()

day_abandonment = (
    (day_carts - day_purchases.reindex(day_carts.index, fill_value=0))
    / day_carts * 100
).fillna(0).sort_values(ascending=False)

print(day_abandonment.to_string())

# ------ Abandonment by Price Group ----------------------------
print("\n[3] Abandonment Rate by Price Group:")
print(price_group_analysis[['cart', 'purchase', 'abandonment_rate']].to_string())

# ------ Top 10 Most Abandoned Products ------------------------
print("\n[4] Top 10 Most Viewed Products That Were Never Purchased:")
abandoned_views = df[
    (df['event_type'] == 'view') & (df['is_abandoned'])
]
top_abandoned_products = (
    abandoned_views.groupby('product_id')['user_session']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)
print(top_abandoned_products.to_string())

# ==============================================================
# PHASE 6: ROOT CAUSE ANALYSIS (STEP 7)
# ==============================================================
print("\n--- PHASE 6: ROOT CAUSE ANALYSIS (STEP 7) ---")

worst_day  = day_abandonment.idxmax()
worst_day_rate = day_abandonment.max()

print(f"""
ROOT CAUSE SUMMARY
{"=" * 56}
Overall cart abandonment rate: {cart_abandonment:.1f}%
This means only {100 - cart_abandonment:.1f}% of users who add an item to their
cart actually complete the purchase.

CAUSE 1 — Price Sensitivity (H1: {"Accepted" if premium_rate > budget_rate else "Rejected"})
  Premium items ($500+) have a {premium_rate:.1f}% abandonment rate
  versus {budget_rate:.1f}% for budget items. Customers hesitate before
  committing to high-value electronics purchases.

CAUSE 2 — Decision Fatigue at Night (H2: {"Accepted" if night_avg > day_avg else "Rejected"})
  Abandonment peaks at {peak_abandon_hour}:00 with {peak_abandon_rate:.1f}% rate.
  Night browsing (after 9 PM) averages {night_avg:.1f}% abandonment
  vs {day_avg:.1f}% during the day. Users browse late but defer decisions.

CAUSE 3 — Brand Trust Gap (H3: {"Accepted" if rate_range > 5 else "Rejected"})
  Top brand '{best_brand}' converts at {best_brand_rate:.1f}%, while
  weaker brands convert far less. A {rate_range:.1f}% gap in purchase
  rates shows brand recognition drives purchase confidence.

CAUSE 4 — Day of Week Effect
  Worst abandonment day: {worst_day} ({worst_day_rate:.1f}%).
  This may reflect weekend browsing without purchase intent.

CONCLUSION:
  The high abandonment rate is caused by three compounding
  factors: price sensitivity in the premium segment, decision
  fatigue during late-night sessions, and insufficient brand
  trust for lesser-known electronics brands.
{"=" * 56}
""")

# ==============================================================
# PHASE 7: EXPORT FOR POWER BI (STEP 9)
# ==============================================================
print("\n--- PHASE 7: EXPORT FOR POWER BI (STEP 9) ---")

# 1. Main enriched dataset
df.to_csv('electronics_final_analysis_results.csv', index=False)
print("  Saved: electronics_final_analysis_results.csv")

# 2. Hourly abandonment summary
hourly_df.to_csv('summary_hourly_abandonment.csv', index=False)
print("  Saved: summary_hourly_abandonment.csv")

# 3. Day of week abandonment summary
day_abandonment_df = pd.DataFrame({
    'day_of_week'     : day_abandonment.index,
    'abandonment_rate': day_abandonment.values,
    'cart_sessions'   : day_carts.reindex(day_abandonment.index, fill_value=0).values,
    'purchase_sessions': day_purchases.reindex(day_abandonment.index, fill_value=0).values,
})
day_abandonment_df.to_csv('summary_day_abandonment.csv', index=False)
print("  Saved: summary_day_abandonment.csv")

# 4. Price group abandonment summary
price_group_analysis.reset_index().to_csv('summary_price_group_abandonment.csv', index=False)
print("  Saved: summary_price_group_abandonment.csv")

# 5. Brand performance summary
brand_summary = brand_analysis[brand_analysis['view'] > 500].reset_index()
brand_summary.to_csv('summary_brand_performance.csv', index=False)
print("  Saved: summary_brand_performance.csv")

# 6. KPI summary table (for Power BI KPI cards)
kpi_df = pd.DataFrame([
    {'KPI': 'Overall Conversion Rate',  'Value': round(conv_rate, 2),          'Unit': '%'},
    {'KPI': 'Cart Abandonment Rate',    'Value': round(cart_abandonment, 2),    'Unit': '%'},
    {'KPI': 'Best Brand Purchase Rate', 'Value': round(best_brand_rate, 2),     'Unit': '%'},
    {'KPI': 'Peak Abandonment Hour',    'Value': int(peak_abandon_hour),        'Unit': 'hour'},
    {'KPI': 'Premium Item Abandonment', 'Value': round(premium_abandonment, 2), 'Unit': '%'},
])
kpi_df.to_csv('summary_kpis.csv', index=False)
print("  Saved: summary_kpis.csv")

print(f"""
{"=" * 60}
  ALL DONE. Load these files into Power BI:
    1. electronics_final_analysis_results.csv  (main data)
    2. summary_kpis.csv                        (KPI cards)
    3. summary_hourly_abandonment.csv          (line chart)
    4. summary_day_abandonment.csv             (bar chart)
    5. summary_price_group_abandonment.csv     (bar chart)
    6. summary_brand_performance.csv           (bar chart)
{"=" * 60}
""")
