from VLF import VelocityLimitFilter
import numpy as np
import matplotlib.pyplot as plt

#0: Global J map
#1: Local J map
#2: Several patterns of time response
#3: Standard Time Response
CALC_MODE = 0

K_LPF = 1
k_min,k_max=(1.5,1.7)
K = 1.65

def calc_diff(gain, *args):
    v = args[0]
    t = args[1]
    ramp = args[2]
    signal = args[3]
    vlf = VelocityLimitFilter(v, gain, 1/t[1], LPF_CutOffFreq=K_LPF*v)
    y = []
    for x in signal:
        y.append(vlf.calc(x))

    if CALC_MODE == 2 or CALC_MODE == 3:
        plt.plot(t,ramp,label=f"$f(t)|_{{v={v:.4g}}}$")
        plt.plot(t,y,label=f"$\\tilde{{u}}(t;{gain:.4g})|_{{v={v:.4g}}}$")



    y = np.array(y)
    return np.abs(np.max(y) - 1.0)

if __name__ == "__main__":
    if CALC_MODE == 0 or CALC_MODE == 1 or CALC_MODE == 2:
        V_list = np.logspace(-3, 3, 7)
    else:
        V_list = [1]
    n = 4
    gain_list = []
    for v in V_list:
        t = np.linspace(0,n, n*1000)/v
        u=np.zeros_like(t)
        u[:len(t)//n] = v
        ramp = np.array([np.sum(u[:i])*t[1] for i in range(len(t))])
        signal = np.ones_like(t)
        
        if CALC_MODE == 0:
            gain = np.logspace(-4, 4, 1000)
        elif CALC_MODE == 1:
            gain = np.linspace(k_min*v, k_max*v, 1000)

        if CALC_MODE == 3:
            calc_diff(K*v, v,t,ramp,signal)

        if CALC_MODE == 0 or CALC_MODE == 1:
            y = []
            for g in gain:
                y.append(calc_diff(g, v,t,ramp,signal))
            
            plt.plot(gain, y, label=f"v={v:.4g}")


    plt.legend()
    plt.show()

