import dash
from dash import html, dcc, callback, Output, Input, State
from utils.sim import Simulation

@callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

@callback(
    Output('network-graph', 'figure'),
    Input('next-gen', 'n_clicks'),
    prevent_initial_call=True
)
def next_generation_click(n_clicks):
    # print('test')
    return sim.next_generation()


@callback(
    Output('strategy-grid', 'children'),
    Input('num-strategies', 'value')
)
def update_strategy_grid(n):
    if not n or n <= 0:
        return []

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
                    style={'width': '60px', 'margin': '2px'}
                )
            )
        grid.append(html.Div(row, style={'display': 'flex'}))

    return grid

if __name__ == "__main__":
    sim = Simulation()
    app = dash.Dash(__name__)
    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })
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
                'width': '20%',
                'padding': '20px',
                'backgroundColor': '#222222'
                # 'boxShadow': '2px 0 5px rgba(0,0,0,0.3)'
            },
            children=[
                html.H2('Controls', style={'textAlign': 'center'}),
                html.Label('Number of Players', style={'textAlign': 'center'}),
                dcc.Input(id='num-players', type='number', value=10, style={'width': '100%'}),
                html.Br(), html.Br(),
                html.Label('Number of Strategies'),
                dcc.Input(
                    id='num-strategies',
                    type='number',
                    min=1,
                    step=1,
                    value=2,
                    style={'width': '100%'}
                ),
                html.Br(), html.Br(),
                html.Div(id='strategy-grid'),
                html.Br(), html.Br(),
                html.Button('Next Generation', id='next-gen', n_clicks=0, style={'width': '100%'}),
                html.Br(), html.Br(),
                html.Div(id='container-button-basic')
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
                html.H1('Network Simulation', style={'textAlign': 'center'}),
                dcc.Graph(id='network-graph', figure=sim.render_graph())
            ]
        )
    ]
)
    app.run(debug=True)
