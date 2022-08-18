import numpy as np
import matplotlib.pyplot as plt

def generate_draw():
    nums = np.arange(1,50)
    nums = np.random.permutation(nums)
    draw = nums[:6]
    extra = nums[-1]
    draw = np.append(draw,extra)
    return draw
    #[1,2,3,4,5,6,extra]

def generate_ticket():
    nums = np.arange(1,50)
    nums = np.random.permutation(nums)
    ticket = nums[:6]
    return ticket
    #print(ticket)

def montecarlo_toto(n):
    results = dict(zip(range(0,8),[0]*8))
    for i in range(n):
        dr = generate_draw()
        tick = generate_ticket()
        res = find_group(dr, tick)
        results[res] += 1
    return results

def find_group(drw, tickt):
    drawn = drw[:6]
    extr = drw[-1]
    matches = len(np.intersect1d(drawn, tickt))
    groups_ex = list(range(6,0,-2))
    groups = list(range(7,0,-2))
    if extr in tickt:
        if matches >= 3:
            return groups_ex[matches-3]
        else:   #impossible to match all + extra
            return 0
    else:
        if matches >= 3:
            return groups[matches-3]
        else:
            return 0
    
def montecarlo_plot(res_d):
    n = sum(res_d.values())
    results_freq = res_d
    for k,v in results_freq.items():
        results_freq[k] = v/n
    plt.bar(results_freq.keys(),results_freq.values(),color='g')
    plt.title("TOTO frequency distribution")

