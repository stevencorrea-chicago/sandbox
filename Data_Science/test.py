import pandas as pd

columns = ['Host Id', 'Host Since', 'Name', 'Neighbourhood', 'Property Type',
       'Review Scores Rating (bin)', 'Room Type', 'Zipcode', 'Beds',
       'Number of Records', 'Number Of Reviews', 'Price',
       'Review Scores Rating']

df = pd.read_excel(r'C:\Users\steve\Downloads\airbnb.xlsx')
df = df[~ df['Host Since'].isna()]
df.columns = columns

print(df.columns)

#print(df['Property Type'].value_counts())

#print(df['Host Since'].sort_values().head(1))

#print(df['Host Since'].sort_values().tail(1))

mask = df['Neighbourhood'] == 'Queens'
df[mask]['Zipcode'].to_csv('output.csv', index=False)

