import random


# PROBE_AND_ADJUST_RATE = 0.1
# RATIO_STRATEGY = 0.5
# RATIO_CONNECTIONS = 1 - RATIO_STRATEGY

class Player:
    def __init__(self, index, strategy):
        self.strategy = strategy
        self.color = 1
        self.index = index
        self.connections = set()
        self.total_payoff = 0
        self.memory = {}

    def connect(self, P):
        # add each other to the connections set
        self.connections.add(P)
        P.connections.add(self)

    def disconnect(self, P):
        if P in self.connections:
            self.connections.remove(P)
        if self in P.connections:
            P.connections.remove(self)
        

    def play_against(self, P, payoffs):
        # self strategy is row, P strategy is column
        return payoffs[self.strategy][P.strategy]
    
    def play_connections(self, payoffs):
        # print("playing connections")
        self.total_payoff = 0
        for conn in self.connections:
            self.total_payoff += (payoff := self.play_against(conn, payoffs))
            # remember how well we did against this player
            self.memory[conn.index] = payoff

    def probe_and_adjust_strategy(self, num_strategies, payoffs):
        # print("probing and adjusting strategy")
        old_strategy = self.strategy
        # randomly try a new strategy
        self.strategy = random.randint(0, num_strategies - 1)
        last_round_payoff = self.total_payoff
        self.total_payoff = 0
        for conn in self.connections:
            self.total_payoff += (payoff := self.play_against(conn, payoffs))
        # if we did better, keep the new strategy
        if self.total_payoff < last_round_payoff:
            # if we did worse, revert to the old strategy
            self.strategy = old_strategy
        else:
            # print('DID BETTER')
            pass

    def probe_and_adjust_connection(self, num_players, payoffs, Players):
        # remove the worst connection
        # print(self.index)
        # print(self.connections)
        # print(self.memory)
        worst_conn = None
        for conn in self.connections:
            # print(conn.index)
            # print(worst_conn.index if worst_conn is not None else None)
            #if memory is empty, set worst_conn to the first connection
            if len(self.memory) == 0:
                worst_conn = conn
            elif conn.index not in self.memory.keys():
                # we have no memory of this connection because someone else added it, lets ignore
                pass
            elif worst_conn is None or self.memory[conn.index] < self.memory[worst_conn.index]:
                worst_conn = conn
        if worst_conn is not None:
            # print("worst conn is at index ", worst_conn.index)
            self.disconnect(worst_conn)
            # now we need to find a new connection
            # pick a random player that is not already connected to us
            new_conn = None
            while new_conn is None or new_conn in self.connections:
                new_conn = Players[random.randint(0, num_players - 1)]
            # connect to the new player
            self.connect(new_conn)
            # print("connecting to new player at index ", new_conn)
            # play against the new player (and all other connections)
            self.total_payoff = 0
            for conn in self.connections:
                self.total_payoff += (payoff := self.play_against(conn, payoffs))
                # remember how well we did against this player
                self.memory[conn.index] = payoff

            # if we did better against the new player than we did against the worst, keep the new connection, else revert back
            if worst_conn.index in self.memory.keys():
                if self.memory[worst_conn.index] > self.memory[new_conn.index]:
                    # print("did worse against the new player")
                    # print(self.memory[worst_conn.index], self.memory[new_conn.index])
                    # if we did worse, revert to the old connection
                    self.disconnect(new_conn)
                    self.connect(worst_conn)
                else:
                    # print("did better against the new player")
                    # print(self.memory[worst_conn.index], self.memory[new_conn.index])
                    pass
                    # if we did better, keep the new connection
            else:
                # print("no memory, keeping new connection")
                # if we did better, keep the new connection
                pass

    def play_round(self, num_strategies, payoffs, num_players, players, probe_rate, strategy_conn_ratio):
        # print("playing round")
        # top level to call other functions once per generation. Will either probe and adjust or play connections normally
        if random.random() < probe_rate:
            # either change strategy or connection
            if random.random() < strategy_conn_ratio:
                self.probe_and_adjust_strategy(num_strategies, payoffs)
            else:
                self.probe_and_adjust_connection(num_players, payoffs, players)
        else:
            self.play_connections(payoffs)