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
import uuid

from main import app

# ----- Dropdown menu for algorithm selection -----
algorithms = ["Find shortest path between two nodes using Dijkstra's algorithm",
              "Find shortest paths from one node to all others using Dijkstra's algorithm",
              "Find shortest paths from each node to all others using Floyd-Warshall algorithm"]
select_algorithm_dropdown = dcc.Dropdown(
    id='select-algorithm-dropown-digraph',
    value="Find shortest path between two nodes using Dijkstra's algorithm",
    clearable=False,
    options=[ {'label': name, 'value': name} for name in algorithms],
    style={"width":"32em"}
)
# -------------------------------------------------------

# ----- Dash Cytoscape instance to display data structures -----
canvas = cyto.Cytoscape(
            id='digraph',
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
                        'target-arrow-shape': 'triangle',
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

# ----- Modals fixed position to allow the user to see the graph while he's updating it -----
modals_position = {
                    "position": "absolute",
                    "top": "0",
                    "right": "0",
                    "bottom": "0",
                    "left": "50%",
                    "z-index": "10040",
                    "overflow": "auto",
                    "overflow-y": "auto"
                }
# -------------------------------------------------------

# ----- Modal to edit nodes -----
edit_nodes_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Edit Nodes"),
                dbc.ModalBody(
                   id="edit-nodes-modal-body-digraph"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-nodes-modal-digraph", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-nodes-modal-digraph", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-nodes-modal-digraph",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            style=modals_position
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
                   id="edit-edges-modal-body-digraph"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-edges-modal-digraph", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-edges-modal-digraph", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-edges-modal-digraph",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            style=modals_position
        )
    ]
)

# ----- MAIN LAYOUT -----
layout = html.Div(children=[
    # ----- Store objects to store nodes and edges information -----
    dcc.Store(
        id='nodes-info-digraph', data=[['a', 1]] # The first element is the first node name that we will use
    ),
 
    # 1- No nodes selected when edit node button is clicked
    # 2- No nodes selected when remove node button is clicked
    # 3- No nodes selected when add edge button is clicked
    # 4- More than two nodes selected when add edge button is clicked
    dcc.Store(
        id='alert-info-digraph', data=None
    ),

    # ----- Div to display nodes errors -----
    html.Div(id="edit-nodes-alert-digraph", children=[]),

    edit_nodes_modal,
    
    edit_edges_modal,

    dbc.Row([
        # Left column
        dbc.Col([
            html.Div([
                dbc.Alert(id="alert-digraph", is_open=False, dismissable=True, color="warning"),
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
                        dbc.Button("Add", id="add-node-btn-digraph", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-nodes-btn-digraph", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-nodes-btn-digraph", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", id="add-edge-btn-digraph", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-edges-btn-digraph", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-edges-btn-digraph", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload directed graph from file", className="mr-1", color="success"),
                ], id="upload-digraph-obj")
                
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
                html.H4('Directed Graph Information'),

                html.Table([

                    html.Tr([
                        html.Td([
                            html.Label("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-nodes-label-digraph", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Label("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-edges-label-digraph", color="primary")
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
                            ], style={"text-align":"center", "width":"32%"}),

                            html.Th([
                                html.H5("Positive Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"32%"}),

                            html.Th([
                                html.H5("Negative Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"32%"})
                        ])
                    ]),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"100%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody(id="nodes-degrees-table-digraph", children=[])
                ],bordered=False, responsive=False),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
])

# ----- Callback to update the graph -----
@app.callback(
    [Output("digraph", "elements"), Output("nodes-degrees-table-digraph", "children"), 
     Output("number-of-nodes-label-digraph", "children"), Output("alert-info-digraph", "data"), 
     Output("number-of-edges-label-digraph", "children"), Output('nodes-info-digraph', 'data'), 
     Output('upload-digraph-obj', 'contents')],

    [Input("add-node-btn-digraph", "n_clicks"), Input("done-btn-edit-nodes-modal-digraph", "n_clicks"),
     Input("remove-nodes-btn-digraph", "n_clicks"), Input("edit-nodes-btn-digraph", "n_clicks"),
     Input("add-edge-btn-digraph", "n_clicks"), Input("done-btn-edit-edges-modal-digraph", "n_clicks"),
     Input("edit-edges-btn-digraph", "n_clicks"), Input('remove-edges-btn-digraph', 'n_clicks'), 
     Input('upload-digraph-obj', 'contents')],
    
    [State("digraph", "elements"), State("nodes-degrees-table-digraph", "children"), 
     State("number-of-nodes-label-digraph", "children"), State("edit-nodes-modal-body-digraph", "children"), 
     State("digraph", "selectedNodeData"), State("number-of-edges-label-digraph", "children"), 
     State("edit-edges-modal-body-digraph", "children"), State("digraph", "selectedEdgeData"), State('nodes-info-digraph', 'data')]
)
def updateDigraph(add_node_btn_n_clicks, done_btn_edit_nodes_modal, remove_nodes_btn, edit_nodes_btn,
    add_edge_btn, done_btn_edit_edges_modal, edit_edges_btn, remove_edges_btn, upload_graph_contents,
    graph_elements, nodes_degrees_table_children, number_of_nodes, edit_nodes_modal_body_childrens, 
    selected_node_data, number_of_edges, edit_edges_modal_body_childrens, selected_edge_data, nodes_info):
    # Getting the callback context to know which input triggered this callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        btn_triggered = ctx.triggered[0]['prop_id'].split('.')[0]

        # ----- Add node case -----
        if btn_triggered == "add-node-btn-digraph":

            # Getting an unique initial name
            while True:
                node_name = nodes_info[0][0] * nodes_info[0][1]
                repeated_name = False

                for node in graph_elements['nodes']:
                    if node['data']['label'] == node_name:
                        repeated_name = True
                        # Updating the node label if it's necesary
                        if node_name[-1] == 'z':    
                            nodes_info[0][0] = 'a'
                            nodes_info[0][1] += 1
                        else:    
                            nodes_info[0][0] = chr(ord(nodes_info[0][0]) + 1)
                        break
                
                if not repeated_name:
                    break
            
            # Getting a unique node id
            node_id = str(uuid.uuid1())

            # Adding the node to the graph_elements
            node = {'data': {'id': node_id, 'label': node_name, 'positive_degree':0, 'negative_degree':0},
                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)}}
            
            graph_elements['nodes'].append(node)

            # Adding the node to the node_degrees_table
            nodes_degrees_table_children.append(html.Tr([
                html.Td(node_name, style={"text-align":"center"}), 
                html.Td(node['data']['positive_degree'],  style={"text-align":"center"}),
                html.Td(node['data']['negative_degree'],  style={"text-align":"center"}),
            ], className="table-primary")),
                

            # Updating the node label if it's necesary
            if node_name[-1] == 'z':    
                nodes_info[0][0] = 'a'
                nodes_info[0][1] += 1
            else:    
                nodes_info[0][0] = chr(ord(nodes_info[0][0]) + 1)
            
            print("ADD NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes+1, None, number_of_edges, nodes_info, ""
        
        # ----- Edit nodes case -----
        elif btn_triggered == "done-btn-edit-nodes-modal-digraph":

            for children in edit_nodes_modal_body_childrens:
                # Getting the new label
                try:
                    new_label = children['props']['children'][1]['props']['children'][1]['props']['value']
                except:
                    continue
                
                # Getting the current label
                current_label = children['props']['children'][0]['props']['children'][1]['props']['children']

                # Do nothing if new label == current label
                if new_label == current_label:
                    continue

                # Checking if the new label is repeated or not
                repeated_label = False
                for node in graph_elements['nodes']:
                    if node['data']['label'] == new_label:
                        repeated_label = True
                        break
                if repeated_label:
                    continue
                
                # Editing the node in graph_elements
                for node in graph_elements['nodes']:
                    if node['data']['label'] == current_label:
                        node['data']['label'] = new_label
                        break
                
                # Editing edges in graph_elements and edges_info
                for edge in graph_elements['edges']:
                    # Editing edges elements
                    if edge['data']['source_node'] == current_label:
                        edge['data']['source_node'] = new_label
                        
                    if edge['data']['target_node'] == current_label:
                        edge['data']['target_node'] = new_label

                
                # Editing the nodes in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == current_label:
                        children['props']['children'][0]['props']['children'] = new_label
                        break

            print("EDIT NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, nodes_info, ""
        
        # ---- Edit nodes button alert handle -----
        elif btn_triggered == "edit-nodes-btn-digraph":
            alert = None
            print("Selected node data")
            print(selected_node_data)
            if not selected_node_data:
                alert = 1
                print("NADA SELECCIONADO")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""

        # ----- Remove nodes case ------
        elif btn_triggered == "remove-nodes-btn-digraph":
            alert = None
            if selected_node_data:
                # The ids of the nodes to remove are in selected node data
                selected_ids = [selectedNode['id'] for selectedNode in selected_node_data]
                selected_labels = [selectedNode['label'] for selectedNode in selected_node_data]

                # Keeping the non selected nodes in graph_elements['nodes']
                graph_elements['nodes'] = [n for n in graph_elements['nodes'] if n['data']['id'] not in selected_ids]
                # Removing all edges in graph_elements['edges'] if one of their vertices is a selected node
                graph_elements['edges'] = [e for e in graph_elements['edges'] if e['data']['source'] not in selected_ids and e['data']['target'] not in selected_ids]

                #Removing deleted nodes from nodes degrees table
                nodes_degrees_table_children = [c for c in nodes_degrees_table_children if c['props']['children'][0]['props']['children'] not in selected_labels]


                # Updating the degrees of remaining nodes in the nodes degrees table
                degrees = {c['props']['children'][0]['props']['children']:{'positive_degree':0, 'negative_degree':0} for c in nodes_degrees_table_children}

                for edge in graph_elements['edges']:
                    degrees[edge['data']['source_node']]['positive_degree'] += 1
                    degrees[edge['data']['target_node']]['negative_degree'] += 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name]['positive_degree'])
                    c['props']['children'][2]['props']['children'] = str(degrees[node_name]['negative_degree'])

                # Updating number of nodes and number of edges
                number_of_nodes -= len(selected_ids)
                number_of_edges = len(graph_elements['edges'])
            else:
                alert = 2
            
            print("REMOVE NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
        
        # ----- Add Edge case -----
        elif btn_triggered == "add-edge-btn-digraph":
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
                node_label = selected_node_data[0]['label']
                loop_id = str(uuid.uuid1())

                loop = {'data': {'source': node, 
                            'target': node, 'weight': "0", 'id':loop_id, 'source_node':node_label, 'target_node':node_label}}
                graph_elements['edges'].append(loop)

                # Updating the node degree in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == node_label:
                        current_positive_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_positive_degree + 1)
                        current_negative_degree = int(children['props']['children'][2]['props']['children'])
                        children['props']['children'][2]['props']['children'] = str(current_negative_degree + 1)
                        
                        break

                number_of_edges += 1
            # When exactly two nodes are selected (edge)
            elif len(selected_node_data) == 2:

                # Node1 is the source, Node2 is the target
                node1 = selected_node_data[0]['id']
                node2 = selected_node_data[1]['id']

                node1_label = selected_node_data[0]['label']
                node2_label = selected_node_data[1]['label']

                edge_id = str(uuid.uuid1())
                edge = {'data': { 'source': node1, 
                                'target': node2, 'weight': "0", 'id':edge_id, 'source_node':node1_label, 'target_node':node2_label}}
                graph_elements['edges'].append(edge)

                # Updating the node degree in the nodes degrees table
                n_edited_nodes = 0
                for children in nodes_degrees_table_children:
                    # Updating the positive degree of the source node (node1)
                    if children['props']['children'][0]['props']['children'] == node1_label:
                        current_positive_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_positive_degree + 1)
                        n_edited_nodes += 1
                    
                    # Updating the negative degree of the target node
                    if children['props']['children'][0]['props']['children'] == node2_label:
                        current_negative_degree = int(children['props']['children'][2]['props']['children'])
                        children['props']['children'][2]['props']['children'] = str(current_negative_degree + 1)
                        n_edited_nodes += 1
                    
                    if n_edited_nodes == 2:
                        break

                number_of_edges += 1

            print("ADD EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
        
        # ----- Edit edges case -----
        elif btn_triggered == "done-btn-edit-edges-modal-digraph":
            for c in edit_edges_modal_body_childrens:
                # Getting the info of the edges
                
                # First node (source)
                node1 = c['props']['children'][0]['props']['children'][1]['props']['children'][:-1]
                # Second node (target)
                node2 = c['props']['children'][0]['props']['children'][2]['props']['children'][:-1]
                # edge id
                edge_id = c['props']['children'][0]['props']['children'][3]['props']['value']

                # Trying to get a new weight and validate if it is a number
                try:
                    new_weight = c['props']['children'][1]['props']['children'][1]['props']['value']
                    float(new_weight)
                except:
                    new_weight = "Error"
                
                #  Check if we need to change the direction
                try:
                    change_direction = c['props']['children'][1]['props']['children'][2]['props']['checked']
                except:
                    change_direction = False
                
                
                if change_direction:
                    # Swap source and target in the edge and update its weight
                    for edge in graph_elements['edges']:
                        if edge['data']['id'] == edge_id:
                            # Swap the source and target (ids and labels)
                            tmp = edge['data']['source']
                            edge['data']['source'] = edge['data']['target']
                            edge['data']['target'] = tmp

                            tmp = edge['data']['source_node']
                            edge['data']['source_node'] = edge['data']['target_node']
                            edge['data']['target_node'] = tmp

                            # If valid new weight exists, update it
                            if new_weight != "Error":
                                edge['data']['weight'] = new_weight
                            
                            break
                    
                    # Update the degrees of the nodes
                    nodes_updated = 0
                    for node in graph_elements['nodes']:
                        if nodes_updated == 2:
                            break

                        if node['data']['label'] == node1:
                            node['data']['positive_degree'] -= 1
                            node['data']['negative_degree'] += 1
                            nodes_updated += 1
                            continue
                        elif node['data']['label'] == node2:
                            node['data']['positive_degree'] += 1
                            node['data']['negative_degree'] -= 1
                            nodes_updated += 1
                            continue

                    
                    # Update the degrees in the nodes degrees table
                    nodes_updated = 0
                    for c in nodes_degrees_table_children:
                        if nodes_updated == 2:
                            break

                        node_name = c['props']['children'][0]['props']['children'] 
                        positive_degree = c['props']['children'][1]['props']['children']
                        negative_degree = c['props']['children'][2]['props']['children']

                        if node_name == node1:
                            c['props']['children'][1]['props']['children'] = str(int(positive_degree) -1)
                            c['props']['children'][2]['props']['children'] = str(int(negative_degree) + 1)
                            nodes_updated += 1
                            continue
                        elif node_name == node2:
                            c['props']['children'][1]['props']['children'] = str(int(positive_degree) + 1)
                            c['props']['children'][2]['props']['children'] = str(int(negative_degree) - 1)
                            nodes_updated += 1
                            continue
                
                # If we dont need to change the direction of the edge, then just update its weight
                if new_weight != "Error":
                    for edge in graph_elements['edges']:
                        if edge['data']['id'] == edge_id:
                            edge['data']['weight'] = new_weight    
                            break

            print("EDIT EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, nodes_info, ""
        
        # ---- Edit edges button alert handle -----
        elif btn_triggered == "edit-edges-btn-digraph":
            alert = None
            if not selected_edge_data:
                alert = 5
            
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
        
        # ----- Remove edges case -----
        elif btn_triggered == "remove-edges-btn-digraph":
            alert = None
            if not selected_edge_data:
                alert = 6
            else:
                # Getting ids of selected edges
                ids = [e['id'] for e in selected_edge_data]

                # Keeping only the unselected edges in graph_elements
                graph_elements['edges'] = [e for e in graph_elements['edges'] if e['data']['id'] not in ids]

                # Updating the number of edges
                number_of_edges -= len(ids)

                # Updating the degrees of remaining nodes in the nodes degrees table
                degrees = {c['props']['children'][0]['props']['children']: {'positive_degree':int(c['props']['children'][1]['props']['children']), 'negative_degree':int(c['props']['children'][2]['props']['children']),} for c in nodes_degrees_table_children}

                for edge in selected_edge_data:
                    degrees[edge['source_node']]['positive_degree'] -= 1
                    degrees[edge['target_node']]['negative_degree'] -= 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name]['positive_degree'])
                    c['props']['children'][2]['props']['children'] = str(degrees[node_name]['negative_degree'])
            
            print("REMOVE EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
    
        # ----- Upload Graph Case -----
        elif btn_triggered == 'upload-digraph-obj':
            # Read the file and convert it to list of elements
            content_type, content_string = upload_graph_contents.split(',')
            graph = [x.replace(" ", "").split(",") for x in base64.b64decode(content_string).decode('ascii').strip().split("\n") if x] 
            print(graph)

            alert = None
            # Validate the data format
            for element in graph:
                # Just accept edges (a,b) or single nodes (a)
                if len(element) > 3:
                    alert = 7
                    break
                # validate if  weight is a number in case the element is an edge
                if len(element) == 3:
                    try:
                        float(element[2])
                    except:
                        alert = 7
                        break

            
            # If file format is ok, then we proceed to create the graph in the interface
            if not alert:
                # Resetting all variables
                new_nodes = []
                new_edges = []
                number_of_edges = 0
                number_of_nodes = 0
                data_info = ['a', 1]

                # To store nodes degrees and then create the table
                nodes_degrees = {}

                # Check if the elements are nodes or edges and add it to UI and data structure
                for element in graph:
                    element_splitted = element
                    # When it's a single node
                    if len(element_splitted) == 1:
                        # Check if node name is already in use
                        for node in new_nodes:
                            if element_splitted[0] == node['data']['label']:
                                continue
                        
                        # If node doesn't exist, then add it to the new nodes
                        node = {'data': {'id': str(uuid.uuid1()), 'label': element_splitted[0], 'positive_degree':0,'negative_degree':0},
                                         'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)}}
                        new_nodes.append(node)

                        # Adding the node to the degrees dict
                        nodes_degrees[element_splitted[0]] = {'positive_degree':0, 'negative_degree':0}
                        number_of_nodes += 1

                    # When it's an edge
                    else:
                        # To store nodes ids
                        node1_id = None
                        node2_id = None

                        # Check if node1 name is already in use
                        node_already_exists = False
                        for node in new_nodes:
                            if node['data']['label'] == element_splitted[0]:
                                node_already_exists = True
                                node1_id = node['data']['id']
                                break
                        
                        # If node 1 doesn't exists, then add it to the new nodes
                        if not node_already_exists:
                            node1_id = str(uuid.uuid1())
                            node = {'data': {'id': node1_id, 'label': element_splitted[0], 'positive_degree':0, 'negative_degree':0},
                                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                    'positive_degree':0, 'negative_degree':0}
                            new_nodes.append(node)
                            number_of_nodes += 1

                            # Adding it to the degrees dict
                            nodes_degrees[element_splitted[0]] = {'positive_degree':0, 'negative_degree':0}
                        
                        # Check if node2 name is already in use
                        node_already_exists = False
                        for node in new_nodes:
                            if node['data']['label'] == element_splitted[1]:
                                node_already_exists = True
                                node2_id = node['data']['id']
                                break
                        
                        # If node 1 doesn't exists, then add it to the new nodes
                        if not node_already_exists:
                            node2_id = str(uuid.uuid1())
                            node = {'data': {'id': node2_id, 'label': element_splitted[1], 'positive_degree':0, 'negative_degree':0},
                                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                    'positive_degree':0, 'negative_degree':0}
                            new_nodes.append(node)
                            number_of_nodes += 1

                            # Adding it to the degrees dict
                            nodes_degrees[element_splitted[1]] = {'positive_degree':0, 'negative_degree':0}
                        
                        # After nodes managing, add the edge between them
                        edge_id = str(uuid.uuid1())
                        try:
                            weight = element_splitted[2]
                        except:
                            weight = 0

                        edge = {'data': { 'source': node1_id, 
                                'target': node2_id, 'weight': weight, 'id':edge_id, 
                                'source_node':element_splitted[0], 'target_node':element_splitted[1]}}
                        new_edges.append(edge)
                        number_of_edges += 1

                        # Update the edge nodes degrees
                        nodes_degrees[element_splitted[0]]['positive_degree'] += 1
                        nodes_degrees[element_splitted[1]]['negative_degree'] += 1
                
                # Updating the graph elements
                graph_elements['nodes'] = new_nodes
                graph_elements['edges'] = new_edges

                # Creating the table
                nodes_degrees_table_children = []
                for node in nodes_degrees .items():   
                    nodes_degrees_table_children.append(html.Tr(
                        [
                            html.Td(node[0], style={"text-align":"center"}), 
                            html.Td(node[1]['positive_degree'],  style={"text-align":"center"}),
                            html.Td(node[1]['negative_degree'],  style={"text-align":"center"})
                        ], className="table-primary"))
            
            # Clean the upload content so we can upload a diferent file
            upload_graph_contents = ""

            print("READ GRAPH CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
    else:
        return dash.no_update


# ----- Callback to manage "Edit nodes" modal -----
@app.callback(
    [Output("edit-nodes-modal-digraph", "is_open"), Output("edit-nodes-modal-body-digraph", "children")],
    [Input("edit-nodes-btn-digraph", "n_clicks"), Input("cancel-btn-edit-nodes-modal-digraph", "n_clicks"), 
     Input('done-btn-edit-nodes-modal-digraph', 'n_clicks')],
    [State("digraph", "selectedNodeData"), State("edit-nodes-modal-digraph", "is_open")]
)
def toggleModal(edit_nodes_btn, cancel_btn_edit_nodes_modal, done_btn_edit_nodes_modal, 
    selected_node_data, is_modal_open):
    if edit_nodes_btn:
        if not selected_node_data:
            return False, []
        else:
            node_forms = []
            for node in selected_node_data:
                node_label = node['label']
                node_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Current label: ", style={"padding":"1em"}),
                                    dbc.Label(node_label)
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
    [Output("edit-edges-modal-digraph", "is_open"), Output("edit-edges-modal-body-digraph", "children")],
    [Input("edit-edges-btn-digraph", "n_clicks"), Input("cancel-btn-edit-edges-modal-digraph", "n_clicks"), 
     Input('done-btn-edit-edges-modal-digraph', 'n_clicks')],
    [State("digraph", "selectedEdgeData"), State("edit-edges-modal-digraph", "is_open")]
)
def toggleModal(edit_edges_btn, cancel_btn_edit_edges_modal, done_btn_edit_edges_modal, 
    selected_edge_data, is_modal_open):
    if edit_edges_btn:
        if not selected_edge_data:
            return False, []
        else:
            edges_forms = []
            for edge in selected_edge_data:
                node1 = edge['source_node']
                node2 = edge['target_node']
                if node1 != node2:
                    radioButton = dbc.RadioButton()
                    label_change_direction = dbc.Label(f"Change direction", style={"padding":"1em"})
                else:
                    radioButton = None
                    label_change_direction = None

                edges_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Edge ("),
                                    dbc.Label(f"{node1},"),
                                    dbc.Label(f"{node2})"),
                                    dbc.Input(type="hidden", value=edge['id']),
                                    dbc.Label("current weight: ", style={"padding":"1em"}),
                                    dbc.Label(edge['weight']),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("New weight: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text", placeholder="Type the new weight"),
                                    radioButton,
                                    label_change_direction                
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
    [Output('alert-digraph', "children"), Output('alert-digraph', "is_open")],
    Input('alert-info-digraph', 'data')
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
    elif alert_info == 6:
        text = "No edge selected to remove. Please, select at least one edge and try again"
        show = True
    elif alert_info == 7:
        text = "Error. Invalid file format. Please, check it and try again"
        show = True
    return text, show