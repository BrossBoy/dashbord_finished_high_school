from dash import Dash, dcc, html, Input, Output
import json
from urllib.request import urlopen
import pandas as pd
import plotly.express as px

with urlopen(
    "https://raw.githubusercontent.com/apisit/thailand.json/master/thailandWithName.json"
) as response:
    counties = json.load(response)

df = pd.read_csv("data/province.csv")

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("จำนวนการจบการศึกษาชั้นมัธยมศึกษาปีที่ 6"),
        html.P("เลือกข้อมูลที่ต้องการ"),
        dcc.RadioItems(
            id="gender", options=["ชาย", "หญิง", "รวม"], value="รวม", inline=True
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(Output("graph", "figure"), Input("gender", "value"))
def display_choropleth(gender):
    look_up_t = ["ชาย", "หญิง", "รวม"]
    gender_id = look_up_t.index(gender)
    col_name = ["totalmale", "totalfemale", "totalstd"]
    fig = px.choropleth_mapbox(
        df,
        geojson=counties,
        featureidkey="properties.name",
        locations="province_eng_name",
        color=col_name[gender_id],
        color_continuous_scale="Viridis",
        hover_name="schools_province",
        mapbox_style="carto-positron",
        center={"lat": 13.342077, "lon": 100.5018},
        zoom=4.9,
        opacity=0.7,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# fig.show()
app.run_server(debug=True)
