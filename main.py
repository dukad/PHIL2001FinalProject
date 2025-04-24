INTERAVAL = 300

import dash
from dash import html, dcc, callback, Output, Input, State
from dash.dependencies import ALL
from utils.sim import Simulation, SimulationParameters
import numpy as np

DEFAULT_CONNECTIONS = 3
DEFAULT_N = 50

parameters = SimulationParameters(
    num_players=DEFAULT_N,
    num_connections=DEFAULT_CONNECTIONS,
    num_strategies=2,
    payoffs=[0, 0],
    percentages=[0, 0]
)

sim = Simulation()
app = dash.Dash(__name__)


@callback(
    Output('network-interval', 'disabled', allow_duplicate=True),
    Output('network-step-store', 'data', allow_duplicate=True),
    Output('network-max-steps', 'data', allow_duplicate=True),
    Input('run-for-button', 'n_clicks'),
    State('run-for-input', 'value'),
    prevent_initial_call=True,
    allow_duplicates=True
)
def start_run_for(n_clicks, num_generations):
    return False, 0, num_generations

@callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Output('network-step-store', 'data', allow_duplicate=True),
    Output('network-interval', 'disabled', allow_duplicate=True),
    Input('network-interval', 'n_intervals'),
    State('network-step-store', 'data'),
    State('network-max-steps', 'data'),
    prevent_initial_call=True,
)
def update_graph(n_intervals, step, max_steps):
    if step >= max_steps:
        return dash.no_update, step, True  # stop interval

    fig = sim.next_generation()
    return fig, step + 1, False

@callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Input('next-gen', 'n_clicks'),
    
    prevent_initial_call=True,
    allow_duplicate=True
)
def next_generation_click(n_clicks):
    print('test')
    return sim.next_generation()

@callback(
    Output('network-graph', 'figure', allow_duplicate=True),
    Input('gen', 'n_clicks'),
    State('num-players', 'value'),
    State('num-connections', 'value'),
    State({"type": "strategy-input", "index": ALL}, "value"),
    State({"type": "strategy-input", "index": ALL}, "id"),
    State({"type": "strategy-percentage", "index": ALL}, "value"),
    State({"type": "strategy-percentage", "index": ALL}, "id"),
    State("num-strategies", "value"),
    State("probe-rate", "value"),
    State("strategy-conn-ratio", "value"),
    # State('num-strategies', 'value')

    prevent_initial_call=True,
    
)
def generate_network(n_clicks, num_players, num_connections, values, ids, percentages, ids2, num_strategies, probe_rate, strategy_conn_ratio):
    if not values:
        print('No values')
        print(values)
        return sim.render_graph()
    if not ids:
        print('No ids')
        print(ids)
        return sim.render_graph()
    
    # print(values)
    # print(ids)
    # print(percentages)
    # print("strategies", num_strategies)
    # format the matrix values to be square with length num_strategies
    matrix = np.zeros((num_strategies, num_strategies))
    # zip the ids and the values, and place the values into the matrix
    for i, id in enumerate(ids):
        # get the row and column from the id
        row, col = id['index'].split('-')
        row = int(row)
        col = int(col)
        # print(row, col)
        # set the value in the matrix
        matrix[row][col] = values[i]
    print(matrix)
    parameters.payoffs = matrix
    parameters.percentages = percentages
    parameters.num_connections = num_connections
    parameters.num_players = num_players
    parameters.num_strategies = num_strategies
    parameters.probe_rate = probe_rate
    parameters.strategy_conn_ratio = strategy_conn_ratio
    sim.update_parameters(parameters)
    # genereate a new network based on number of players and connections
    return sim.render_graph()

@callback(
    Output('strategy-grid', 'children'),
    Input('num-strategies', 'value')
)
def update_strategy_grid(n):
    if not n or n <= 0:
        return []
    if n > 5:
        # show user an error message, and set it to 6
        n = 5
        # change the input to 6
        return [html.Div('# of strategies cannot exceed 5', style={'color': 'red'})]
    


    header_row = [html.Div('', style={'width': '60px'})]  # Empty top-left corner
    for j in range(n):
        header_row.append(html.Div(f'S{j+1}', style={'width': '60px', 'textAlign': 'center'}))

    grid = [html.Div(header_row, style={'display': 'flex', 'marginBottom': '4px'})]

    for i in range(n):
        row = [html.Div(f'S{i+1}', style={'width': '60px', 'textAlign': 'center'})]  # Row label
        for j in range(n):
            row.append(
                dcc.Input(
                    id={'type': 'strategy-input', 'index': f'{i}-{j}'},
                    type='number',
                    style={'width': '60px', 'margin': '2px'},
                    value = 0
                )
            )
        grid.append(html.Div(row, style={'display': 'flex'}))

    header_row2 = [html.Div('', style={'width': '60px'})]  # Empty top-left corner
    for j in range(n):
        header_row2.append(html.Div(f'S{j+1}%', style={'width': '60px', 'textAlign': 'center'}))
    # add a break into the grid
    grid.append(html.Br())
    grid.append(html.Div(header_row2, style={'display': 'flex', 'marginBottom': '4px'}))
    
    # add a input for each column, each labled with strategy percentage
    row = [html.Div(style={'width': '60px', 'textAlign': 'center'})]  # Row label
    for j in range(n):
        #label for the column
        # center

        row.append(
            dcc.Input(
                id={'type': 'strategy-percentage', 'index': f'{j}'},
                type='number',
                style={'width': '60px', 'margin': '2px'},
                value = 1,
                min=0,
            )
        )
    grid.append(html.Div(row, style={'display': 'flex'}))

    # generate a color key (square of color for each strategy in a row)
    color_key = [html.Div('', style={'width': '60px'})]  # Empty top-left corner
    for j in range(n):
        color = SimulationParameters.strategy_to_color(j, dashParam=True)
        color_key.append(
            
            html.Div(
                style={
                    'width': '60px',
                    'height': '20px',
                    'backgroundColor': color,
                    'margin': '2px'
                }
            )
        )
    grid.append(html.Div(color_key, style={'display': 'flex', 'marginBottom': '4px'}))

    # wrap all this info into a SimulationParameters object and update the simulation
    # change parameters # of strategies
    parameters.num_strategies = n
    # pull data from the grid and update the payoffs and percentages
    # create

    return grid




# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })
app.layout = html.Div(
style={
    'display': 'flex',
    'backgroundColor': '#111111',
    'color': 'white',
    'minHeight': '100vh',
    'padding': '0px',
    'margin': '0px'
},
children=[
    # Side panel
    html.Div(
        style={
            'width': '30%',
            'padding': '20px',
            'backgroundColor': '#222222'
            # 'boxShadow': '2px 0 5px rgba(0,0,0,0.3)'
        },
        children=[
            html.H2('Controls', style={'textAlign': 'center'}),
            html.Label('Number of Players', style={'textAlign': 'center'}),
            dcc.Input(id='num-players', type='number', value=DEFAULT_N, style={'width': '100%'}, min=5, max=1000),
            html.Br(),
            html.Label('Starting # of Connections', style={'textAlign': 'center'}),
            dcc.Input(id='num-connections', type='number', value=DEFAULT_CONNECTIONS, style={'width': '100%'}, min=1, max=100),
            html.Br(),
            html.Label('Number of Strategies'),
            dcc.Input(
                id='num-strategies',
                type='number',
                min=1,
                step=1,
                value=2,
                style={'width': '100%'},
                max=5
            ),
            html.Br(),
            html.Div(id='strategy-grid'),
            html.Br(),
            
            html.Button('Generate', id='gen', n_clicks=0, style={'width': '100%'}),
            html.Br(), html.Br(),
            html.Button('Next Generation', id='next-gen', n_clicks=0, style={'width': '100%'}),
            html.Br(), html.Br(),
            html.Div(id='run-for', children=[
            html.Label('Run for (generations)', style={'width': '100%'}),
            html.Br(),
            dcc.Input(
                id='run-for-input',
                type='number',
                min=1,
                step=1,
                value=1,
                style={'width': '40%'},
                max=10000
            ),
            html.Button('Run', id='run-for-button', n_clicks=0, style={'width': '50%', 'margin-left': '10%'}),
            html.Br(), html.Br(),
            html.Label('Probe and Adjust Rate', style={'textAlign': 'center'}),
            dcc.Input(id='probe-rate', type='number', value=0.01, style={'width': '100%'}, min=0, max=1, step=0.001),
            html.Label('Strategy/Connection Ratio', style={'textAlign': 'center', 'width': '50%'}),
            dcc.Input(id='strategy-conn-ratio', type='number', value=0.5, style={'width': '100%'}, min=0, max=1, step=0.001),
        ]),
        dcc.Interval(id='network-interval', interval=INTERVAL, n_intervals=0, disabled=True),
        dcc.Store(id='network-step-store', data=0),
        dcc.Store(id='network-max-steps', data=0),

        ]
    ),

    # Main content (Graph)
    html.Div(
        style={
            'flexGrow': 1,
            'padding': '20px',
            'margin': '0px',
        },
        children=[
            html.H1('Simulation', style={'textAlign': 'center'}),
            dcc.Graph(id='network-graph', figure=sim.render_graph(), config={'displayModeBar': False}),
        ]
    )
]
)
app.run(debug=False)

