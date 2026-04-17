import pandas as pd

# Load all three CSV files
df = pd.concat([
    pd.read_csv('data/daily_sales_data_0.csv'),
    pd.read_csv('data/daily_sales_data_1.csv'),
    pd.read_csv('data/daily_sales_data_2.csv')
])

# Keep only Pink Morsels
df = df[df['product'] == 'pink morsel']

# Calculate sales (remove $ from price first)
df['price'] = df['price'].str.replace('$', '').astype(float)
df['sales'] = df['price'] * df['quantity']

# Keep only the required columns
df = df[['sales', 'date', 'region']]

# Save to output file
df.to_csv('output.csv', index=False)

print("Done! output.csv created.")
