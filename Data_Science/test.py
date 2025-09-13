import pandas as pd
from pathlib import Path

columns = ['Host Id', 'Host Since', 'Name', 'Neighbourhood', 'Property Type',
       'Review Scores Rating (bin)', 'Room Type', 'Zipcode', 'Beds',
       'Number of Records', 'Number Of Reviews', 'Price',
       'Review Scores Rating']

script_path = Path(__file__).resolve()
parent_dir = script_path.parent

print(script_path)
print(parent_dir)

# Recommended way: use `/` to join paths
file_path = parent_dir.parent/ "mock_airbnb_data_500.xlsx"

df = pd.read_excel(file_path)

print(df.columns)

