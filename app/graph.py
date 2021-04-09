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
import digraph

from main import app


# ----- Dropdown menu for data structure selection -----
data_structures = ['Graph', "Directed Graph"]
select_data_structure_dropdown = dcc.Dropdown(
    id='select-data-structure-dropdown',
    value='Graph',
    clearable=False,
    options=[ {'label': name.capitalize(), 'value': name} for name in data_structures],
    style={"width":"14em"}
)
# -------------------------------------------------------

# ----- Dropdown menu for algorithm selection -----
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
# -------------------------------------------------------

# ----- Dash Cytoscape instance to display data structures -----
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
# -------------------------------------------------------

# ----- Modal to edit nodes -----
edit_nodes_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Edit Nodes"),
                dbc.ModalBody(
                   id="edit-nodes-modal-body"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-nodes-modal", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-nodes-modal", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-nodes-modal",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=True, 
            fade=True
        )
    ]
)
# -------------------------------------------------------
edit_edges_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Edit edge"),
                dbc.ModalBody(
                   id="edit-edges-modal-body"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-edges-modal", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-edges-modal", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-edges-modal",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=True, 
            fade=True
        )
    ]
)

# ----- MAIN LAYOUT -----
layout = html.Div(children=[
    # ----- Store objects to store nodes and edges information -----
    dcc.Store(
        id='nodes-info', data=[]
    ),
    dcc.Store(
        id='edges-info', data=[]
    ),
    # 1- No nodes selected when edit node button is clicked
    # 2- No nodes selected when remove node button is clicked
    # 3- No nodes selected when add edge button is clicked
    # 4- More than two nodes selected when add edge button is clicked
    dcc.Store(
        id='alert-info', data=None
    ),

    # ----- Div to display nodes errors -----
    html.Div(id="edit-nodes-alert", children=[]),

    edit_nodes_modal,
    
    edit_edges_modal,

    dbc.Row([
        # Left column
        dbc.Col([
            html.Div([
                dbc.Alert(id="alert", is_open=False, dismissable=True, color="warning"),
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
                        dbc.Button("Add", id="add-node-btn", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-nodes-btn", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-nodes-btn", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", id="add-edge-btn", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-edges-btn", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-edges-btn", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload graph from file", className="mr-1", color="success"),
                ])
                
            ], justify="center")
        ], md=6),

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
                            html.Label("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-nodes-label", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Label("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-edges-label", color="primary")
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
                            ], style={"text-align":"center"}),

                            html.Th([
                                html.H5("Degree", className="text-muted"),   
                            ], style={"text-align":"center"})
                        ])
                    ]),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"100%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody(id="nodes-degrees-table", children=[])
                ],bordered=False, responsive=False),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
])

# ----- AUXILIAR FUNCTIONS -----
def manage_nodes_table(table_childrens, action, values=None):
    if action == "edit":
        for value in values:
            for children in table_childrens:
                if children['props']['children'][0]['props']['children'] == value[0]:
                    children['props']['children'][0]['props']['children'] = value[1]
                    break
    
    elif action == "remove nodes":
        table_childrens = [c for c in table_childrens if c['props']['children'][0]['props']['children'] not in values]
    
    elif action == "increment degree":
        for value in values:
            for children in table_childrens:
                if children['props']['children'][0]['props']['children'] == value:
                    current_degree = int(children['props']['children'][1]['props']['children'])
                    children['props']['children'][1]['props']['children'] = str(current_degree + 1)
                    break

    elif action == "update degrees":
        childrens = table_childrens[0]
        graph_edges = table_childrens[1]

        degrees = {children['props']['children'][0]['props']['children']:0 for children in childrens}

        for edge in graph_edges:

            degrees[edge['data']['source']] += 1
            degrees[edge['data']['target']] += 1

        for children in childrens:
            node = children['props']['children'][0]['props']['children'] 
            children['props']['children'][1]['props']['children'] = str(degrees[node])
        
        table_childrens = childrens
            


    return table_childrens

def manage_graph_elements(graph_elements, action, values=None):
    if action == "edit nodes":
        for value in values:
            for node in graph_elements['nodes']:
                if node['data']['id'] == value[0]:
                    node['data']['id'] = value[1]
                    node['data']['label'] = value[1]
                    break

    elif action == "remove nodes":
        graph_elements['nodes'] = [e for e in graph_elements['nodes'] if e['data']['id'] not in values]
        graph_elements['edges'] = [e for e in graph_elements['edges'] if e['data']['source'] not in values and e['data']['target'] not in values]
    
    return graph_elements

def manage_nodes_info(nodes_info, action, values=None):
    if action == "edit":
        for value in values:
            nodes_info[nodes_info.index(value[0])] = value[1]

    elif action == "remove":
        nodes_info = [node for node in nodes_info if node not in values]
    
    return nodes_info

def manage_edges_info(edges_info, action, values=None):
    if action == "remove due nodes elimination":
        edges_info = [e for e in edges_info if e[0] not in values and e[1] not in values]
    return edges_info

# ----- Callback to update the graph -----
@app.callback(
    [Output("graph", "elements"), Output("nodes-info", "data"), 
     Output("nodes-degrees-table", "children"), Output("number-of-nodes-label", "children"),
     Output("alert-info", "data"), Output("number-of-edges-label", "children"), 
     Output("edges-info", "data")],

    [Input("add-node-btn", "n_clicks"), Input("done-btn-edit-nodes-modal", "n_clicks"),
     Input("remove-nodes-btn", "n_clicks"), Input("edit-nodes-btn", "n_clicks"),
     Input("add-edge-btn", "n_clicks"), Input("done-btn-edit-edges-modal", "n_clicks"),
     Input("edit-edges-btn", "n_clicks"),],
    
    [State("graph", "elements"), State("nodes-info", "data"), 
     State("nodes-degrees-table", "children"), State("number-of-nodes-label", "children"),
     State("edit-nodes-modal-body", "children"), State("graph", "selectedNodeData"),
     State("number-of-edges-label", "children"), State("edges-info", "data"),
     State("edit-edges-modal-body", "children"), State("graph", "selectedEdgeData")]
)
def updateGraph(add_node_btn_n_clicks, done_btn_edit_nodes_modal, remove_nodes_btn, edit_nodes_btn,
    add_edge_btn, done_btn_edit_edges_modal, edit_edges_btn, graph_elements, nodes_info, 
    nodes_degrees_table_children, number_of_nodes, edit_nodes_modal_body_childrens, 
    selected_node_data, number_of_edges, edges_info, edit_edges_modal_body_childrens,
    selected_edge_data):
    # Getting the callback context to know which input triggered this callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        btn_triggered = ctx.triggered[0]['prop_id'].split('.')[0]

        # ----- Add node case -----
        if btn_triggered == "add-node-btn":
            # Adding the node to the graph_elements and to nodes_info data
            node = {'data': {'id': add_node_btn_n_clicks, 'label': add_node_btn_n_clicks},
                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)}}
            
            graph_elements['nodes'].append(node)
            nodes_info.append(str(add_node_btn_n_clicks))

            # Adding the node to the node_degrees_table
            nodes_degrees_table_children.append(html.Tr([
                html.Td(str(add_node_btn_n_clicks), style={"text-align":"center"}), 
                html.Td(0,  style={"text-align":"center"})
                ], className="table-primary"))
            print("ADD NODE CASE")
            print("graph elements")
            print(graph_elements)
            print("\nNodes info")
            print(nodes_info)
            print("\nEdges info")
            print(edges_info)
            print("------------------------------\n")
            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes+1, None, number_of_edges, edges_info
        
        # ----- Edit nodes case -----
        elif btn_triggered == "done-btn-edit-nodes-modal":
            # If no node is selected, raise an error message
            values = []
            # Getting the new values
            for children in edit_nodes_modal_body_childrens:
                # Getting the new label
                try:
                    new_label = children['props']['children'][1]['props']['children'][1]['props']['value']
                except:
                    continue
                
                # Getting the current label
                current_label = children['props']['children'][0]['props']['children'][1]['props']['children']

                print("new label", new_label)
                print("current label", current_label)
                # Do nothing if new label == current label or if the new label already exists
                if new_label == current_label or new_label in nodes_info:
                    continue

                # Add the new label to the node info
                nodes_info[nodes_info.index(current_label)] = new_label

                values.append((current_label, new_label))
                
                # Editing nodes
                for node in graph_elements['nodes']:
                    if node['data']['id'] == current_label:
                        node['data']['id'] = new_label
                        node['data']['label'] = new_label
                        break
                
                # Editing edges
                old_edges = []
                for edge, edge_info_element in zip(graph_elements['edges'], edges_info):
                    new_source = None
                    new_target = None
                    # Editing edges elements
                    if edge['data']['source'] == current_label or edge['data']['target'] == current_label:
                        if edge['data']['source'] == current_label:
                            new_source = new_label
                        else:
                            new_source = edge['data']['source']
                        
                        if edge['data']['target'] == current_label:
                            new_target = new_label
                        else:
                            new_target = edge['data']['target']
                        
                        graph_elements['edges'].append({'data': {'source': new_source, 'target': new_target, 'weight': edge['data']['weight']}})                
                        old_edges.append(edge)
                    
                    # Editing edges_info
                    if edge_info_element[0] == current_label:
                        edge_info_element[0] = new_label
                    if edge_info_element[1] == current_label:
                        edge_info_element[1] = new_label
                
                graph_elements['edges'] = [e for e in graph_elements['edges'] if e not in old_edges]

            
            # Editing the nodes in the nodes degrees table
            nodes_degrees_table_children = manage_nodes_table(nodes_degrees_table_children, "edit", values)


            print("EDIT NODE CASE")
            print("graph elements")
            print(graph_elements)
            print("\nNodes info")
            print(nodes_info)
            print("\nEdges info")
            print(edges_info)
            print("------------------------------\n")

            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, edges_info
        
        # ---- Edit nodes button alert handle -----
        elif btn_triggered == "edit-nodes-btn":
            alert = None
            if not selected_node_data:
                alert = 1
            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, edges_info

        # ----- Remove nodes case ------
        elif btn_triggered == "remove-nodes-btn":
            alert = None
            if selected_node_data:
                # Getting the names of the nodes to remove
                ids = [selectedNode['id'] for selectedNode in selected_node_data]
                
                # Updating remaining nodes and edges from graph elements
                graph_elements = manage_graph_elements(graph_elements, "remove nodes", ids)
                # Removing deleted nodes from the nodes info
                nodes_info = manage_nodes_info(nodes_info, "remove", ids)
                #Removing deleted nodes from nodes degrees table
                nodes_degrees_table_children = manage_nodes_table(nodes_degrees_table_children, "remove nodes", ids)
                nodes_degrees_table_children = manage_nodes_table((nodes_degrees_table_children, graph_elements['edges']), "update degrees")
                # Removing deleted edges from edges_info
                edges_info = manage_edges_info(edges_info, "remove due nodes elimination", ids)
                # Updating number of nodes and number of edges
                number_of_nodes -= len(ids)
                number_of_edges = len(graph_elements['edges'])
            else:
                alert = 2
            
            print("REMOVE NODES CASE")
            print("graph elements")
            print(graph_elements)
            print("\nNodes info")
            print(nodes_info)
            print("\nEdges info")
            print(edges_info)
            print("------------------------------\n")
            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, edges_info
        
        # ----- Add Edge case -----
        elif btn_triggered == "add-edge-btn":
            alert = None
            # When no node is selected
            if not selected_node_data:
                alert = 3
            # When more than two nodes are selected
            elif len(selected_node_data) > 2:
                alert = 4
            # When exactly one node is selected (loop)
            elif len(selected_node_data) == 1:
                node = selected_node_data[0]['id']
                loop = {'data': {'source': node, 
                            'target': node, 'weight': "0"}}
                graph_elements['edges'].append(loop)

                # Updating the node degree in the nodes degrees table
                nodes_degrees_table_children = manage_nodes_table(nodes_degrees_table_children, "increment degree", [node, node])
                number_of_edges += 1
                edges_info.append([node, node, "0"])
            # When exactly two nodes are selected (edge)
            elif len(selected_node_data) == 2:
                node1 = selected_node_data[0]['id']
                node2 = selected_node_data[1]['id']
                edge = {'data': { 'source': node1, 
                                'target': node2, 'weight': "0"}}
                graph_elements['edges'].append(edge)

                # Updating the node degree in the nodes degrees table
                nodes_degrees_table_children = manage_nodes_table(nodes_degrees_table_children, "increment degree", [node1, node2])
                number_of_edges += 1
                edges_info.append([node1, node2, "0"])

            print("ADD EDGES CASE")
            print("graph elements")
            print(graph_elements)
            print("\nNodes info")
            print(nodes_info)
            print("\nEdges info")
            print(edges_info)
            print("------------------------------\n")

            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, edges_info
        
        elif btn_triggered == "done-btn-edit-edges-modal":

            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, edges_info
        
        # ---- Edit edges button alert handle -----
        elif btn_triggered == "edit-edges-btn":
            alert = None
            if not selected_edge_data:
                alert = 5
            return graph_elements, nodes_info, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, edges_info

        
    else:
        return dash.no_update

# ----- Callback to manage "Edit nodes" modal -----
@app.callback(
    [Output("edit-nodes-modal", "is_open"), Output("edit-nodes-modal-body", "children")],
    [Input("edit-nodes-btn", "n_clicks"), Input("cancel-btn-edit-nodes-modal", "n_clicks"), 
     Input('done-btn-edit-nodes-modal', 'n_clicks')],
    [State("graph", "selectedNodeData"), State("edit-nodes-modal", "is_open")]
)
def toggleModal(edit_nodes_btn, cancel_btn_edit_nodes_modal, done_btn_edit_nodes_modal, 
    selected_node_data, is_modal_open):
    if edit_nodes_btn:
        if not selected_node_data:
            return False, []
        else:
            node_forms = []
            for node in selected_node_data:
                current_id = node['id']
                node_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Current label: ", style={"padding":"1em"}),
                                    dbc.Label(current_id, id=str(current_id))
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("New label: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text", placeholder="Type the new label")
                                ],
                                className="mr-3"
                            )
                        ],
                        inline=True
                    )
                )

            return not is_modal_open, node_forms
    return is_modal_open, []

# ----- Callback to manage "Edit edge" modal -----
@app.callback(
    [Output("edit-edges-modal", "is_open"), Output("edit-edges-modal-body", "children")],
    [Input("edit-edges-btn", "n_clicks"), Input("cancel-btn-edit-edges-modal", "n_clicks"), 
     Input('done-btn-edit-edges-modal', 'n_clicks')],
    [State("graph", "selectedEdgeData"), State("edit-edges-modal", "is_open")]
)
def toggleModal(edit_edges_btn, cancel_btn_edit_edges_modal, done_btn_edit_edges_modal, 
    selected_edge_data, is_modal_open):
    if edit_edges_btn:
        if not selected_edge_data:
            return False, []
        else:
            edges_forms = []
            for edge in selected_edge_data:
                node1 = edge['source']
                node2 = edge['target']
                edges_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label(f"Edge ({node1},{node2}) current weight: ", style={"padding":"1em"}),
                                    dbc.Label(edge['weight'])
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("New weight: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text", placeholder="Type the new weight")
                                ],
                                className="mr-3"
                            )
                        ],
                        inline=True
                    )
                )
            
            return not is_modal_open, edges_forms

    return is_modal_open, []

# ----- Chained callback to display an alert if it is necesary
@app.callback(
    [Output('alert', "children"), Output('alert', "is_open")],
    Input('alert-info', 'data')
)
def manageAlert(alert_info):
    print(alert_info)
    text = ""
    show = False
    if alert_info == 1:
        text = "No node selected to edit. Please, select at least one node and try again"
        show = True
    elif alert_info == 2:
        text = "No node selected to remove. Please, select at least one node and try again"
        show = True
    elif alert_info == 3:
        text = "No nodes selected to add an edge. Please, select one or two nodes and try again"
        show = True
    elif alert_info == 4:
        text = "More than two nodes selected to add an edge. Please, select one or two nodes and try again"
        show = True
    elif alert_info == 5:
        text = "No edge selected to edit. Please, select at least one edge and try again"
        show = True
    
    return text, show