import pandas as pd
import plotly.express as px  # (version 4.7.0)

import pandas as pd
import geopandas
from config import dbconfig
from sqlalchemy import create_engine
import plotly.express as px

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
GRParcels=geopandas.read_file('City_of_grand_rapids_parcels.shp')
GRParcels=GRParcels.to_crs('EPSG:4326')
GRParcels=GRParcels.__geo_interface__

database = dbconfig()
table = r"walkscore"
walkscore = pd.read_sql(table, database)
print(walkscore[:5])


dff = walkscore.copy(deep = True)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    dcc.Dropdown(id="select_score",
                 options=[
                     {"label": "0", "value": 0},
                     {"label": "1", "value": 1},
                     {"label": "2", "value": 2},
                     {"label": "3", "value": 3},
                     {"label": "4", "value": 4},
                     {"label": "5", "value": 5},
                     {"label": "6", "value": 6},
                     {"label": "7", "value": 7},
                     {"label": "8", "value": 8},
                     {"label": "9", "value": 9},
                     {"label": "10", "value": 10},
                     {"label": "11", "value": 11},
                     {"label": "12", "value": 12}
                 ],
                 multi=False,
                 value=0,
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='city_map', figure={})])


# +
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='city_map', component_property='figure')],
    [Input(component_id='select_score', component_property='value')]
)
def update_graph(option_score):
    print(option_score)
    print(type(option_score))

    container = "The min score chosen was: {}".format(option_score)

    dff = walkscore.copy(deep = True)
    dff = dff[dff.walkscore >= option_score]


    fig=px.choropleth_mapbox(dff,geojson=GRParcels,color='walkscore',\
                            locations='original_apn',featureidkey='properties.PNUM',\
                            center={'lat':42.9634,'lon':-85.6681},
                            mapbox_style="carto-positron", zoom=5)
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})



#     # Plotly Express
#     fig = px.choropleth(
#         data_frame=dff,
#         locationmode='USA-states',
#         locations='original_apn',
#         scope="usa",
#         color='walkscore',
#         hover_data=['original_apn', 'walkscore'],
#         color_continuous_scale=px.colors.sequential.YlOrRd,
#         labels={'walkscore': 'walkscore'},
#         template='plotly_dark'
#     )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig
# -

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


