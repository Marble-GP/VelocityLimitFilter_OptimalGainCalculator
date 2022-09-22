from math import pi


class VelocityLimitFilter():
    def __init__(self, v_max, FB_gain, ControlFreq, LPF_CutOffFreq=-1) -> None:
        self.v_max = v_max
        self.FB_gain = FB_gain
        self.Ts = 1.0/ControlFreq
        self.LPF_gain = (2*pi*self.v_max*self.Ts)/(1.0 + 2*pi*self.v_max*self.Ts) if LPF_CutOffFreq < 0 else (2*pi*LPF_CutOffFreq*self.Ts)/(1.0 + 2*pi*LPF_CutOffFreq*self.Ts)
        
        self.output = 0.0
        self.LPF_input_pre = 0.0

    
    def calc(self, x):
        LPF_input = self.LPF_gain*x + (1.0 - self.LPF_gain)*self.output
        self.output += self._limitter((LPF_input - self.LPF_input_pre)/self.Ts - self.FB_gain*(self.output - LPF_input), self.v_max)*self.Ts
        self.LPF_input_pre = LPF_input

        return self.output
    
    def _limitter(self, x, v_lim):
        return v_lim if x > v_lim else (-v_lim if x < -v_lim else x)