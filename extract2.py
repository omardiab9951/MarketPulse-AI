import pandas as pd

# 1. Load your filtered electronics file
print("Loading the data...")
df = pd.read_csv('electronics_only_feb.csv')

# 2. Fill missing brands with 'Unknown'
df['brand'] = df['brand'].fillna('Unknown')

# 3. Remove items with $0 price
df = df[df['price'] > 0]

# 4. THE COMPROMISE: Take a random sample of 600,000 rows
print("Sampling the data to fit in Excel...")
# random_state=42 ensures that if you run this twice, you get the same random rows
df_sampled = df.sample(n=600000, random_state=42) 

# 5. Save this perfect, Excel-sized file
df_sampled.to_csv('cleaned_electronics_sampled.csv', index=False)

print("Done! You can now safely open 'cleaned_electronics_sampled.csv' in Excel.")