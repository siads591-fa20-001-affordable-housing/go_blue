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


# +
# Convert json into a dataframe to be merged with the dataframe
a_df = pd.json_normalize(GRParcels['features'])

# Drop tables that will not be needed in the data frame
a_df.drop(columns = ['id', 
                     'type', 
                     'bbox', 
                     'geometry.type', 
                     'geometry.coordinates',
                     'properties.SHAPE_len', 
                     'geometry.coordinates',
                     'properties.Govt_Unit',
                     'properties.PPN',
                     'properties.Prop_Class', 
                     'properties.School_Dis'
                    ], 
          inplace = True)

# Remove the prefix from the col labels
a_df.rename(columns = {'properties.PNUM':'APN', 
                       'properties.Address':'Address',
                       'properties.City':'City',
                       'properties.Zip_Code':'Zip',
                       'properties.SHAPE_area':'Area',
                      }, inplace = True)


# +
# Read in the data from database and clean-up
database = dbconfig()
table = r"siads591_property_level"
# condition = r" where walkscore > 0"
condition = ""

sql = f'select * from {table}{condition}'
df = pd.read_sql(sql, database)
df = df.rename(columns={'apn':'APN', 
                        'mshda score' : 'mshda_score'}
              )
# -


# Merge the plot attributes to the dataframe
details = df.merge(a_df, on = "APN", how = "outer").copy(deep = True)

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
    [Input(component_id='select_score', component_property='value')])

def update_graph(option_score):
    print(option_score)
    print(type(option_score))

    container = "The min score chosen was: {}".format(option_score)
    
    dff = details.copy(deep=True)
    selection = dff.mshda_score > option_score
    dff = dff[selection]

    # plot dff data\
    fig=px.choropleth_mapbox(dff,
                             geojson=GRParcels,
                             color='mshda_score',
                             opacity=0.2,
                             locations='APN',
                             featureidkey = 'properties.APN',
                             center= {'lat':42.9634,'lon':-85.6681}, 
                             hover_data = ['APN',
                                           'address', 
                                           'city',
                                           'zip_code',
                                           'acres', 
                                           'sev'
                                          ],
                             mapbox_style="carto-positron", zoom=5)
    
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

    return container, fig


# -

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)


