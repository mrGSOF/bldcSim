"""
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
from svmLib import SVM

class Controller():
    def __init__(self, setBldcPhaseV, getEncoder, encCntToRad, dt=0.001):    
        self.dt = dt
        self.encCntToRad = encCntToRad
        self.getEncoder = getEncoder
        self.setBldcPhaseV = setBldcPhaseV
        self.ctrlV = 0.0

    def setV(self, v):
        self.ctrlV = v

    def step(self, ctrlV=None, dt=1.0) -> None:
        if ctrlV != None:
            self.ctrlV = ctrlV
        rotor_r = self.getEncoder()*self.encCntToRad
        stator_r = (rotor_r -(pi/2.0))%(2*pi)
        phaseV, bias = SVM.getPhase(self.ctrlV, stator_r, biasGain=0.155)
        self.setBldcPhaseV(*phaseV)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matLib import matrix
    from vecLib import polarV2
    from ClarkeTransform import clarke
    _2pi = 2*pi
    
    class BldcMock():
        """  """
        def __init__(self, encCounts=4096):
            self.encCounts = encCounts
            self.rotor_r = 0.0

        def getEncoderCount(self) -> int:
            return int(self.encCounts*self.rotor_r/_2pi +0.5)

        #def getHall(self) -> list:
        #    return self.halls

        def setRotor_r(self, angle_r) -> None:
            self.rotor_r = angle_r

        def setPhaseV(self, va, vb, vc) -> None:
            self.phaseV = (va, vb, vc)

        def getField(self) -> list:
            B_abc = self.phaseV
            self.magField = clarke(*B_abc) #< Bxy
            return polarV2(self.magField)

        def print(self):
            print("Encoder: %d"%(self.getEncoderCount()))
            print("Rotor_r: %.2f"%(self.rotor_r))
            print("PhaseV : %s"%(str(self.phaseV)))
            print("Field_r: %.2f"%((self.getField())[1]))
            
    dt = 0.001
    encCounts = 4096
##    bldc = BldcMock(encCounts)
##    ctrl = Controller(setBldcPhaseV = bldc.setPhaseV,
##                      getEncoder    = bldc.getEncoderCount,
##                      encCntToRad   = _2pi/encCounts,
##                      dt=dt
##                      )
##
##    for rad in (0.0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4):
##        bldc.setRotor_r(rad)
##        ctrl.step(ctrlV=1, dt=dt)
##        bldc.print()
##        print("\n")


    from EM_model import BLDC
    from Load_constant import Load_const as Load
    bldc = BLDC(inertia_kgm2=0.000002, friction_Nm=0.0003, viscosity_Nm_rps=0.00002,
                coilImpedance_Ohm=1.67, Kv_rpm_v=258,
                load=Load(inertia=0.0, viscosity=0.0, friction=0.0, torque=0.000),
                #load=Load(inertia=0.01, viscosity=0.0, friction=0.0, torque=0.000),
                encoderLines=encCounts,
                )

    ctrl = Controller(setBldcPhaseV = bldc.setPhaseV,
                      getEncoder    = bldc.getEncoderCount,
                      encCntToRad   = _2pi/encCounts,
                      dt=dt
                      )

    dt = 0.001
    runTime_s = 2.0
    STEPS  = int((runTime_s/dt) +0.5)
    phaseV = matrix(rows=STEPS, cols=3, val=0)
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        ctrl.step(ctrlV=0.07, dt=dt)
        bldc.step(dt=dt)
        phaseV[frame] = bldc.phaseV
        time[frame] = frame*dt

    plt.plot(time, phaseV)
    plt.show()
