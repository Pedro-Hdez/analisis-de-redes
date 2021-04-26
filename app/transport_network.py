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
algorithms = ["Algorithm 1", "Algorithm 2", "Algorithm 3"]
select_algorithm_dropdown = dcc.Dropdown(
    id='select-algorithm-dropown-network',
    value="Algorithm 1",
    clearable=False,
    options=[ {'label': name, 'value': name} for name in algorithms],
    style={"width":"32em"}
)
# -------------------------------------------------------

# ----- Dash Cytoscape instance to display data structures -----
canvas = cyto.Cytoscape(
            id='network',
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
                        'label': "data(restrictions)"
                    }
                },

                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'text-halign':'center',
                        'text-valign':'center',
                        'width':'30px',
                        'height':'30px'
                    }
                },
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
                   id="edit-nodes-modal-body-network"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-nodes-modal-network", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-nodes-modal-network", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-nodes-modal-network",
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
                   id="edit-edges-modal-body-network"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-edges-modal-network", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-edges-modal-network", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-edges-modal-network",
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
        id='nodes-info-network', data=[['a', 1]] # The first element is the first node name that we will use
    ),
 
    # 1- No nodes selected when edit node button is clicked
    # 2- No nodes selected when remove node button is clicked
    # 3- No nodes selected when add edge button is clicked
    # 4- More than two nodes selected when add edge button is clicked
    dcc.Store(
        id='alert-info-network', data=None
    ),

    # ----- Div to display nodes errors -----
    html.Div(id="edit-nodes-alert-network", children=[]),

    edit_nodes_modal,
    
    edit_edges_modal,

    dbc.Row([
        # Left column
        dbc.Col([
            html.Div([
                dbc.Alert(id="alert-network", is_open=False, dismissable=True, color="warning"),
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
                        dbc.Button("Add", id="add-node-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-nodes-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-nodes-btn-network", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", id="add-edge-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-edges-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-edges-btn-network", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload transport network from file", className="mr-1", color="success"),
                ], id="upload-network-obj")
                
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
                html.H4('Transport Network Information'),

                html.Table([

                    html.Tr([
                        html.Td([
                            html.Label("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-nodes-label-network", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Label("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-edges-label-network", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ])
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                html.H4("Nodes Information"),
            ], justify="center"),

            html.Div([
                dbc.Table([
                
                    # Head of the table
                    html.Thead([
                        html.Tr([
                            html.Th([
                                html.H5("Node", className="text-muted"),   
                            ], style={"text-align":"center", "width":"20%"}),

                            html.Th([
                                html.H5("Positive Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"20%"}),

                            html.Th([
                                html.H5("Negative Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"20%"}),

                            html.Th([
                                html.H5("Min. Restriction", className="text-muted"),   
                            ], style={"text-align":"center", "width":"20%"}),

                            html.Th([
                                html.H5("Max. Restriction", className="text-muted"),   
                            ], style={"text-align":"center", "width":"20%"}),
                        ])
                    ]),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"100%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody(id="nodes-degrees-table-network", children=[])
                ],bordered=False, responsive=False),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
])

# ----- Callback to update the graph -----
@app.callback(
    [Output("network", "elements"), Output("nodes-degrees-table-network", "children"), 
     Output("number-of-nodes-label-network", "children"), Output("alert-info-network", "data"), 
     Output("number-of-edges-label-network", "children"), Output('nodes-info-network', 'data'), 
     Output('upload-network-obj', 'contents')],

    [Input("add-node-btn-network", "n_clicks"), Input("done-btn-edit-nodes-modal-network", "n_clicks"),
     Input("remove-nodes-btn-network", "n_clicks"), Input("edit-nodes-btn-network", "n_clicks"),
     Input("add-edge-btn-network", "n_clicks"), Input("done-btn-edit-edges-modal-network", "n_clicks"),
     Input("edit-edges-btn-network", "n_clicks"), Input('remove-edges-btn-network', 'n_clicks'), 
     Input('upload-network-obj', 'contents')],
    
    [State("network", "elements"), State("nodes-degrees-table-network", "children"), 
     State("number-of-nodes-label-network", "children"), State("edit-nodes-modal-body-network", "children"), 
     State("network", "selectedNodeData"), State("number-of-edges-label-network", "children"), 
     State("edit-edges-modal-body-network", "children"), State("network", "selectedEdgeData"), State('nodes-info-network', 'data')]
)
def updateNetwork(add_node_btn_n_clicks, done_btn_edit_nodes_modal, remove_nodes_btn, edit_nodes_btn,
    add_edge_btn, done_btn_edit_edges_modal, edit_edges_btn, remove_edges_btn, upload_graph_contents,
    graph_elements, nodes_degrees_table_children, number_of_nodes, edit_nodes_modal_body_childrens, 
    selected_node_data, number_of_edges, edit_edges_modal_body_childrens, selected_edge_data, nodes_info):
    # Getting the callback context to know which input triggered this callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        btn_triggered = ctx.triggered[0]['prop_id'].split('.')[0]

        # ----- Add node case -----
        if btn_triggered == "add-node-btn-network":

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
            node = {'data': {'id': node_id, 'label': node_name, 'positive_degree':0, 'negative_degree':0,
                    'min_restriction':0, 'max_restriction':"Inf"},
                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)}}
            
            graph_elements['nodes'].append(node)

            # Adding the node to the node_degrees_table
            nodes_degrees_table_children.append(html.Tr([
                html.Td(node_name, style={"text-align":"center"}), 
                html.Td(node['data']['positive_degree'],  style={"text-align":"center", "width":"20%"}),
                html.Td(node['data']['negative_degree'],  style={"text-align":"center", "width":"20%"}),
                html.Td(node['data']['min_restriction'],  style={"text-align":"center", "width":"20%"}),
                html.Td("Inf",  style={"text-align":"center", "width":"20%"}),
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
        elif btn_triggered == "done-btn-edit-nodes-modal-network":
            # Excluding the H3 elements
            edit_nodes_modal_body_childrens = [c for c in edit_nodes_modal_body_childrens if edit_nodes_modal_body_childrens.index(c) % 2 == 1]

            for children in edit_nodes_modal_body_childrens:
                # Getting the new label
                try:
                    # if exists, get it 
                    new_label = children['props']['children'][0]['props']['children'][3]['props']['value']

                    # Checking if the new label is repeated or not
                    repeated_label = False
                    for node in graph_elements['nodes']:
                        if node['data']['label'] == new_label:
                            repeated_label = True
                            break
                    # If the label is repeated, then keep the current label for the node
                    if repeated_label:
                        new_label = children['props']['children'][0]['props']['children'][1]['props']['children']
                    
                except:
                    # If no new label exists, get the current label as new and current label
                    new_label = children['props']['children'][0]['props']['children'][1]['props']['children']
                
                # Getting the current label
                current_label = children['props']['children'][0]['props']['children'][1]['props']['children']


                # Getting the new min restriction
                try:
                    # if exists, get it
                    new_min_restriction = children['props']['children'][1]['props']['children'][3]['props']['value']
                except:
                    # If doesn't exists, new min restriction will be as same as current min restriction
                    new_min_restriction = children['props']['children'][1]['props']['children'][1]['props']['children']
                
                # Getting the current restriction as number (this always be possible because it is inicially 0)
                current_min_restriction = float(children['props']['children'][1]['props']['children'][1]['props']['children'])

                # validate if new min restriction is a numbrer
                try:
                    # if it is, then cast it to float EXCEPT IF ITS INFINITE
                    new_min_restriction = float(new_min_restriction)
                    if new_min_restriction == math.inf:
                        new_min_restriction = current_min_restriction    
                except:
                    # If it isn't, do new min restriction = current min restriction
                    new_min_restriction = current_min_restriction
                
                

                # Getting the new max restriction
                try:
                    # if exists, get it
                    new_max_restriction = children['props']['children'][2]['props']['children'][3]['props']['value']
                except:
                    # If doesn't exists, new max restriction will be as same as current max restriction
                    new_max_restriction = children['props']['children'][2]['props']['children'][1]['props']['children']
                
                # Getting the current max restriction as number (inicially "Inf")
                current_max_restriction = float(children['props']['children'][2]['props']['children'][1]['props']['children'])
                
                # validate if new max restriction is a numbrer
                try:
                    # if it is, then cast it to float
                    new_max_restriction = float(new_max_restriction)    
                except:
                    # If it isn't, do new min restriction = current min restriction
                    new_max_restriction = current_max_restriction
                
                # Validate if new min restriction is at least 0. If it isn't, then new min restriction
                # will be as same as current min restriction which alway is greater or equal than 0
                # The same will happen if new_min_restriction is greater than new_max_restriction
                if new_min_restriction < 0 or new_min_restriction > new_max_restriction:
                    new_min_restriction = current_min_restriction

                # Validate if new max restriction is equal or greater than min restriction
                # If new max restriction is Inf, then always min restriction is ok
                if new_max_restriction != math.inf:
                    if new_max_restriction < new_min_restriction:
                        new_max_restriction = current_max_restriction

                # Editing the node in graph_elements
                for node in graph_elements['nodes']:
                    if node['data']['label'] == current_label:
                        # Updating the label
                        node['data']['label'] = new_label
                        # Updating the min restriction
                        node['data']['min_restriction'] = new_min_restriction
                        # Updating the max restriction
                        if new_max_restriction == math.inf:
                            node['data']['max_restriction'] = "Inf"
                        else:
                            node['data']['max_restriction'] = new_max_restriction
                        break
            
                # Editing edges in graph_elements (only if node label has changed)
                if new_label != current_label:
                    for edge in graph_elements['edges']:
                        # Editing edges elements
                        if edge['data']['source_node'] == current_label:
                            edge['data']['source_node'] = new_label
                            
                        if edge['data']['target_node'] == current_label:
                            edge['data']['target_node'] = new_label

            
                # Editing the nodes in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == current_label:
                        # Updating the name
                        children['props']['children'][0]['props']['children'] = new_label
                        # Updating the min restriction
                        children['props']['children'][3]['props']['children'] = new_min_restriction
                        # Updating the max restriction
                        if new_max_restriction == math.inf:
                            children['props']['children'][4]['props']['children'] = "Inf"
                        else:
                            children['props']['children'][4]['props']['children'] = new_max_restriction
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
        elif btn_triggered == "edit-nodes-btn-network":
            alert = None
            print("Selected node data")
            print(selected_node_data)
            if not selected_node_data:
                alert = 1
                print("NADA SELECCIONADO")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""

        # ----- Remove nodes case ------
        elif btn_triggered == "remove-nodes-btn-network":
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
        elif btn_triggered == "add-edge-btn-network":
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

                # Restrictions are: [min_restriction, flow, max_restriction, cost]
                loop = {'data': {'source': node, 
                            'target': node, 'restrictions': [0,0,"Inf", 0], 'id':loop_id, 'source_node':node_label, 'target_node':node_label}}
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
                                'target': node2, 'restrictions': [0,0,"Inf", 0], 'id':edge_id, 'source_node':node1_label, 'target_node':node2_label}}
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
        elif btn_triggered == "done-btn-edit-edges-modal-network":
            radio_buttons = [c for c in edit_edges_modal_body_childrens if edit_edges_modal_body_childrens.index(c) % 2 == 0]
            edit_edges_modal_body_childrens = [c for c in edit_edges_modal_body_childrens if c not in radio_buttons]
            
            for r in radio_buttons:
                continue
                # Button checked
                
            
            for c,r in zip(edit_edges_modal_body_childrens, radio_buttons):
                print(c, "\n\n")
                # Getting hidden input Object with edge data
                edge_data = c['props']['children'][0]['props']['children'][0]['props']['value']
                
                #Getting the edge's id
                edge_id = edge_data[0]
                #Getting the edge's source node
                node1 = edge_data[1]
                #Getting the edge's target node
                node2 = edge_data[2]

                # trying to get radio button value to know if we need to chenage edge's direction
                try:
                    change_direction = r['props']['children'][1]['props']['checked']
                except:
                    change_direction = False
                
                # Getting current min restriction
                current_min_restriction = float(c['props']['children'][0]['props']['children'][2]['props']['children'])

                # Trying to get new min restriction 
                try:
                    new_min_restriction = c['props']['children'][0]['props']['children'][4]['props']['value']
                    # Validate if it is a number, not infinite and greater or equal than 0
                    new_min_restriction = float(new_min_restriction)
                    if new_min_restriction == math.inf or new_min_restriction < 0:
                        raise Exception()
                except:
                    # If there isn't new min restriction, or new min restriction is not a number or
                    # it's infinite, or is len than 0, then new min restriction = current min restriction
                    new_min_restriction = current_min_restriction
                
                # Getting current flow
                current_flow = float(c['props']['children'][1]['props']['children'][1]['props']['children'])

                # Trying to get new flow
                try:
                    new_flow = c['props']['children'][1]['props']['children'][3]['props']['value']
                    # Validate if it is a number, not infinite and greater or equal than 0
                    new_flow = float(new_flow)
                    if new_flow == math.inf or new_flow < 0:
                        raise Exception()
                except:
                    # If there isn't new flow, or new flow is not a number or
                    # it's infinite, or is less than 0, then new flow = current flow
                    new_flow = current_flow
                
                # Getting current capacity
                current_capacity = float(c['props']['children'][2]['props']['children'][1]['props']['children'])

                # Trying to get new capacity
                try:
                    new_capacity = c['props']['children'][2]['props']['children'][3]['props']['value']
                    # Validate if it's a number (can be infinite) and if it is greater than 0
                    new_capacity = float(new_capacity)
                    if new_capacity < 0:
                        raise Exception()
                except:
                    # If there isn't new capacity, or new capactity is 
                    # less than 0, then new capacity = current capacity
                    new_capacity = current_capacity
                
                # Getting current cost
                current_cost = float(c['props']['children'][3]['props']['children'][1]['props']['children'])
                
                # Trying to get new cost
                try:
                    new_cost = c['props']['children'][3]['props']['children'][3]['props']['value']
                    # Validate if it's a number (can not be infinite) and if it is greater than 0
                    new_cost = float(new_cost)
                    if new_cost == math.inf:
                        raise Exception()
                except:
                    # If there isn't new cost, or new cost is 
                    # infinite, then new cost = current cost
                    new_cost = current_cost
                
                # Validate min_restriction
                if new_min_restriction > new_capacity:
                    new_min_restriction = current_min_restriction
                
                # Validate new flow
                if new_flow > new_capacity:
                    new_flow = current_flow
                
                # Validate new capacity
                if new_capacity < new_min_restriction or new_capacity < new_flow:
                    new_capacity = current_capacity
                
                # *New cost doesn't need validation since it is independent of others restrictions*
                
                # Change direction if it is needed
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

                            # update restrictions
                            # min restriction
                            edge['data']['restrictions'][0] = new_min_restriction
                            # flow
                            edge['data']['restrictions'][1] = new_flow
                            # capacity
                            if new_capacity == math.inf:
                                edge['data']['restrictions'][2] = "Inf"
                            else:
                                edge['data']['restrictions'][2] = new_capacity
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
                
                # If we dont need to change the direction of the edge, then just update its restrictions
                for edge in graph_elements['edges']:
                    if edge['data']['id'] == edge_id:
                        # min restriction
                        edge['data']['restrictions'][0] = new_min_restriction
                        # flow
                        edge['data']['restrictions'][1] = new_flow
                        # capacity
                        if new_capacity == math.inf:
                            edge['data']['restrictions'][2] = "Inf"
                        else:
                            edge['data']['restrictions'][2] = new_capacity
                        # Cost
                        edge['data']['restrictions'][3] = new_cost
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
        elif btn_triggered == "edit-edges-btn-network":
            alert = None
            if not selected_edge_data:
                alert = 5
            
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, ""
        
        # ----- Remove edges case -----
        elif btn_triggered == "remove-edges-btn-network":
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
        elif btn_triggered == 'upload-network-obj':
            # Read the file and convert it to list of elements
            content_type, content_string = upload_graph_contents.split(',')
            graph = [x.replace(" ", "").split(",") for x in base64.b64decode(content_string).decode('ascii').strip().split("\n") if x] 
            print(graph)

            alert = None
            nodes = [e for e in graph if len(e) == 3]
            edges = [e for e in graph if len(e) == 5]

            # Validate non repetitions in nodes labels
            labels = []
            for n in nodes:
                if n[0] not in labels:
                    labels.append(n[0])
                else:
                    # Repetition in nodes label
                    alert = 11
                    break
            # Validate if each node of an edge exists
            if not alert:
                for e in edges:
                    if e[0] not in labels or e[1] not in labels:
                        # Edge with nonexistent node
                        alert = 12
                        break

            # Validate the data format
            if not alert:
                for element in graph:
                    # Just accept edges: [a,b,min_res,flow,capacity]
                    # or nodes: [a,min_res,max_res]
                    if len(element) != 5 and len(element) != 3: 
                        alert = 7
                        break

                    # Nodes validation
                    if len(element) == 3:
                        # Validate if node restrictions are non negative numbers
                        try:
                            for i in range(1,3):
                                element[i] = float(element[i])
                                if element[i] < 0:
                                    raise Exception()
                        except:
                            # Restrictions aren't numbers or are negative numbers
                            alert = 8 
                            break
                        # Validate min restriction. As max_restriction just need to be greater than min_restriction,
                        # this case will also validate max_restriction
                        if element[1] == math.inf or element[1] > element[2]:
                            # Inconsistent node restrictions
                            alert = 9 
                            break

                    # Edges validation
                    if len(element) == 5:
                        # Validate if node restrictions are non negative numbers
                        try:
                            for i in range(2,5):
                                element[i] = float(element[i])
                                if element[i] < 0:
                                    raise Exception()
                        except:
                            # Restrictions aren't numbers or are negative numbers
                            alert = 8 
                            break

                        # Validate min_restriction
                        if element[2] > element[4]:
                            # Inconsistent edges restrictions
                            alert = 10
                            break
                        
                        # Validate new flow
                        if element[3] > element[4]:
                            alert = 10
                            break
                        
                        # Validate new capacity
                        if element[4] < element[2] or element[4] < element[3]:
                            alert = 10
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
                    # When it's a node
                    if len(element_splitted) == 3:
                        # Check if max restriction is Inf to store it as string
                        if element_splitted[2] == math.inf:
                            element_splitted[2] = 'Inf'

                        # Add it to the new nodes
                        node = {'data': {'id': str(uuid.uuid1()), 'label': element_splitted[0], 'positive_degree':0, 'negative_degree':0,
                                'min_restriction':element_splitted[1], 'max_restriction':element_splitted[2]},
                                'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)}}

                        new_nodes.append(node)

                        # Adding the node to the degrees dict
                        nodes_degrees[element_splitted[0]] = {'positive_degree':0, 'negative_degree':0, 
                                                              'min_restriction':element_splitted[1],
                                                              'max_restriction':element_splitted[2]}
                        number_of_nodes += 1

                    # When it's an edge
                    else:
                        # To store nodes ids
                        node1_id = None
                        node2_id = None
                        
                        # add the edge between the nodes

                        # Find the node1 id
                        for n in new_nodes:
                            if n['data']['label'] == element_splitted[0]:
                                node1_id = n['data']['id']
                                break
                        
                        # Find the node2 id
                        for n in new_nodes:
                            if n['data']['label'] == element_splitted[1]:
                                node2_id = n['data']['id']
                                break

                        # Create the edge
                        edge_id = str(uuid.uuid1())
                        # Getting min restriction
                        min_restriction = element_splitted[2]
                        # Getting flow
                        flow = element_splitted[3]
                        # Getting max restriction
                        if element_splitted[4] == math.inf:
                            max_restriction = "Inf"
                        else:
                            max_restriction = element_splitted[4]
                        
                        edge = {'data': { 'source': node1_id, 
                                'target': node2_id, 'restrictions': [min_restriction,flow,max_restriction], 
                                'id':edge_id, 'source_node':element_splitted[0], 
                                'target_node':element_splitted[1]}}

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
                            html.Td(node[1]['negative_degree'],  style={"text-align":"center"}),
                            html.Td(node[1]['min_restriction'],  style={"text-align":"center"}),
                            html.Td(node[1]['max_restriction'],  style={"text-align":"center"})
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
    [Output("edit-nodes-modal-network", "is_open"), Output("edit-nodes-modal-body-network", "children")],
    [Input("edit-nodes-btn-network", "n_clicks"), Input("cancel-btn-edit-nodes-modal-network", "n_clicks"), 
     Input('done-btn-edit-nodes-modal-network', 'n_clicks')],
    [State("network", "selectedNodeData"), State("edit-nodes-modal-network", "is_open")]
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
                node_forms.append(html.H3(f"Node {node_label}"))
                node_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Current label: ", style={"padding":"1em"}),
                                    dbc.Label(node_label),
                                    dbc.Label("New label: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                    
                                    
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                   
                                    dbc.Label("Current Min. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(node['min_restriction']),
                                    dbc.Label("New Min. Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),

                                ]
                            ),

                            dbc.FormGroup(
                                [
                             
                                    dbc.Label("Current Max. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(node['max_restriction']),
                                    dbc.Label("New Max Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ]
                            ),
                            
                        ], inline=True
                    )
                )

            return not is_modal_open, node_forms
    return is_modal_open, []

# ----- Callback to manage "Edit edge" modal -----
@app.callback(
    [Output("edit-edges-modal-network", "is_open"), Output("edit-edges-modal-body-network", "children")],
    [Input("edit-edges-btn-network", "n_clicks"), Input("cancel-btn-edit-edges-modal-network", "n_clicks"), 
     Input('done-btn-edit-edges-modal-network', 'n_clicks')],
    [State("network", "selectedEdgeData"), State("edit-edges-modal-network", "is_open")]
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

                
                edges_forms.append(dbc.FormGroup([
                                                    html.H3(f"Edge({node1},{node2})"),
                                                    radioButton,
                                                    label_change_direction                
                                                ], style={"padding-left":"1em"})
                                    )

                edges_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Input(type="hidden", value=[edge['id'], node1, node2]),
                                    dbc.Label("Current Min. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][0]),
                                    dbc.Label("New Min. Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Flow: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][1]),
                                    dbc.Label("New Flow: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Capacity: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][2]),
                                    dbc.Label("New Capacity: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Cost: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][3]),
                                    dbc.Label("New Cost: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            
                        ],
                        inline=True
                    )
                )
            
            return not is_modal_open, edges_forms

    return is_modal_open, []


# ----- Chained callback to display an alert if it is necesary
@app.callback(
    [Output('alert-network', "children"), Output('alert-network', "is_open")],
    Input('alert-info-network', 'data')
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
    elif alert_info == 8:
        text = "Error. Some restrictions are not numbers, or negative numbers. Please, check it and try again"
        show = True
    elif alert_info == 9:
        text = "Error. Inconsistency in some node restrictions. Please, check it and try again"
        show = True
    elif alert_info == 10:
        text = "Error. Inconsistency in some edge restrictions. Please, check it and try again"
        show = True
    elif alert_info == 11:
        text = "Error. There are some different nodes with same label. Please, check it and try again"
        show = True
    elif alert_info == 12:
        text = "Error. There are some edge from/to nonexistent node. Please, check it and try again"
        show = True
    return text, show