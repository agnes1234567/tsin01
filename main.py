import itertools
import math
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
from Slotted_system import Slotted_system
from Stabilized_slotted_system import Stabilized_slotted_system
from Plot import plot_Q3, plot_Q4, plot_Q5, plot_Q6, plot_Q7, plot_Q8
from Theoretical_expressions import avg_delay_slotted, calc_prob_success 

def main():
    #Shared for all simulations
    slots = 1000
    m = 100

    #Set up systems with lambda and qr from Q3, Q5 and Q6
    system_q3 = Slotted_system(m, system_arrival_rate=1/math.e, qr=0.01)
    system_q5 = Slotted_system(m, system_arrival_rate=1/2, qr=0.01)
    system_q6 = Slotted_system(m, system_arrival_rate=1/math.e, qr=0.1)

    #Set up system with lambda=1/e and psuedo-Bayesian for Q7
    system_q7 = Stabilized_slotted_system(m, system_arrival_rate=1/math.e)

    #Set up systems with lambda=(0.05...0.35) and psuedo-Bayesian for Q8
    arrival_rates_q8 = np.round_(np.arange(0.05,0.40,0.05), 3)
    systems_q8 =[Stabilized_slotted_system(m, system_arrival_rate=val) \
        for val in arrival_rates_q8]
    
    #Run simulation for 1000 slots for all systems
    systems = [system_q3, system_q5, system_q6, system_q7] + systems_q8
    for _ in itertools.repeat(None, slots):
        for system in systems:
            system.step()

    #Calculations for Q4
    mean_ps_theoretical = mean(calc_prob_success(100, 0.01, 1/math.e))
    state_occurrences = list(dict.fromkeys(system_q3.backlogged_by_slot))
    state_occurrences.sort()
    mean_ps_empirical = mean([feedback.count(1)/len(feedback)\
        for feedback in [system_q3.feedback_by_state[i] \
            for i in state_occurrences]])
    
    #Calculations for Q8
    theoretical_avg_delay_q8 = [avg_delay_slotted(val) for val in arrival_rates_q8]
    simulated_avg_delay_q8 = [mean(system.delay_by_packet) for system in systems_q8]

    #Plot
    plot_Q3(slots, system_q3)
    plot_Q4(m, system_q3.backlogged_by_slot, mean_ps_empirical, mean_ps_theoretical)
    plot_Q5(slots, system_q5)
    plot_Q6(slots, system_q6)
    plot_Q7(slots, system_q7)
    plot_Q8(arrival_rates_q8, simulated_avg_delay_q8, theoretical_avg_delay_q8)
    
    #Show
    plt.show()

main()



