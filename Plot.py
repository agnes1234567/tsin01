import matplotlib.pyplot as plt
import numpy as np    

def create_fig(slots, system, fig_name, title):
    fig = plt.figure(fig_name)
    left, right = fig.subplots(nrows=1, ncols=2)
    fig.suptitle(title)

    left.plot(range(0,slots), system.backlogged_by_slot, color='orange')
    left.set_xlabel('Slot')
    left.set_ylabel('Backlogged nodes')
    left.set_xlim(left=0, right=slots)
    left.set_ylim(bottom=0)

    right.plot(range(0,slots), np.cumsum(system.arrivals_by_slot),\
            color='red', label='Total packet arrivals')
    right.plot(range(0,slots), np.cumsum(system.entering_by_slot), \
            color='blue', label='Total packets entering')
    right.plot(range(0,slots), np.cumsum(system.success_in_slot), \
            color='green', label='Total packets leaving')
    
    right.legend(loc="lower right")
    right.set_xlabel('Slot')
    right.set_ylabel('Packets')
    right.set_xlim(left=0, right=slots)
    right.set_ylim(bottom=0)
    
    plt.gcf().set_size_inches(16, 8)

def plot_Q3(slots, system):
    fig_name = 'Q3'
    title = 'Plots for Q3, lambda=1/e and qr=0.01'
    create_fig(slots, system, fig_name, title)

def plot_Q5(slots, system):
    fig_name = 'Q5'
    title = 'Plots for Q5, lambda=1/2 and qr=0.01'
    create_fig(slots, system, fig_name, title)

def plot_Q6(slots, system):
    fig_name = 'Q6'
    title = 'Plots for Q6, lambda=1/e and qr=0.1'
    create_fig(slots, system, fig_name, title)   

def plot_Q4(m, backlogged_by_slot, mean_ps_empirical, mean_ps_theoretical):
    max_backed = max(backlogged_by_slot)

    fig = plt.figure('Q4_1')
    plot1, plot2 = fig.subplots(2,1)

    plot1.set_title('Frequency of each backlog value for system in Q3')
    freq1 = np.histogram(backlogged_by_slot, range(m+2))[0].tolist()
    plot1.bar(range(m+1), freq1)
    plot1.set_xlim(-1,max_backed+1)

    plot2.set_title('Normalized frequency of each backlog value for system in Q3')
    freq2 = np.histogram(backlogged_by_slot, range(m+2), density=True)[0].tolist()
    plot2.bar(range(m+1), freq2)
    plot2.set_xlim(-1,max_backed+1)
    plt.gcf().set_size_inches(16, 8)

    plt.figure('Q4_2')
    plt.title('Probability of success comparison')
    plt.plot([mean_ps_empirical]*(max_backed+1), linestyle='dashed',\
         label=('Empirical mean: '+ str(mean_ps_empirical)))
    plt.plot([mean_ps_theoretical]*(max_backed+1), linestyle='dashed', \
        label=('Theoretical mean: '+ str(mean_ps_theoretical)))
    plt.xlim(-1,max_backed + 1)
    plt.ylim(0,1)

    plt.legend()
    plt.gcf().set_size_inches(16, 8)
    
def plot_Q7(slots, system):
    plt.figure('Q7_1')
    plt.title('True vs estimated backlog using Pseudo-Bayesian stabilization')
    plt.plot(system.n_hat_by_slot, label='Estimated n')
    plt.plot(system.backlogged_by_slot, label='True n')

    plt.xlabel('Slot')
    plt.ylabel('n backlogged nodes')
    plt.xlim(0,slots)
    plt.ylim(bottom=0)
    plt.legend()
    plt.gcf().set_size_inches(16, 8)
    
    plt.figure('Q7_2')
    plt.plot(range(0,slots), np.cumsum(system.arrivals_by_slot),\
            color='red', label='Total packet arrivals')
    plt.plot(range(0,slots), np.cumsum(system.entering_by_slot), \
            color='blue', label='Total packets entering')
    plt.plot(range(0,slots), np.cumsum(system.success_in_slot), \
            color='green', label='Total packets leaving')
    
    plt.legend(loc="lower right")
    plt.xlabel('Slot')
    plt.ylabel('Packets')
    plt.xlim(left=0, right=slots)
    plt.ylim(bottom=0)
    
    plt.gcf().set_size_inches(16, 8)

def plot_Q8(arrival_rates, simulated_avg_delay, theoretical_avg_delay):
    plt.figure('Q8')
    plt.title('Average delay for a successful packet transmission')

    plt.plot(arrival_rates, simulated_avg_delay, linestyle='None', marker='o', \
        label='Empirical')
    plt.plot(arrival_rates, theoretical_avg_delay, linestyle='None', marker='x', \
        label='Theoretical')

    plt.xlabel('Arrival rate')
    plt.ylabel('Average delay')
    plt.legend()
    plt.gcf().set_size_inches(16, 8)

