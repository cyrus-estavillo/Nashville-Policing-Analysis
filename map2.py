import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon

# Read state, county data, and cleaned_data.csv
state_df = gpd.read_file("https://datascience.quantecon.org/assets/data/cb_2016_us_state_5m.zip")
county_df = gpd.read_file("https://datascience.quantecon.org/assets/data/cb_2016_us_county_5m.zip")
data_df = pd.read_csv("cleaned_data.csv")

# Filter for the specific county by FIPS code
tennessee_county_037 = county_df.query("STATEFP == '47' and COUNTYFP == '037'")

# Get the geometry of the specific county and set the CRS
county_polygon = tennessee_county_037.geometry.iloc[0]
county_crs = tennessee_county_037.crs

# Create a GeoDataFrame from cleaned_data.csv with lat and lng as Point geometry
geometry = [Point(xy) for xy in zip(data_df['lng'], data_df['lat'])]
geo_df = gpd.GeoDataFrame(data_df, crs=county_crs, geometry=geometry)

# Filter the data to only include points within the specific county
geo_df = geo_df[geo_df.geometry.within(county_polygon)]

# Define a function to map subject_race to colors
def race_color(race):
    if race == 'white':
        return 'blue'
    elif race == 'black':
        return 'orange'
    elif race == 'hispanic':
        return 'green'
    elif race == 'asian/pacific islander':
        return 'red'
    else:
        return 'purple'

# Apply the function to create a new column with colors
geo_df['color'] = geo_df['subject_race'].apply(race_color)

# Convert the 'date' column to a datetime object
geo_df['date'] = pd.to_datetime(geo_df['date'])

print("About to plot a map for each year")

# Plot a map for each year between 2010 and 2019
for year in range(2010, 2019):
    yearly_geo_df = geo_df[geo_df['date'].dt.year == year]
    
    fig, gax = plt.subplots(figsize=(10, 10))
    tennessee_county_037.plot(ax=gax, edgecolor="white", color="black")

    for _, row in yearly_geo_df.iterrows():
        gax.plot(*row['geometry'].coords.xy, marker='o', markersize=5, color=row['color'])
    
    # Create the legend
    race_categories = {'white': 'blue', 'black': 'orange', 'hispanic': 'green',
                       'asian/pacific islander': 'red', 'unknown': 'purple', 'other': 'purple'}
    for race, color in race_categories.items():
        gax.plot([], [], marker='o', markersize=5, color=color, label=race)

    print("About to plot")
    
    gax.legend(title='Subject Race')
    plt.title(f"Traffic Stops in Nashville, Tennessee ({year})")
    plt.savefig(f"map_{year}.png")
    plt.show()