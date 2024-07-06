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
dropdown_opt = []
for i, j in zip(df.schools_province.tolist(), df.province_eng_name.tolist()):
    dropdown_opt.append({"label": i, "value": j})

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("จำนวนการจบการศึกษาชั้นมัธยมศึกษาปีที่ 6"),
        html.P("เลือกข้อมูลที่ต้องการ"),
        dcc.Dropdown(
            options=dropdown_opt,
            id="dropdown",
            placeholder="เลือกจังหวัด",
        ),
        dcc.RadioItems(
            id="gender", options=["ชาย", "หญิง", "รวม"], value="รวม", inline=True
        ),
        dcc.Graph(id="graph"),
        dcc.Graph(id="bar_chart"),
    ]
)


@app.callback(Output("bar_chart", "figure"), Input("dropdown", "value"))
def update_bar_chart(value):
    if value != None:
        tmp_df = df[df["province_eng_name"] == value]
        data = {
            "sex": ["ผู้หญิง", "ผู้ชาย"],
            "total": [tmp_df["totalfemale"].iloc[0], tmp_df["totalmale"].iloc[0]],
        }
        topic = "จังหวัด" + tmp_df["schools_province"].iloc[0]
    else:
        data = {
            "sex": ["ผู้หญิง", "ผู้ชาย"],
            "total": [df["totalfemale"].sum(), df["totalmale"].sum()],
        }
        topic = "ทุกจังหวัด"
    df_new = pd.DataFrame(data)
    fig = px.bar(df_new, x="sex", y="total", text_auto=True, title=topic)
    return fig


@app.callback(
    Output("graph", "figure"),
    Input("gender", "value"),
    Input("dropdown", "value"),
)
def display_choropleth(gender, dropdow):
    look_up_t = ["ชาย", "หญิง", "รวม"]
    gender_id = look_up_t.index(gender)
    col_name = ["totalmale", "totalfemale", "totalstd"]
    data = df
    if dropdow != None:
        data = df[df["province_eng_name"] == dropdow]
        # locations = dropdow

    fig = px.choropleth_mapbox(
        data,
        geojson=counties,
        featureidkey="properties.name",
        locations="province_eng_name",
        color=col_name[gender_id],
        color_continuous_scale="Viridis",
        hover_name="schools_province",
        mapbox_style="carto-positron",
        center={"lat": 13.342077, "lon": 100.5018},
        zoom=4.3,
        opacity=0.7,
        labels={
            "province_eng_name": "Province",
            "totalmale": "ผู้ชาย",
            "totalfemale": "ผู้หญิง",
            "totalstd": "รวม",
        },
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# fig.show()
app.run_server(debug=True)
