from math import pi
from vecLib import subV, scaleV, crossV3, polarV2
from matLib import MxV, rotateV2, getM, putCol, putRow
from ClarkeTransform import clarke, clarkeInv

def crossV2(V2a, V2b) -> float:
    return (crossV3(list(V2a) +[0], list(V2b) +[0]))[2]

def sign(val) -> int:
    if val < 0.0:
        return -1
    return 1

class Rotor():
    def __init__(self, inertia, omega_rps, theta_rad, magField_T=1.0):
        self.inertia       = inertia
        self.magField      = [magField_T, 0.0]
        self.omega_rps_dot = 0.0
        self.omega_rps     = omega_rps
        self.theta_rad     = theta_rad
##        ### x[k +1] = Ax[k] +Bu[k]  #< u[k] is Omega_rps_dot
##        self.A = [[0, 1],  #< Omega_rps
##                  [dt,1]]  #< theta_rad
##
##        self.B = [dt,        #< Omega_rps
##                  0.5*dt**2] #< Theta_rad
        
        
    def getMagField(self) -> list:
        return rotateV2(self.theta_rad, self.magField)
    
    def getState(self) -> list:
        return [self.omega_rps_dot,
                self.omega_rps,
                self.theta_rad]

    def step(self, torque, dt) -> list:
        """Update next state values"""
        self.omega_rps_dot = torque / self.inertia
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

        self.VtoI_svm = [[ 1/1.5*Z, -1/3*Z,   -1/3*Z  ],
                         [-1/3*Z,    1/1.5*Z, -1/3*Z  ],
                         [-1/3*Z,   -1/3*Z,    1/1.5*Z]]

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
            self.phaseA = MxV(self.VtoI_svm, self.phaseV)
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
                 coilImpedance_Ohm=1.67, Kv_rpm_v=258):
        self.Kv        = Kv_rpm_v*2*pi/60 #< Might belong to the Rotor class
        self.Kt        = 1/Kv_rpm_v
        self.friction  = friction_Nm
        self.viscosity = viscosity_Nm_rps
        self.rotor     = Rotor(inertia_kgm2, omega_rps, theta_rad)
        self.stator    = Stator(coilImpedance_Ohm)

    def step(self, va, vb, vc, dt) -> None:
        phaseV = [va, vb, vc]
        bemf = self.stator.calcBemf(self.rotor, self.Kv)
        for i,(pv,bv) in enumerate(zip(phaseV,bemf)):
            if pv != None:
                phaseV[i] = pv -bv
        torque = self.Kt * crossV2(self.stator.calcMagField(va, vb, vc), self.rotor.getMagField())
        self._stepRotor(torque, dt)

    def _stepRotor(self, torque, dt) -> None:
        rotor = self.rotor
        ### Calculate next state values
        torque -= rotor.omega_rps*self.viscosity
        if (abs(rotor.omega_rps) < 0.01) and (abs(torque) < self.friction):
            torque = 0.0
            rotor.omega_rps = 0.0
        else:
            torque -= sign(rotor.omega_rps)*self.friction

        ### Update Rotors next state values
        rotor.step(torque, dt)

    def print(self):
        bldc.stator.print()
        bldc.rotor.print()
        print("\n")

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matLib import zeros
    from Controller_openloop import Controller_openloop
    
    bldc = BLDC(inertia_kgm2=0.000002, friction_Nm=0.0005, viscosity_Nm_rps=0.00002,
                coilImpedance_Ohm=1.67, Kv_rpm_v=258)
    bldc.print()

    dt = 0.001
    Type = "step_com" #< "step_svm", "step_com", "ideal"
    ctrl = Controller_openloop(Type, dt)
    ctrl.print()
    STEPS  = int(12*ctrl.dwell/dt +0.5)
    stator = [0]*STEPS
    theta  = [0]*STEPS
    omega  = [0]*STEPS
    bemf   = zeros(rows=STEPS, cols=3)
    time   = [0]*STEPS

    for frame in range(0, STEPS):
        ### Step the controller
        phaseV = ctrl.step()

        ### Step the BLDC motor
        bldc.step( *phaseV, dt=dt )
        time[frame]  = ctrl.time
        theta[frame] = bldc.rotor.theta_rad
        omega[frame] = bldc.rotor.omega_rps
        stator[frame] = bldc.stator.magField_rad
        bemf[frame]  = bldc.stator.phaseBemf


    plt.plot(time, theta)
    plt.plot(time, stator)
    if (Type != "step_com") and (Type != "step_svm"):
        plt.plot(time, bemf)  #< Comment out when in "step" mode
        plt.plot(time, omega) #< Comment out when in "step" mode
    plt.show()
