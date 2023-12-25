import pandas as pd

df = pd.read_excel(r'C:\Users\steve\Downloads\airbnb.xlsx')
df = df[~ df['Host Since'].isna()]

print(df['Property Type'].value_counts())