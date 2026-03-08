from vecLib import scaleV

class Controller_openloop():
    def __init__(self, Type="none", dwell=None, V=None, dt=0.001):    
        self.dt = dt
        self.Type = Type
        if Type == "ideal":
            self.dwell  = 0.08 #< Almost ideal dwell time at each comutation state
            self.V      = 0.2
        elif Type == "step":
            self.dwell  = 0.5 #< Almost ideal dwell time at each comutation state
            self.V      = 2.0
        else:
            self.dwell  = dwell
            self.V      = V

        self.CAMUTATION = [[0,0,1],
                           [1,0,1],
                           [1,0,0],
                           [1,1,0],
                           [0,1,0],
                           [0,1,1]]

        self.time = 0
        self.camIdx = 0
        self.dwellEnd = self.dwell

    def print(self):
        print("Controller type: %s"%self.Type)
        print("Dwell time: %d sec"%self.dwell)
        print("Phase voltage: %.2f Volt"%self.V)
        
    def step(self) -> list:
        phaseV = scaleV(self.CAMUTATION[self.camIdx], self.V)
        if self.time > self.dwellEnd:
            self.dwellEnd += self.dwell
            self.camIdx = (self.camIdx +1)%len(self.CAMUTATION)

        self.time  += self.dt
        return phaseV

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matLib import matrix

    dt = 0.001
    ctrl = Controller_openloop(Type="step", dt=dt)
    ctrl.print()
    STEPS  = int(6*ctrl.dwell/dt +0.5)
    phaseV = matrix(rows=STEPS, cols=3, val=0)
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        phaseV[frame] = ctrl.step()
        time[frame] = ctrl.time
    plt.plot(time, phaseV)
    plt.show()
