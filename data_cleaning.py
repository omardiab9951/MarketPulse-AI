import pandas as pd
import warnings
warnings.filterwarnings('ignore')


# Load the file you extracted
df = pd.read_csv('electronics_full_cleaned.csv')

# --- STUDENT 1: DATA OPTIMIZATION ---
# 1. Convert event_time to actual datetime objects (Essential for Week 3 time analysis)
df['event_time'] = pd.to_datetime(df['event_time'].str.replace(' UTC', ''), errors='coerce')

# 2. Memory Management: Convert 'event_type' to Category type
# This makes the file size smaller and faster for Power BI
df['event_type'] = df['event_type'].astype('category')

# 3. Handle Missing Values: Fill missing brands and categories with 'Unknown'
df['brand'] = df['brand'].fillna('Unknown')
df['category_code'] = df['category_code'].fillna('Unknown')

# 4. Final Integrity Check
print("--- Data Quality Report ---")
print(f"Total Rows: {len(df)}")
print(f"Missing Category Codes: {df['category_code'].isnull().sum()}") # Should be 0 now
print(f"Missing Brands: {df['brand'].isnull().sum()}") # Should be 0 now
print(f"Price Errors (<=0): {len(df[df['price'] <= 0])}") # Should be 0 now

# Save the final "Gold Standard" version
df.to_csv('electronics_final_for_team.csv', index=False)
print("Project Data is now 'Analysis-Ready'!")