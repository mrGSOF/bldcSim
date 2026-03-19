"""
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
from vecLib import subV, scaleV, crossV3, polarV2
from matLib import MxV, rotateV2, getM, putCol, putRow
from ClarkeTransform import clarke, clarkeInv
from Load_base import Load_base

_2pi = 2*pi
def crossV2(V2a, V2b) -> float:
    return (crossV3(list(V2a) +[0], list(V2b) +[0]))[2]

def sign(val) -> int:
    if val < 0.0:
        return -1
    return 1

class Encoder():
    def __init__(self, counts):

        self.counts = counts
        self.radToCounts = counts/_2pi

    def getCount(self, rad) -> int:
        return (rad%_2pi)*self.radToCounts
        
class Hall():
    def __init__(self, location_rad, sector_rad, northHigh=True):
        Max = location_rad +sector_rad
        Min = location_rad -sector_rad
        self.offset = 0
        if (Max > _2pi):
            self.offset -= (Max -_2pi)
        elif (Min < 0):
            self.offset += abs(Min)
        self.max = Max + self.offset
        self.min = Min + self.offset
        self.northHigh = northHigh
        self.state = False
        #print(self.offset*180/pi, self.min*180/pi, self.max*180/pi)

    def _isInRange(self, northAngle) -> bool:
        northAngle = (_2pi +northAngle%(_2pi) +self.offset)%(_2pi)
        if (northAngle > self.min) and (northAngle < self.max):
            #print(f"1:{self.min:.2f}<{northAngle:.2f}<{self.max:.2f}", end="; ")
            return self.northHigh
        #print(f"0:{self.min:.2f}<{northAngle:.2f}<{self.max:.2f}", end="; ")
        return not self.northHigh
        
    def getState(self, northAngle_rad) -> bool:
        self.state = self._isInRange(northAngle_rad)
        return self.state
        
class Rotor():
    def __init__(self, inertia, omega_rps, theta_rad, magField_T=1.0):
        self.inertia       = inertia
        self.magField      = [magField_T, 0.0]
        self.omega_rps_dot = 0.0
        self.omega_rps     = omega_rps
        self.theta_rad     = theta_rad
        
    def getMagField(self) -> list:
        return rotateV2(self.theta_rad, self.magField)
    
    def getState(self) -> list:
        return [self.omega_rps_dot,
                self.omega_rps,
                self.theta_rad]

    def step(self, torque, loadInertia=0.0, dt=1.0) -> list:
        """Update next state values"""
        self.omega_rps_dot = torque / (self.inertia +loadInertia)
        self.theta_rad    += self.omega_rps*dt +0.5*self.omega_rps_dot*dt*dt
        self.omega_rps    += self.omega_rps_dot*dt

    def print(self) -> None:
        print("## ROTOR STATE ##")
        print("omega_rps_dot: %.4f"%self.omega_rps_dot)
        print("omega_rps    : %.4f"%self.omega_rps)
        print("theta-rad    : %.4f"%self.theta_rad)

class Stator():
    def __init__(self, coilImpedance_Ohm):
        self.Z = coilImpedance_Ohm
        Z = self.Z

        ### Iabc = A x Vabc
        self.VtoI_com = [[ 1/2*Z, -1/2*Z, -1/2*Z],
                         [-1/2*Z,  1/2*Z, -1/2*Z],
                         [-1/2*Z, -1/2*Z,  1/2*Z]]

        self.VtoI_sin = [[ 2/3*Z, -1/3*Z, -1/3*Z],
                         [-1/3*Z,  2/3*Z, -1/3*Z],
                         [-1/3*Z, -1/3*Z,  2/3*Z]]

        self.phaseV    = [0,0,0]
        self.calcMagField(*self.phaseV)
        self.phaseBemf = [0,0,0]

    def _calcCurrent(self, va, vb, vc) -> list:
        self.phaseV = [va, vb, vc]
        if None in self.phaseV:
            phaseV = [va, vb, vc]
            offV = [0,0,0]
            offIdx = phaseV.index(None)
            phaseV[offIdx] = 0
            VtoI_com = getM(self.VtoI_com)
            putRow(VtoI_com, offIdx, offV)
            putCol(VtoI_com, offIdx, offV)
            self.phaseA = MxV(VtoI_com, phaseV)
        else:
            self.phaseA = MxV(self.VtoI_sin, self.phaseV)
        return self.phaseA

    def calcMagField(self, va, vb, vc) -> list:
        I_abc = self._calcCurrent(va, vb, vc)
        B_abc = I_abc #<B_abc = scaleV(I_abc, self.AtoT)
        self.magField = clarke(*B_abc) #< Bxy
        self.magField_mag, self.magField_rad = polarV2(self.magField)
        return self.magField

    def getField(self) -> list:
        return self.magField

    def calcBemf(self, rotor, Kv) -> list:
        self.phaseBemf = scaleV(clarkeInv(*rotor.getMagField()), rotor.omega_rps/Kv)
        return self.phaseBemf

    def print(self) -> None:
        V = self.phaseV
        A = self.phaseA
        T = self.magField
        print("## STATOR STATE ##")
        print("Phase (V) (A,B,C): %.4f, %.4f, %.4f"%(V[0], V[1], V[2]))
        print("Phase (A) (A,B,C): %.4f, %.4f, %.4f"%(A[0], A[1], A[2]))
        print("Field (T) (X,Y)  : %.4f, %.4f"%(T[0], T[1]))
        
class BLDC():
    def __init__(self, inertia_kgm2=0.000005, omega_rps=0.0, theta_rad=0.0,
                 friction_Nm=0.1, viscosity_Nm_rps=0.2,
                 coilImpedance_Ohm=1.67, Kv_rpm_v=258,
                 load=Load_base()):
        self.Kv        = Kv_rpm_v*2*pi/60 #< Might belong to the Rotor class
        self.Kt        = 1/Kv_rpm_v
        self.friction  = friction_Nm
        self.viscosity = viscosity_Nm_rps
        self.rotor     = Rotor(inertia_kgm2, omega_rps, theta_rad)
        self.stator    = Stator(coilImpedance_Ohm)
        self.load      = load
        hallSector_rad = 90*pi/180 #< +/-50 deg
        self.hallA     = Hall(180*pi/180, hallSector_rad)
        self.hallB     = Hall(300*pi/180, hallSector_rad)
        self.hallC     = Hall(60*pi/180,  hallSector_rad)
        self.halls     = [False, False, False]
        self._sampleHallState()
        self.encoder   = Encoder(counts=4096)
        
    def step(self, va, vb, vc, dt) -> None:
        """"""
        self._sampleHallState()
        phaseV = [va, vb, vc]
        bemf = self.stator.calcBemf(self.rotor, self.Kv)
        for i,(pv,bv) in enumerate(zip(phaseV,bemf)):
            if pv != None:
                phaseV[i] = pv -bv
        torque = self.Kt * crossV2(self.stator.calcMagField(va, vb, vc), self.rotor.getMagField())
        self._stepRotor(torque, dt)

    def _sampleHallState(self) -> list:
        for i,hall in enumerate((self.hallA, self.hallB, self.hallC)):
            self.halls[i] = hall.getState(self.rotor.theta_rad)
        return self.halls

    def _stepRotor(self, torque, dt) -> None:
        rotor = self.rotor
        ### Combile motor and load parameters
        load = self.load.step(dt)
        viscosity = self.viscosity +load.viscosity
        friction  = self.friction +load.friction
        torque   += load.torque
        
        ### Acount for friction
        torque -= rotor.omega_rps*viscosity
        if (abs(rotor.omega_rps) < 0.01) and (abs(torque) < friction):
            torque = 0.0
            rotor.omega_rps = 0.05
        else:
            torque -= sign(rotor.omega_rps)*friction

        ### Update Rotors next state values
        rotor.step(torque, load.inertia, dt)

    def getBemf(self) -> list:
        return self.stator.phaseBemf()
    
    def getHall(self) -> list:
        return self.halls

    def getEncoderCount(self) -> int:
        return self.encoder.getCount(self.rotor.theta_rad)

    def print(self):
        bldc.stator.print()
        bldc.rotor.print()
        print("\n")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matLib import zeros
    from Controller_openloop import Controller_openloop
    from Load_constant import Load_const as Load
    
    bldc = BLDC(inertia_kgm2=0.000002, friction_Nm=0.0005, viscosity_Nm_rps=0.00002,
                coilImpedance_Ohm=1.67, Kv_rpm_v=258,
                load=Load(inertia=0.0, viscosity=0.0, friction=0.0, torque=0.000)
               )
    bldc.print()

    dt = 0.001
    Type = "smooth_svm" #< "smooth_svm", "smooth_sin", "smooth_6sin", "step_12com", "step_6sin", "step_6com"
    ctrl = Controller_openloop(Type, dt)
    ctrl.print()
    STEPS  = int(2*len(ctrl.COMMUTATION)*ctrl.dwell/dt +0.5)
    stator = [0]*STEPS
    theta  = [0]*STEPS
    omega  = [0]*STEPS
    bemf   = zeros(rows=STEPS, cols=3)
    halls  = zeros(rows=STEPS, cols=3)
    count  = [0]*STEPS
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        ### Step the controller
        phaseV = ctrl.step()

        ### Step the BLDC motor
        bldc.step( *phaseV, dt=dt )
        time[frame]   = ctrl.time
        theta[frame]  = bldc.rotor.theta_rad
        omega[frame]  = bldc.rotor.omega_rps
        stator[frame] = bldc.stator.magField_rad
        bemf[frame]   = bldc.stator.phaseBemf
        hal           = bldc.getHall()
        halls[frame]  = [int(hal[0]) +4, int(hal[1]) +6, int(hal[2]) +8]
        count[frame]  = bldc.getEncoderCount()/1024
    plt.plot(time, theta)
    plt.plot(time, stator)
    plt.plot(time, halls)
    plt.plot(time, count)
    if (Type != "step_6com") and (Type != "step_12com") and (Type != "step_6sin"):
        plt.plot(time, bemf)
        plt.plot(time, omega)
    plt.show()
