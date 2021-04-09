import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd  # pip install pandas
import plotly.express as px
import random
from grafica import *
import base64

from main import app


# ----- Dropdown menu for 
data_structures = ['Graph', "Directed Graph"]
select_data_structure_dropdown = dcc.Dropdown(
    id='select-data-structure-dropown',
    value='Graph',
    clearable=False,
    options=[ {'label': name.capitalize(), 'value': name} for name in data_structures],
    style={"width":"14em"}
)

algorithms = ['Check if the graph is bipartite', 'Search for Eulerian walk', 
              'Search for a spanning tree by Breadth First Search', 
              'Search for a spanning tree by Depth First Search', 
              "Search for a minimum spanning tree using Kruskal's algorithm",
              "Search for a minimum spanning tree using Prim's algorithm"]

select_algorithm_dropdown = dcc.Dropdown(
    id='select-algorithm-dropown',
    value='Check if the graph is bipartite',
    clearable=False,
    options=[ {'label': name, 'value': name} for name in algorithms],
    style={"width":"32em"}
)

canvas = cyto.Cytoscape(
            id='graph',
            minZoom=0.2,
            maxZoom=1,
            layout={'name': 'preset'},
            boxSelectionEnabled = True,
            style={'width': '100%', 'height': '500px'},
            elements={'nodes': [], 'edges': []},
            stylesheet=[
                {
                    'selector': 'edge',
                    'style':{
                        'curve-style': 'bezier',
                        'label': 'data(weight)',
                    }
                },

                {
                    'selector': 'node',
                    'style':{
                        'label': 'data(label)',
                    }
                }
            ]
        )


layout = html.Div([
    dbc.Row([
        # Left column
        html.Div([
            html.Div([
                canvas,
            ], className="border border-secondary rounded"),

            html.Br(),

            dbc.Row([
                html.H4("Controls"),
            ], justify="center"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5("Nodes", className="text-muted"),   
                        dbc.Button("Add", className="mr-1", color="primary"),
                        dbc.Button("Edit", className="mr-1", color="primary"),
                        dbc.Button("Remove", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", className="mr-1", color="primary"),
                        dbc.Button("Edit", className="mr-1", color="primary"),
                        dbc.Button("Remove", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload Directed Graph from file", className="mr-1", color="success"),
                ])
                
            ], justify="center")

        ], className="col-md-6"),

        # Right Column
        dbc.Col([
            html.Div([
                    html.H4('Select Algorithm'),
                html.Table([

                    html.Tr([
                        html.Td([
                            select_algorithm_dropdown
                        ]),
                        html.Td([
                            dbc.Button("Run", size="sm", className="btn btn-warning"),
                        ], style={"padding":"1em"}),
                        
                    ])
                ]), 
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div([
                html.H4('Graph Information'),

                html.Table([

                    html.Tr([
                        html.Td([
                            html.P("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Input(value="", disabled=True)
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.P("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Input(value="", disabled=True)
                        ], style={"padding":"1em"}),
                        
                    ])
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                html.H4("Nodes Degrees"),
            ], justify="center"),

            html.Div([
                dbc.Table([
                
                    # Head of the table
                    html.Thead([
                        html.Tr([
                            html.Th([
                                html.H5("Node", className="text-muted"),   
                            ], className="col-xs-3"),

                            html.Th([
                                html.H5("Degree", className="text-muted"),   
                            ], className="col-xs-3")
                        ], style={"text-align":"center"})
                    ], style={}),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"97.5%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody([])
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
], id="main-content2")