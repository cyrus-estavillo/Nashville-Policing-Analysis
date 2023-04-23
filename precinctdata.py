import pandas as pd

# Read the CSV file
df = pd.read_csv('cleaned_data.csv')

# Remove rows with null values in the 'precinct', 'date', or 'time' columns
df = df.dropna(subset=['precinct', 'date', 'time'])

# Convert the 'date' column to datetime format and extract the year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Group by 'precinct' and 'year', and count unique 'stop_id' values
result = df.groupby(['precinct', 'year'])['stop_id'].nunique().reset_index()

# Rename the 'stop_id' column to 'stop_count'
result = result.rename(columns={'stop_id': 'stop_count'})

# Save the result to a new CSV file
result.to_csv('precinct_stops.csv', index=False)