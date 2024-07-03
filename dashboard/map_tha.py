import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

with urlopen(
    "https://raw.githubusercontent.com/apisit/thailand.json/master/thailandWithName.json"
) as response:
    counties = json.load(response)

df = pd.read_csv("data/province.csv")

fig = px.choropleth_mapbox(
    df,
    geojson=counties,
    featureidkey="properties.name",
    locations="province_eng_name",
    color="totalstd",
    color_continuous_scale="Viridis",
    hover_name="schools_province",
    mapbox_style="carto-positron",
    center={"lat": 13.342077, "lon": 100.5018},
    zoom=4.9,
    opacity=0.7,
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
