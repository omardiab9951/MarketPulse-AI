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