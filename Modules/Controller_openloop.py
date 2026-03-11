from vecLib import scaleV

class Controller_openloop():
    def __init__(self, Type="none", dwell=None, V=None, dt=0.001):    
        self.dt = dt
        self.Type = Type

## CW
        self.COMMUTATION_COM = [
                                [0,    None, 1   ], #5
                                [None, 0,    1   ], #2
                                [1,    0,    None], #1
                                [1,    None, 0   ], #4
                                [None, 1,    0   ], #3
                                [0,    1,    None], #0
                                ]
## CCW
##        self.COMMUTATION_COM = [
##                                [0,    1,    None], #0
##                                [None, 1,    0   ], #3
##                                [1,    None, 0   ], #4
##                                [1,    0,    None], #1
##                                [None, 0,    1   ], #2
##                                [0,    None, 1   ], #5
##                                ]

        self.COMMUTATION_SVM = [[0,0,1], #0
                                [1,0,1], #1
                                [1,0,0], #2
                                [1,1,0], #3
                                [0,1,0], #4
                                [0,1,1], #5
                                ]

        if Type == "ideal":
            self.dwell  = 0.08 #< Almost ideal dwell time at each comutation state
            self.V      = 0.2
            self.COMMUTATION = self.COMMUTATION_SVM
        elif Type == "step_com":
            self.dwell  = 0.5 #< Almost ideal dwell time at each comutation state
            self.V      = 2.0
            self.COMMUTATION = self.COMMUTATION_COM
        elif Type == "step_svm":
            self.dwell  = 0.5 #< Almost ideal dwell time at each comutation state
            self.V      = 2.0
            self.COMMUTATION = self.COMMUTATION_SVM
        else:
            self.dwell  = dwell
            self.V      = V
            self.COMMUTATION = self.COMMUTATION_SVM

        self.time = 0
        self.camIdx = 0
        self.dwellEnd = self.dwell

    def print(self):
        print("Controller type: %s"%self.Type)
        print("Dwell time: %d sec"%self.dwell)
        print("Phase voltage: %.2f Volt"%self.V)
        
    def step(self) -> list:
        phaseV = [0,0,0]
        for i, phase in enumerate(self.COMMUTATION[self.camIdx]):
            phaseV[i] = phase
            if phase != None:
                phaseV[i] *= self.V
                
        #phaseV = scaleV(self.COMMUTATION[self.camIdx], self.V)
        if self.time > self.dwellEnd:
            self.dwellEnd += self.dwell
            self.camIdx = (self.camIdx +1)%len(self.COMMUTATION)

        self.time  += self.dt
        return phaseV

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matLib import matrix

    dt = 0.001
    ctrl = Controller_openloop(Type="step_com", dt=dt)
    ctrl.print()
    STEPS  = int(6*ctrl.dwell/dt +0.5)
    phaseV = matrix(rows=STEPS, cols=3, val=0)
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        phaseV[frame] = ctrl.step()
        time[frame] = ctrl.time
    plt.plot(time, phaseV)
    plt.show()
