import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

mapbox_api_key = "pk.eyJ1IjoiY3lydXMtZXN0YXZpbGxvIiwiYSI6ImNsZ3I3NGQzaDA2OW8zZHM4eWVib3VwZDMifQ.4lVrgK9XrmT1IpRqCYNaHQ"
px.set_mapbox_access_token(mapbox_api_key)

data = pd.read_csv("cleaned_data.csv", parse_dates=["date"])

data = data.sort_values(by="date")

# Ignore null time samples
data = data[data["time"].notnull()]

# Extract the year from the 'date' column
data['year'] = data['date'].dt.year

# Count the number of stops for each year
stops_by_year = data['year'].value_counts()


# Print the result
print(stops_by_year)



# Filter data for stops in 2012, because it has the most stops
data = data[data["date"].dt.year == 2012]


data["date_str"] = data["date"].dt.strftime("%m-%d-%Y")


colors = {
    "white": "blue",
    "black": "orange",
    "hispanic": "#0BDA51",
    "asian/pacific islander": "red",
    "unknown": "#BF40BF",
    "other": "#BF40BF",
}

fig = px.scatter_mapbox(
    data,
    lat="lat",
    lon="lng",
    color="subject_race",
    hover_name="subject_race",
    animation_frame="date_str",
    animation_group="subject_race",
    zoom=9,
    height=600,
    labels={"subject_race": "Race"},
    custom_data=["subject_race"],
    color_discrete_map=colors,
)

fig.update_layout(
    mapbox_style="mapbox://styles/mapbox/dark-v11",
    title={
        'text': "",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 24, 'family': 'Arial', 'color': 'white'}
    }
)

fig.update_traces(marker=dict(size=5))

fig.update_traces(
    hovertemplate="<b>Lat:</b> %{lat}<br><b>Lon:</b> %{lon}<br><b>Race:</b> %{customdata[0]}<extra></extra>"
)

# Save the figure to an HTML file
pio.write_html(fig, file="traffic_stops_2012.html", auto_open=True)
