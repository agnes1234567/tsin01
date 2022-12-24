import random

class Node:
    def __init__(self, id, qa, qr_start):
        self.id = id #Used for debug purposes
        self.qa = qa
        self.qr = qr_start
        self.backlogged = False #Start node at unbacklogged
        self.counter = 0 #Counter for delay
    
    def step(self):
        #Checks for new arrival (new arrival has probability qa)
        has_arrival = random.random() < self.qa 
        if self.backlogged:
            #Increment delay counter
            self.counter += 1
            #Retransmitts with probability qr
            retransmitt = random.random() < self.qr 
            #Dropped is used for detecting arrivals that don't enter the system
            return {"transmission": retransmitt, "dropped": has_arrival} 
        else:
            return {"transmission": has_arrival, "dropped": False}

    def feedback(self, feedback):
        #Recieves feedback from system after transmission attempt
        if feedback == 1: #Success
            self.backlogged = False
            self.counter = 0
        elif feedback == 'e': #Collision
            self.backlogged = True
    
    def update_qr(self, new_qr):
        #Used for psuedo-Bayesian stabilization
        self.qr = new_qr

