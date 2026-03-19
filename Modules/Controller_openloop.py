"""
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi, sin, cos
from vecLib import scaleV
from svmLib import SVM

class Controller_openloop():
    def __init__(self, Type="none", dwell=None, V=None, dt=0.001):    
        self.dt = dt
        self.Type = Type

## CW with two phase activation on each step
        self.COMMUTATION_6COM = [
                                #PhsA  PhsB  PhsC 
                                [0,    None, 1   ], #0 P:C->A, H:011
                                [None, 0,    1   ], #1 P:C->B, H:010
                                [1,    0,    None], #2 P:A->B, H:110
                                [1,    None, 0   ], #3 P:A->C, H:100
                                [None, 1,    0   ], #4 P:B->C, H:101
                                [0,    1,    None], #5 P:B->A, H:001
                                ]

## CCW with two phase activation on each step
##        self.COMMUTATION_6COM = [
##                                #PhsA  PhsB  PhsC 
##                                [0,    1,    None], #5
##                                [None, 1,    0   ], #4
##                                [1,    None, 0   ], #3
##                                [1,    0,    None], #2
##                                [None, 0,    1   ], #1
##                                [0,    None, 1   ], #0
##                                ]

## CW with three phase activation on each step
        self.COMMUTATION_6SIN = [
                                [0,0,1], #0
                                [1,0,1], #1
                                [1,0,0], #2
                                [1,1,0], #3
                                [0,1,0], #4
                                [0,1,1], #5
                                ]

## CW with two phase activation on each step
        self.COMMUTATION_12COM = []
        for com,sin in zip(self.COMMUTATION_6COM, self.COMMUTATION_6SIN):
            self.COMMUTATION_12COM.append(com)
            self.COMMUTATION_12COM.append(sin)
##        self.COMMUTATION_12COM = [
##                                #PhsA  PhsB  PhsC 
##                                [0,    None, 1   ], #0 P:C->A, H:011
##                                [0,    0,    1   ], #a P:C->A, H:011
##                                [None, 0,    1   ], #1 P:C->B, H:010
##                                [1,    0,    1   ], #b P:C->B, H:010
##                                [1,    0,    None], #2 P:A->B, H:110
##                                [1,    0,    0   ], #c P:A->B, H:110
##                                [1,    None, 0   ], #3 P:A->C, H:100
##                                [1,    1,    0   ], #d P:A->C, H:100
##                                [None, 1,    0   ], #4 P:B->C, H:101
##                                [0,    1,    0   ], #e P:B->C, H:101
##                                [0,    1,    None], #5 P:B->A, H:001
##                                [0,    1,    1   ], #f P:B->A, H:001
##                                ]

        if Type == "smooth_6sin":
            self.dwell  = 0.08 #< Almost ideal dwell time at each comutation state
            self.V      = 0.2
            self.COMMUTATION = self.COMMUTATION_6SIN
        elif Type == "step_6com":
            self.dwell  = 0.5
            self.V      = 2.0
            self.COMMUTATION = self.COMMUTATION_6COM
        elif Type == "step_12com":
            self.dwell  = 0.3
            self.V      = 2.0
            self.COMMUTATION = self.COMMUTATION_12COM
        elif Type == "step_6sin":
            self.dwell  = 0.5
            self.V      = 2.0
            self.COMMUTATION = self.COMMUTATION_6SIN
        elif Type == "smooth_sin":
            self.dwell  = 0.01
            self.V      = 0.1
            DELTA_DEG   = 5        #< Five degree step resolution
            self.COMMUTATION = [0]*int(360/DELTA_DEG)
            PHASE_RAD = 120*pi/180 #< 120 degrees
            for i, deg in enumerate(range(0,360,DELTA_DEG)):
                phase_r = deg*pi/180
                self.COMMUTATION[i] = [cos(phase_r +2*PHASE_RAD),
                                       cos(phase_r +1*PHASE_RAD),
                                       cos(phase_r +0*PHASE_RAD)]
        elif Type == "smooth_svm":
            self.dwell  = 0.025
            self.V      = 0.1
            DELTA_DEG   = 5        #< Five degree step resolution
            self.COMMUTATION = [0]*int(360/DELTA_DEG)
            PHASE_RAD = 120*pi/180 #< 120 degrees
            for i, deg in enumerate(range(0,360,DELTA_DEG)):
                phase_r = deg*pi/180 -pi
                self.COMMUTATION[i],bias = SVM.getPhase(1.0, phase_r)
        else:
            self.dwell  = dwell
            self.V      = V
            self.COMMUTATION = self.COMMUTATION_6SIN

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
    ctrl = Controller_openloop(Type="smooth_svm", dt=dt)
    ctrl.print()
    STEPS  = int(len(ctrl.COMMUTATION)*ctrl.dwell/dt +0.5)
    phaseV = matrix(rows=STEPS, cols=3, val=0)
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        phaseV[frame] = ctrl.step()
        time[frame] = ctrl.time
    plt.plot(time, phaseV)
    plt.show()
