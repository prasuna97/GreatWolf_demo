import pandas as pd
from sqlalchemy import create_engine

# Define the folder path for data files
folder_path = 'GW_DataEngineer'

# Create SQLite engine
engine = create_engine('sqlite:///hotel_data.db')

# Load CSV data into DataFrames using the folder path
property_df = pd.read_csv(f'{folder_path}/dim_property.csv')
inventory_df = pd.read_csv(f'{folder_path}/property_inventory.csv')
reservations_df = pd.read_csv(f'{folder_path}/reservations.csv')
revenue_center_df = pd.read_csv(f'{folder_path}/dim_revenue_center.csv')
ancillary_df = pd.read_csv(f'{folder_path}/ancillary.csv')

# Load DataFrames into SQL tables
property_df.to_sql('dim_property', engine, if_exists='replace', index=False)
inventory_df.to_sql('property_inventory', engine, if_exists='replace', index=False)
reservations_df.to_sql('reservations', engine, if_exists='replace', index=False)
revenue_center_df.to_sql('dim_revenue_center', engine, if_exists='replace', index=False)
ancillary_df.to_sql('ancillary_data', engine, if_exists='replace', index=False)
