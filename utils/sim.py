import networkx as nx
import plotly.graph_objs as go
import random
import numpy as np

from utils.player import Player

class SimulationParameters:
    # basically a wrapper class that the GUI can manipulate and pass all at once to the main simulation class to update
    def __init__(self, num_players, num_connections, num_strategies=0, payoffs=[], percentages=[]): 
        self.num_players = num_players
        self.num_connections = num_connections
        self.num_strategies = num_strategies
        self.payoffs = payoffs
        self.percentages = percentages
        # check to make sure everything is the right dimension
        if len(payoffs) != num_strategies:
            raise ValueError("Payoffs must be the same length as number of strategies")
        if len(percentages) != num_strategies:
            raise ValueError("Percentages must be the same length as number of strategies")
        
    @staticmethod
    def strategy_to_color(strategy: int, dashParam = False):
        match strategy:
            case 0:
                color = (255, 0, 255)  # Magenta
            case 1:
                color = (255, 100, 0)  # Orange
            case 2:     
                color = (255, 255, 0)  # Yellow
            case 3:
                color = (0, 0, 255)  # Blue
            case 4:
                color = (180, 0, 80)  # Maroon
        if dashParam:
            # convert to a string for dash
            return f'rgba({color[0]}, {color[1]}, {color[2]}, 1)'

                

class Simulation: 
    def __init__(self):
        self.conns = 3
        self.N = 50
        self.num_strategies = 2
        self.payoffs = np.zeros((self.num_strategies, self.num_strategies))
        self.percentages = [100 // self.num_strategies for _ in range(self.num_strategies)] # even distribution of strategies
        self.players = {}
        self.graph = nx.random_regular_graph(self.conns, self.N)
        
        # print("ADJ", self.graph._adj)
        # print(" Edges:", self.graph.edges)
        # print("degree", self.graph.degree)

        # print(self.pos)

        self.init_players()

    def update_parameters(self, params: SimulationParameters):
        self.N = params.num_players
        self.conns = params.num_connections
        self.num_strategies = params.num_strategies
        self.payoffs = params.payoffs
        self.percentages = params.percentages
        self.init_players()

    def change_num_players(self, n):
        self.N = n
        self.graph = nx.random_regular_graph(self.conns, self.N)
        self.init_players()

    def change_num_connections(self, c):
        self.conns = c
        self.graph = nx.random_regular_graph(self.conns, self.N)
        self.init_players()

    def init_players(self): 
        self.players = {}

        total = sum(self.percentages) # this should be 100 but no reason to have it be that really
        # almost definitely not the most efficient way to do this
        for node in self.graph.nodes:
            # genearte a random strategy based on the strategy percentages
            if total <= 1:
                rand = total
            else:
                rand = random.randint(0, total - 1)
            # map the random number to a strategy based on the percentages
            strategy = 0
            for i, percent in enumerate(self.percentages):
                if rand < percent:
                    strategy = i
                    break
                else:
                    rand -= percent

            # create a dict of players based on all the created nodes
            self.players[node] = Player(node, strategy)
        for node1, node2 in self.graph.edges:
            self.players[node1].connect(self.players[node2])
            
    def update_graph_object(self):
        # remove all edges and recreate based on separately stored connections (inefficient prolly)
        for edge in self.graph.edges:
            self.graph.remove_edge(edge[0], edge[1])
        # update the local graph object based on new player connections
        self.graph.nodes = self.players.keys()
        # create the edges based on the player connections
        # self.graph.edges = []
        for player in self.players.values():
            for conn in player.connections:
                # check to see if the opposite connection already exists
                if not (conn.index, player.index) in self.graph.edges:
                    # if not, add it
                    self.graph.add_edge(player.index, conn.index)
        # print(self.graph.edges)
        
        # recreate the layout
        self.pos = nx.spring_layout(self.graph, seed=0) # generate positions of nodes based on connections

    def next_generation(self):
        return self.render_graph()
    
    def render_graph(self):
        self.update_graph_object()
        # generate all edges in the graph
        edge_x = []
        edge_y = []
        for edge in self.graph.edges:
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        # put the list of edges into an object
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='gray'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        node_text = []
        for node in self.graph.nodes:
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f'Node {node}')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                # color=[player.strategy for player in self.players.values()], # change this later -- colorizes each node
                color = [SimulationParameters.strategy_to_color(player.strategy, dashParam=True) for player in self.players.values()], # change this later -- colorizes each node
                size=20,
                line=dict(width=2, color='white')
            )
        )

        self.fig = go.Figure(
        data=[edge_trace, node_trace],
        # data = [node_trace],
        layout=go.Layout(
            title='Network Simulation',
            template='plotly_dark',  # Dark mode theme
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600,
            plot_bgcolor='#111111',
            paper_bgcolor='#111111'
            )
        )
        return self.fig

