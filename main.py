import pandas as pd
from pathlib import Path

# Set up paths
data_folder = Path("data")
output_file = "formatted_output.csv"

# Read all CSV files from the data folder
csv_files = list(data_folder.glob("*.csv"))
print(f"Found {len(csv_files)} CSV files in the data folder")

# Read and combine all CSV files
dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    
    # Clean the price column if needed
    if df['price'].dtype == 'object':
        df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.split('$').str[0]
    
    # Convert to numeric
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Standardize product names (lowercase)
    df['product'] = df['product'].str.lower().str.strip()
    
    dataframes.append(df)
    print(f"Loaded {file.name}: {len(df)} rows")

# Combine all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)
print(f"\nTotal rows combined: {len(combined_df)}")

# Filter for Pink Morsel only
pink_morsel_df = combined_df[combined_df['product'] == 'pink morsel'].copy()
print(f"Pink Morsel rows: {len(pink_morsel_df)}")

# Calculate sales (price × quantity)
pink_morsel_df['sales'] = pink_morsel_df['price'] * pink_morsel_df['quantity']

# Select only the required columns: sales, date, region
output_df = pink_morsel_df[['sales', 'date', 'region']].copy()

# Rename columns to match exact specification
output_df.columns = ['sales', 'date', 'region']

# Sort by date for better organization
output_df = output_df.sort_values('date').reset_index(drop=True)

# Display sample of the output
print("\n" + "="*60)
print("OUTPUT PREVIEW (first 10 rows)")
print("="*60)
print(output_df.head(10))

print("\n" + "="*60)
print("OUTPUT STATISTICS")
print("="*60)
print(f"Total rows in output: {len(output_df)}")
print(f"Date range: {output_df['date'].min()} to {output_df['date'].max()}")
print(f"Regions: {output_df['region'].unique()}")
print(f"Total sales: ${output_df['sales'].sum():,.2f}")

# Save to CSV
output_df.to_csv(output_file, index=False)
print("\n" + "="*60)
print(f"✅ Output saved to: {output_file}")
print("="*60)

# Re-read the file to confirm it was saved correctly
verification_df = pd.read_csv(output_file)
print(f"\nVerification: File contains {len(verification_df)} rows and {len(verification_df.columns)} columns")
print(f"Columns: {list(verification_df.columns)}")
