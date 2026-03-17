import pandas as pd
import numpy as np
import os

# Set up the base directory (location of this script)
base_dir = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.abspath(os.path.join(base_dir, '..', 'data', 'UnCleandSA_Aqar.csv'))
output_path = os.path.abspath(os.path.join(base_dir, '..', 'data', 'CleanedSA_Aqar.csv'))

print(f"🔍 Searching for file at: {input_path}")

# --- Data Loading Stage ---
try:
    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        print("✅ File found successfully! Starting the cleaning process...")
    else:
        raise FileNotFoundError
except FileNotFoundError:
    print(f"❌ Error: File not found. Please ensure your folder structure is:")
    print(f"Project_Folder/")
    print(f"  ├── data/UnCleandSA_Aqar.csv")
    print(f"  └── scripts/clean_data.py")
    exit()

# --- Core Cleaning Stage ---

# 1. Text Cleaning (City & District)
# Stripping whitespace and ensuring consistent string format
for col in ['city', 'district', 'front']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 2. Standardizing Boolean Features
# Ensuring features like (pool, elevator, garage) contain only 0 or 1
binary_cols = ['furnished', 'ac', 'roof', 'pool', 'frontyard', 'basement', 
               'duplex', 'stairs', 'elevator', 'fireplace', 'kitchen', 
               'garage', 'driver_room', 'maid_room']

for col in binary_cols:
    if col in df.columns:
        # Filling missing values with 0 (assuming feature is missing if not mentioned)
        df[col] = df[col].fillna(0).astype(int)

# --- Data Engineering & Logic Stage ---

# 3. Handling Outliers (Price & Size)
# Filtering out unrealistic prices (e.g., less than 50k or more than 100M SAR)
df = df[(df['price'] >= 50000) & (df['price'] <= 100000000)]

# Filtering out extreme sizes (e.g., less than 20m² or more than 10,000m²)
df = df[(df['size'] >= 20) & (df['size'] <= 10000)]

# 4. Feature Engineering
# Adding 'Price per Meter': A crucial metric for investors
df['price_per_meter'] = (df['price'] / df['size']).round(2)

# Categorizing Property Age for better filtering in the dashboard
def categorize_age(age):
    if age == 0: return 'New'
    elif age <= 5: return 'Modern'
    elif age <= 15: return 'Medium'
    else: return 'Old'

df['age_category'] = df['property_age'].apply(categorize_age)

# 5. Handling Missing Values in Numeric Columns
# Replacing NaN in room counts with the mode (most frequent value)
cols_to_fix = ['bedrooms', 'bathrooms', 'livingrooms']
for col in cols_to_fix:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0]).astype(int)

# --- Final Export Stage ---

# 6. Saving the Cleaned Dataset
df.to_csv(output_path, index=False, encoding='utf-8')

print("---")
print("✅ Data Cleaning Completed Successfully!")
print(f"📊 Total records before cleaning: {len(pd.read_csv(input_path))}")
print(f"📊 Total records after cleaning:  {len(df)}")
print(f"📈 New feature 'price_per_meter' created.")
print(f"📂 Cleaned file saved to: {output_path}")