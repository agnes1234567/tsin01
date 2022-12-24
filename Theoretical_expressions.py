import math

def avg_delay_slotted(arrival_rate):
    e_minus_half = (math.e-(1/2))
    e_minus_one = (math.e-1)

    one_minus_lambdae = (1-arrival_rate*math.e)
    e_pwr_lambda_minus_one = (math.pow(math.e, arrival_rate)-1)

    term_one = e_minus_half/one_minus_lambdae
    term_two = e_minus_one*e_pwr_lambda_minus_one/\
        (arrival_rate*(1-e_minus_one*e_pwr_lambda_minus_one))
    return term_one-term_two

def calc_prob_success(m, qr, arrival_rate):
    qa = 1 - (math.pow(math.e,(-arrival_rate/m)))
    res = []
    for n in range(m+1):
        G = (m-n)*qa+n*qr
        res.append(G*math.pow(math.e,(-G)))
    return res