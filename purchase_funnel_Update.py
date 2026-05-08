
# ─────────────────────────────────────────────
#extractfinal.py Student 1 (Lead Technician):
# ─────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────────────────

import pandas as pd

input_file = '2020-Feb.csv.gz'
output_file = 'electronics_full_cleaned.csv'
chunk_size = 100000  # Process 100k rows at a time to save RAM

print("Starting memory-safe extraction...")

# Initialize an empty list to store the pieces
electronics_chunks = []

# Read the file in chunks
for chunk in pd.read_csv(input_file, compression='gzip', chunksize=chunk_size, low_memory=False):
    # 1. Keep only electronics (Scoping)
    filtered_chunk = chunk[chunk['category_code'].str.startswith('electronics', na=False)].copy()
    
    if not filtered_chunk.empty:
        # 2. Clean Brands (Student 2 Task)
        filtered_chunk['brand'] = filtered_chunk['brand'].fillna('Unknown')
        
        # 3. Quality Control (Price > 0)
        filtered_chunk = filtered_chunk[filtered_chunk['price'] > 0]
        
        electronics_chunks.append(filtered_chunk)

# Combine all small pieces into one final table
print("Combining all electronics data...")
df_final = pd.concat(electronics_chunks)

# Save the final file for Power BI
df_final.to_csv(output_file, index=False)
print(f"Success! Created {output_file} with {len(df_final)} rows.")
# ──────────────────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────
#data_cleaning.py Student 2 (Data Cleaner):
# ─────────────────────────────────────────────

# Load the file you extracted
df = pd.read_csv('electronics_full_cleaned.csv')

# --- STUDENT 1: DATA OPTIMIZATION ---
# 1. Convert event_time to actual datetime objects (Essential for Week 3 time analysis)
df['event_time'] = pd.to_datetime(df['event_time'].str.replace(' UTC', ''), errors='coerce')

# 2. Memory Management: Convert 'event_type' to Category type
# This makes the file size smaller and faster for Power BI
df['event_type'] = df['event_type'].astype('category')

# 3. Final Integrity Check
print("--- Data Quality Report ---")
print(f"Total Rows: {len(df)}")
print(f"Missing Brands: {df['brand'].isnull().sum()}") # Should be 0 now
print(f"Price Errors (<=0): {len(df[df['price'] <= 0])}") # Should be 0 now

# Save the final "Gold Standard" version
df.to_csv('electronics_final_for_team.csv', index=False)
print("Project Data is now 'Analysis-Ready'!")

# ──────────────────────────────────────────────────────────────────────────────────────────

#purchase_funnel.py Student 3 (Conversion Analyst):
# ─────────────────────────────────────────────
# Purchase Funnel Analysis  
# ─────────────────────────────────────────────


# ── Step 1: Load the data ────────────────────
df = pd.read_csv("C:\\Users\\nnasr\\OneDrive\\Desktop\\New folder (5)\\electronics_full_cleaned.csv")

# Quick look at what we have
print("Shape:", df.shape)
print(df[["event_type", "user_session"]].head())

# ── Step 2: Count unique sessions per stage ──
# A session "counts" for a stage if it had
# at least one event of that type.

views = df[df["event_type"] == "view"]["user_session"].nunique()
carts = df[df["event_type"] == "cart"]["user_session"].nunique()
purchases = df[df["event_type"] == "purchase"]["user_session"].nunique()

# ── Step 3: Print the funnel ─────────────────
print("\n===== Purchase Funnel =====")
print(f"  Views    : {views:,} sessions")
print(f" Carts    : {carts:,} sessions")
print(f" Purchases: {purchases:,} sessions")

# ── Step 4: Calculate conversion rate ────────
# Conversion Rate = Purchases ÷ Views × 100
if views > 0:
    conversion_rate = (purchases / views) * 100
    print(f"\n Overall Conversion Rate: {conversion_rate:.2f}%")

# ── Step 5: Find the biggest drop-off ────────
# Drop-off = how many people left between stages
view_to_cart_drop  = views - carts
cart_to_buy_drop   = carts - purchases

print("\n===== Drop-off Analysis =====")
print(f"View → Cart drop-off   : {view_to_cart_drop:,} people left")
print(f"Cart → Purchase drop-off: {cart_to_buy_drop:,} people left")

if view_to_cart_drop > cart_to_buy_drop:
    print("\n Biggest problem: View → Cart")
    print("   People see products but don't add them to cart.")
    print("   Possible cause: product interest / pricing issue.")
else:
    print("\n Biggest problem: Cart → Purchase")
    print("   People add to cart but don't complete checkout.")
    print("   Possible cause: checkout friction / payment issue.")

# ──────────────────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────

#Price & Brand Specialist Student 4 (Price & Brand Specialist): 
# ─────────────────────────────────────────────