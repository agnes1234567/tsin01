import math
from Node import Node

class Stabilized_slotted_system:
    def __init__(self, number_of_nodes, system_arrival_rate):
        #Used for pseudo-Bayesian stabilization algorithm
        self.n_hat = 0
        self.qr = 1
        self.system_arrival_rate = system_arrival_rate
        self.n_hat_by_slot = []

        #Set up nodes
        qa = 1 - (math.pow(math.e,(-system_arrival_rate/number_of_nodes)))
        self.nodes = [Node(i, qa, self.qr) \
            for i in range(0,number_of_nodes)]
        
        self.backlogged_by_slot = [] 
        self.arrivals_by_slot = []
        self.entering_by_slot = []
        self.success_in_slot = []

        #Used for average delay calculations
        self.delay_by_packet = []
           
    def step(self):
        #Store number of backlogged nodes for plot
        n_backlogged = len([node for node in self.nodes if node.backlogged])
        self.backlogged_by_slot.append(n_backlogged)
    
        arrivals = 0 
        entering = 0
        
        #Update qr for all nodes
        for node in self.nodes:
            node.update_qr(self.qr)

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
            self.delay_by_packet.append(node.counter) #Store delay for plot
            node.feedback(feedback) #Send feedback=success
        else: #Collision
            feedback = 'e'
            for node in transmitting_nodes:
                node.feedback(feedback) #Send feedback=collision

        #Store success event for plot
        self.success_in_slot.append((1 if feedback==1 else 0))

        #Pseudo-Bayesian stabilization algorithm
        self.update_est_n(feedback)
        self.update_qr()       
        return 

    def update_est_n(self, feedback):
        #Store ^n_k for plot
        self.n_hat_by_slot.append(self.n_hat)

        #Update to ^n_k+1 
        if feedback=='e':
            self.n_hat = self.n_hat + self.system_arrival_rate + (1/(math.e-2))
        else:
            self.n_hat = max(self.system_arrival_rate, \
                self.n_hat + self.system_arrival_rate - 1)

    def update_qr(self):
        #Update qr
        if self.n_hat >= 1:
            self.qr= 1/self.n_hat
        else:
            self.qr = 1