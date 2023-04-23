import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

"""
# read .cvs files
df = pd.read_csv('tn_nashville_2020_04_01.csv')

# Drop the specified columns
columns_to_drop = [
    'raw_verbal_warning_issued',
    'raw_written_warning_issued',
    'raw_traffic_citation_issued',
    'raw_misd_state_citation_issued',
    'raw_suspect_ethnicity',
    'raw_driver_searched',
    'raw_passenger_searched',
    'raw_search_consent',
    'raw_search_arrest',
    'raw_search_warrant',
    'raw_search_inventory',
    'raw_search_plain_view',
    'notes'
]
df = df.drop(columns=columns_to_drop)

# Rename the 'raw_row_number' column to 'stop_id'
df.rename(columns={'raw_row_number': 'stop_id'}, inplace=True)


print('Sum of null values for columns:')
null_count = df[['stop_id', 'precinct', 'reporting_area', 'zone', 'officer_id_hash']].isnull().sum()
print(null_count)

print('Sum of non-null values for columns:')
nonnull_count = df[['stop_id', 'precinct', 'reporting_area', 'zone', 'officer_id_hash']].notnull().sum()
print(nonnull_count)

# Drop rows with 'NA' in the "precinct" and "officer_id" columns
df = df[df['precinct'] != 'NA']
df = df[df['officer_id_hash'] != 'NA']

# Drop duplicates in the "raw_row_number" column
df = df.drop_duplicates(subset='stop_id')

# Replace null values in the specified columns with 0
df[['contraband_found', 'contraband_weapons', 'contraband_drugs']] = df[['contraband_found', 'contraband_weapons', 'contraband_drugs']].fillna(0)

# Drop rows with null values in the specified columns
df.dropna(subset=['precinct', 'reporting_area', 'zone', 'officer_id_hash'], inplace=True)

# Replace non-number values with null for the specified columns
df['zone'] = pd.to_numeric(df['zone'], errors = 'coerce')
df['precinct'] = pd.to_numeric(df['precinct'], errors = 'coerce')
df['reporting_area'] = pd.to_numeric(df['reporting_area'], errors = 'coerce')

# Drop rows with null values in the specified columns
df.dropna(subset = ['zone', 'precinct', 'reporting_area'], inplace = True)

print('Sum of non-null values for columns after dropping null values:')
nonnull_count = df[['stop_id', 'precinct', 'reporting_area', 'zone', 'officer_id_hash']].notnull().sum()
print(nonnull_count)

# Replace "True" values with 1 and "False" values with 0
df.replace({True: 1, False: 0}, inplace=True)




# Save the cleaned data to a new .csv file
df.to_csv("cleaned_data.csv", index=False)
"""

df = pd.read_csv('cleaned_data.csv')
# Convert the 'date' column to a datetime object
df['date'] = pd.to_datetime(df['date'])



# DESCRIPTION AND FINDINGS | DESCRIPTION AND FINDINGS | DESCRIPTION AND FINDINGS | DESCRIPTION AND FINDINGS

# "For the year 2012, what percentage of officers committed what percentage of stops?"
"""
# Add 'StopYear' column to the DataFrame
df['StopYear'] = pd.to_datetime(df['date']).dt.year

# Filter the dataset for the year 2012
stops_2012 = df[df['StopYear'] == 2012]

# Calculate the number of stops per officer in 2012
officer_stops_2012 = stops_2012.groupby('officer_id_hash')['stop_id'].count().reset_index()

# Calculate the total number of stops and officers in 2012
total_stops_2012 = officer_stops_2012['stop_id'].sum()
total_officers_2012 = len(officer_stops_2012)

# Sort officers by the number of stops they conducted in 2012
officer_stops_2012_sorted = officer_stops_2012.sort_values('stop_id', ascending=False)

# Calculate the cumulative percentage of officers and the cumulative percentage of stops
officer_stops_2012_sorted['cumulative_officer_pct'] = np.arange(1, total_officers_2012 + 1) / total_officers_2012 * 100
officer_stops_2012_sorted['cumulative_stop_pct'] = officer_stops_2012_sorted['stop_id'].cumsum() / total_stops_2012 * 100

# Create the line chart
plt.plot(officer_stops_2012_sorted['cumulative_officer_pct'], officer_stops_2012_sorted['cumulative_stop_pct'])

# Customize the chart
plt.title("Cumulative Percentage of Officers vs. Cumulative Percentage of Stops in 2012")
plt.xlabel("Cumulative Percentage of Officers")
plt.ylabel("Cumulative Percentage of Stops")
plt.grid()

# Save the chart as a file
plt.savefig("cumulative_percentage_of_officers_vs_stops_2012.png", bbox_inches='tight')

# Show the chart
plt.show()
"""



# Percentage of stops resulting in each outcome per year
"""
# Add 'year' column to the DataFrame
df['year'] = pd.to_datetime(df['date']).dt.year

# Group by year and outcome, and count the number of stops for each group
year_outcome_counts = df.groupby(['year', 'outcome']).agg(num_stops=('stop_id', 'count')).reset_index()

# Calculate the total number of stops for each year
year_total_counts = year_outcome_counts.groupby('year').agg(total_stops=('num_stops', 'sum')).reset_index()

# Merge the two DataFrames to compute the percentage of stops for each outcome within a year
result = year_outcome_counts.merge(year_total_counts, on='year')
result['percentage'] = (result['num_stops'] / result['total_stops']) * 100

# Sort the result by year
result = result.sort_values('year')

print(result)

# Pivot the result DataFrame to create a table with years as index, outcomes as columns, and percentages as values
pivot_df = result.pivot(index='year', columns='outcome', values='percentage')

# Create the stacked bar chart
ax = pivot_df.plot(kind='bar', stacked=True)

# Customize the chart
plt.title("Percentage of Stops Resulting in Each Outcome per Year")
plt.xlabel("Year")
plt.ylabel("Percentage of Stops")
plt.legend(title="Outcome")
plt.xticks(rotation=0)

# Save the chart as a file
plt.savefig("percentage_of_stops_by_outcome_per_year.png", bbox_inches='tight')

# Show the chart
plt.show()
"""


# Code for top_3_precincts_by_percentage_of_total_stops_per_year
"""
# Create the PoliceOfficer DataFrame
police_officer_df = df[['officer_id_hash', 'precinct']]

# Create the SubjectSearch DataFrame
subject_search_df = df[['stop_id', 'officer_id_hash', 'date']]

# Create the PoliceOfficer dictionary mapping officer_id_hash to precinct
officer_to_precinct = pd.Series(df['precinct'].values, index=df['officer_id_hash']).to_dict()

# Create the SubjectSearch DataFrame with only necessary columns
subject_search_df = df[['stop_id', 'officer_id_hash', 'date']]

# Add precinct information to the SubjectSearch DataFrame
subject_search_df['precinct'] = subject_search_df['officer_id_hash'].map(officer_to_precinct)
subject_search_df['StopYear'] = pd.to_datetime(subject_search_df['date']).dt.year

# Perform the equivalent SQL query using pandas
precinct_yearly_stops = subject_search_df.groupby(['StopYear', 'precinct']).agg(NumStops=('stop_id', 'count')).reset_index()

yearly_stops = precinct_yearly_stops.groupby('StopYear').agg(TotalStops=('NumStops', 'sum')).reset_index()

precinct_yearly_stops['Rank'] = precinct_yearly_stops.groupby('StopYear')['NumStops'].rank(ascending=False, method='min')

result = precinct_yearly_stops[precinct_yearly_stops['Rank'] <= 3].merge(yearly_stops, on='StopYear')
result['PercentOfTotalStops'] = result['NumStops'] * 100.0 / result['TotalStops']
result = result.sort_values(['StopYear', 'Rank'])

print(result)

# Create the bar graph
pivot_df = result.pivot(index='StopYear', columns='precinct', values='PercentOfTotalStops')
ax = pivot_df.plot(kind='bar', stacked=False)

plt.title("Top 3 Precincts by Percentage of Total Stops per Year")
plt.xlabel("Year")
plt.ylabel("Percentage of Total Stops")
plt.legend(title="Precinct")
plt.xticks(rotation=0)

# Save the chart as a file
plt.savefig("top_3_precincts_by_percentage_of_total_stops_per_year.png", bbox_inches='tight')

plt.show()
"""


# RACE AND DISCRIMINATION | RACE AND DISCRIMINATION | RACE AND DISCRIMINATION | RACE AND DISCRIMINATION |


# searches per 100 drivers for each race
"""
# Convert the 'date' column to a datetime object
df['date'] = pd.to_datetime(df['date'])

# Calculate the total number of searches conducted for each race and year
searches_by_race_year = df[df['subject_race'].isin(['black', 'white', 'asian/pacific islander', 'hispanic'])].groupby([df['subject_race'], df['date'].dt.year]).agg(num_searches=('search_conducted', 'sum')).reset_index()

# Calculate the total number of drivers stopped for each race and year
drivers_by_race_year = df[df['subject_race'].isin(['black', 'white', 'asian/pacific islander', 'hispanic'])].groupby([df['subject_race'], df['date'].dt.year]).agg(num_drivers=('stop_id', 'count')).reset_index()

# Merge the two dataframes on race and year
merged_df = pd.merge(searches_by_race_year, drivers_by_race_year, on=['subject_race', 'date'])

# Calculate the number of searches conducted per 100 drivers for each race and year
merged_df['searches_per_100_drivers'] = merged_df['num_searches'] / merged_df['num_drivers'] * 100

# Pivot the data to create a table of searches per 100 drivers by race and year
pivot_table = merged_df.pivot(index='date', columns='subject_race', values='searches_per_100_drivers')

# Plot the multi-line graph
ax = pivot_table.plot(kind='line')
plt.title("Number of Searches Conducted per 100 Drivers by Race and Year")
plt.xlabel("Year")
plt.ylabel("Number of Searches Conducted per 100 Drivers")
plt.legend(title="Subject Race")

# Save the graph as a PNG file
plt.savefig("searches_per_100_drivers.png", bbox_inches='tight')

plt.show()
"""




# Stacked bar graph with percentage_of_stops_by_race_per_year.png
"""
# Define a dictionary to map subject races to colors
color_dict = {'black': '#7B3F00', 'white': 'orange', 'asian/pacific islander': 'blue', 'hispanic': 'green', 'other': 'red', 'unknown': 'purple'}

# Convert 'date' to a datetime object and extract the year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Group the data by year and subject_race, and count the stops
stops_by_race_year = df.groupby(['year', 'subject_race']).agg(num_stops=('stop_id', 'count')).reset_index()

# Calculate the total stops for each year
total_stops_by_year = df.groupby('year').agg(total_stops=('stop_id', 'count')).reset_index()

# Calculate the percentage of stops for each race and year
stops_by_race_year = stops_by_race_year.merge(total_stops_by_year, on='year')
stops_by_race_year['percentage'] = (stops_by_race_year['num_stops'] / stops_by_race_year['total_stops']) * 100

# Pivot the data to create a table suitable for plotting
pivot_table = stops_by_race_year.pivot(index='year', columns='subject_race', values='percentage')

# Plot the stacked bar graph
ax = pivot_table.plot(kind='bar', stacked=True, color=[color_dict[race] for race in pivot_table.columns])
plt.title("Percentage of Stops by Race Over the Years")
plt.xlabel("Year")
plt.ylabel("Percentage of Stops")
plt.legend(title="Subject Race")
plt.xticks(rotation=0)

# Save the chart as a file
plt.savefig("percentage_of_stops_by_race_per_year.png", bbox_inches='tight')

plt.show()
"""



# GENDER AGE & INEQUALITY | GENDER AGE & INEQUALITY | GENDER AGE & INEQUALITY | GENDER AGE & INEQUALITY | 

# Percentage of stops resulting in each outcome (warning, citation, arrest) by gender per year
"""
# Filter the data to include only stops with a warning or citation outcome
df = df[(df['warning_issued'] == 1) | (df['citation_issued'] == 1) | (df['arrest_made'] == 1)]

# Group the data by year, gender, and outcome, and count the unique stops
grouped = df.groupby([df['date'].dt.year, 'subject_sex', 'warning_issued', 'citation_issued', 'arrest_made']).agg(total_stops=('stop_id', 'nunique')).reset_index()

# Calculate the total stops for each gender and year
total_stops_by_year_gender = grouped.groupby(['date', 'subject_sex']).agg(total_stops=('total_stops', 'sum')).reset_index()

# Calculate the percentage of stops for each outcome
grouped['percentage'] = grouped['total_stops'] / grouped.merge(total_stops_by_year_gender, on=['date', 'subject_sex'], suffixes=('', '_total'))['total_stops_total'] * 100

# Pivot the data to create a table of percentages by year and gender
pivot_table = grouped.pivot_table(index=['date', 'subject_sex'], columns=['warning_issued', 'citation_issued', 'arrest_made'], values='percentage').fillna(0).reset_index()

years = sorted(df['date'].dt.year.unique())
width = 0.35

male_percentages = pivot_table.loc[pivot_table['subject_sex'] == 'male']
female_percentages = pivot_table.loc[pivot_table['subject_sex'] == 'female']

male_warnings = male_percentages.loc[:, (1, 0, 0)].values
male_citations = male_percentages.loc[:, (0, 1, 0)].values
male_arrests = male_percentages.loc[:, (0, 0, 1)].values

female_warnings = female_percentages.loc[:, (1, 0, 0)].values
female_citations = female_percentages.loc[:, (0, 1, 0)].values
female_arrests = female_percentages.loc[:, (0, 0, 1)].values

fig, ax = plt.subplots(figsize=(10, 6))

# Plot male bars
ax.bar(np.arange(len(years)) - width / 2, male_warnings, width, label='Male: Warning Issued')
ax.bar(np.arange(len(years)) - width / 2, male_citations, width, bottom=male_warnings, label='Male: Citation Issued')
ax.bar(np.arange(len(years)) - width / 2, male_arrests, width, bottom=male_warnings + male_citations, label='Male: Arrest Made')

# Plot female bars
ax.bar(np.arange(len(years)) + width / 2, female_warnings, width, label='Female: Warning Issued')
ax.bar(np.arange(len(years)) + width / 2, female_citations, width, bottom=female_warnings, label='Female: Citation Issued')
ax.bar(np.arange(len(years)) + width / 2, female_arrests, width, bottom=female_warnings + female_citations, label='Female: Arrest Made')

ax.set_title("Outcomes of Stops for Male and Female Drivers")
ax.set_xlabel("Year")
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years)
ax.set_ylabel("Percentage of Stops")
ax.legend(title="Outcome")
plt.savefig("male_female_outcomes_of_stops.png", bbox_inches='tight')
plt.show()
"""

# For each gender, determine the percentage of stops resulting in contraband found, drugs found, or weapons found
"""
# Filter the data to include only stops where a search was conducted
searched_df = df[df['search_conducted'] == 1]

# Group the data by year, gender, and contraband-related columns, and count the unique stops
grouped = searched_df.groupby([searched_df['date'].dt.year, 'subject_sex', 'contraband_found', 'contraband_drugs', 'contraband_weapons']).agg(total_stops=('stop_id', 'nunique')).reset_index()

# Calculate the total stops for each gender and year
total_searched_by_year_gender = grouped.groupby(['date', 'subject_sex']).agg(total_searched=('total_stops', 'sum')).reset_index()

# Calculate the percentage of stops for each contraband-related category
grouped['percentage'] = grouped['total_stops'] / total_searched_by_year_gender.merge(grouped.drop('total_stops', axis=1), on=['date', 'subject_sex'])['total_searched'] * 100

# Pivot the data to create a table of percentages by year and gender
pivot_table = grouped.pivot_table(index=['date', 'subject_sex'], columns=['contraband_found', 'contraband_drugs', 'contraband_weapons'], values='percentage').fillna(0).reset_index()

years = sorted(df['date'].dt.year.unique())
width = 0.3

grouped_sum = grouped.groupby(['date', 'subject_sex', 'contraband_found', 'contraband_drugs', 'contraband_weapons']).agg({'percentage': 'sum'}).reset_index()
pivot_table = grouped_sum.pivot_table(index=['date', 'subject_sex'], columns=['contraband_found', 'contraband_drugs', 'contraband_weapons'], values='percentage').fillna(0).reset_index()

# Calculate the percentage of stops for each contraband-related category
male_percentages = pivot_table.loc[pivot_table['subject_sex'] == 'male']
female_percentages = pivot_table.loc[pivot_table['subject_sex'] == 'female']

default_series = pd.Series(np.zeros(len(male_percentages)), index=male_percentages.index)

male_contraband = male_percentages.get((1, 0, 0), default_series).values + male_percentages.get((1, 1, 0), default_series).values + male_percentages.get((1, 0, 1), default_series).values + male_percentages.get((1, 1, 1), default_series).values
male_drugs = male_percentages.get((0, 1, 0), default_series).values + male_percentages.get((1, 1, 0), default_series).values + male_percentages.get((0, 1, 1), default_series).values + male_percentages.get((1, 1, 1), default_series).values
male_weapons = male_percentages.get((0, 0, 1), default_series).values + male_percentages.get((1, 0, 1), default_series).values + male_percentages.get((0, 1, 1), default_series).values + male_percentages.get((1, 1, 1), default_series).values

default_series = pd.Series(np.zeros(len(female_percentages)), index=female_percentages.index)

female_contraband = female_percentages.get((1, 0, 0), default_series).values + female_percentages.get((1, 1, 0), default_series).values + female_percentages.get((1, 0, 1), default_series).values + female_percentages.get((1, 1, 1), default_series).values
female_drugs = female_percentages.get((0, 1, 0), default_series).values + female_percentages.get((1, 1, 0), default_series).values + female_percentages.get((0, 1, 1), default_series).values + female_percentages.get((1, 1, 1), default_series).values
female_weapons = female_percentages.get((0, 0, 1), default_series).values + female_percentages.get((1, 0, 1), default_series).values + female_percentages.get((0, 1, 1), default_series).values + female_percentages.get((1, 1, 1), default_series).values

fig, ax = plt.subplots(figsize=(10, 6))

# Plot male bars
ax.bar(np.arange(len(years)) - width, male_contraband, width, label='Male: Contraband Found')
ax.bar(np.arange(len(years)) - width, male_drugs, width, bottom=male_contraband, label='Male: Drugs Found')
ax.bar(np.arange(len(years)) - width, male_weapons, width, bottom=male_contraband + male_drugs, label='Male: Weapons Found')

# Plot female bars
ax.bar(np.arange(len(years)), female_contraband, width, label='Female: Contraband Found')
ax.bar(np.arange(len(years)), female_drugs, width, bottom=female_contraband, label='Female: Drugs Found')
ax.bar(np.arange(len(years)), female_weapons, width, bottom=female_contraband + female_drugs, label='Female: Weapons Found')

ax.set_title("Percentage of Searches Resulting in Contraband, Drugs, or Weapons Found by Gender")
ax.set_xlabel("Year")
ax.set_xticks(np.arange(len(years)))
ax.set_xticklabels(years)
ax.set_ylabel("Percentage")
ax.legend()

# Save the figure as a PNG file
plt.savefig("search_contraband_gender_comparison.png", dpi=300, bbox_inches='tight')

# Display the figure
plt.show()
"""


# Average age of drivers pulled over in the top 5 precincts (ranked by highest number of stops)
"""
# Find the top 5 precincts by average number of stops
top_precincts = df.groupby('precinct').agg(total_stops=('stop_id', 'nunique')).sort_values(by='total_stops', ascending=False).head(5).index

# Filter data to include only the top 5 precincts
top_precincts_df = df[df['precinct'].isin(top_precincts)]

# Group data by precinct, year, and calculate the average driver age
grouped = top_precincts_df.groupby([top_precincts_df['date'].dt.year, 'precinct']).agg(avg_driver_age=('subject_age', 'mean')).reset_index()

# Create a multi-line graph
fig, ax = plt.subplots(figsize=(10, 6))

for precinct in top_precincts:
    precinct_data = grouped[grouped['precinct'] == precinct]
    ax.plot(precinct_data['date'], precinct_data['avg_driver_age'], label=f"Precinct {int(precinct)}")

ax.set_title("Average Age of Drivers Stopped in Top 5 Precincts by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Average Age")
ax.legend()

# Save the figure as a PNG file
plt.savefig("average_age_top_precincts.png", dpi=300, bbox_inches='tight')

# Display the figure
plt.show()
"""