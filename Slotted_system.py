import itertools
from Node import Node
import math

class Slotted_system:
    def __init__(self, number_of_nodes, system_arrival_rate, qr):
        #Set up nodes
        qa = 1 - (math.pow(math.e,(-system_arrival_rate/number_of_nodes)))
        self.nodes = [Node(i, qa, qr) \
            for i in range(0,number_of_nodes)]
        
        self.backlogged_by_slot = [] 
        self.arrivals_by_slot = []
        self.entering_by_slot = []
        self.success_in_slot = []

        #Used for probability of success calculations
        self.feedback_by_state = [[] for _  \
            in itertools.repeat(None, number_of_nodes + 1)]
        
    def step(self):
        #Store number of backlogged nodes for plot
        n_backlogged = len([node for node in self.nodes if node.backlogged])
        self.backlogged_by_slot.append(n_backlogged)

        arrivals = 0 
        entering = 0

        transmitting_nodes = []
        for node in self.nodes:
            events = node.step() #Simulate one slot at node
            if events.get("transmission"): #Node wants to transmitt 
                transmitting_nodes.append(node)
                if not node.backlogged: #Collect data for plots
                    arrivals += 1
                    entering += 1
            if events.get("dropped"): #Collect data for plots
                arrivals += 1

        #Store arrivals and entering for plot
        self.arrivals_by_slot.append(arrivals)
        self.entering_by_slot.append(entering)

        transmissions = len(transmitting_nodes) #Num of transmitting nodes
        if transmissions == 0: #Idle
            feedback = 0
        elif transmissions == 1: #Success
            feedback = 1
            node = transmitting_nodes.pop()
            node.feedback(feedback) #Send feedback=success
        else: #Collision
            feedback = 'e'
            for node in transmitting_nodes:
                node.feedback(feedback) #Send feedback=collision
        
        #Store feedback given number of backlogged
        self.feedback_by_state[n_backlogged].append(feedback)
        #Store success event for plot
        self.success_in_slot.append((1 if feedback==1 else 0))
        return 

