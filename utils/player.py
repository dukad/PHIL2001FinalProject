import random

UPDATE_RATE_STRATEGY = 0.1
UPDATE_RATE_CONNECTIONS = 0.01

class Player:
    def __init__(self, index, strategy):
        self.strategy = strategy
        self.color = 1
        self.index = index
        self.connections = set()

    def connect(self, P):
        # add each other to the connections set
        self.connections.add(P)
        P.connections.add(self)

    def disconnect(self, P):
        if P in self.connections:
            self.connections.remove(P)
            P.connections.remove(self)
        else:
            raise KeyError("Players not connected")
        
    def update(self):
        # if success -- then update
        if random.random() < UPDATE_RATE_STRATEGY:
            # whatever stra
            pass
        if random.random() < UPDATE_RATE_CONNECTIONS:
            # update the player's connections based on
            pass