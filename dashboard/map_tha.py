import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

with urlopen(
    "https://raw.githubusercontent.com/apisit/thailand.json/master/thailandWithName.json"
) as response:
    counties = json.load(response)

df = pd.read_csv("data/province.csv")

fig = px.choropleth(
    df,
    geojson=counties,
    featureidkey="properties.name",
    locations="province_eng_name",
    scope="asia",
    color="totalstd",
    color_continuous_scale="Viridis",
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()
