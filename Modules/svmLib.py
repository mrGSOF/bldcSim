## By: Guy Soffer (GSOF) 18/Mar/2026
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = ""
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

from math import sin, pi
from matLib import rotateV2
from vecLib import addV, addV_bias
from ClarkeTransform import clarkeInv

def clip(vVal, Min, Max) -> float:
    for i,val in enumerate(vVal):
        if val < Min:
            vVal[i] = Min
        elif val > Max:
            vVal[i] = Max
    return vVal

class SVM():
    @staticmethod
    def getCarrier(angle_rad) -> float:
        return -sin(3*angle_rad +pi/2)

    @staticmethod
    def getPhase(mag, angle_rad, biasGain=0.155) -> list:
        _mag = 0.5*mag
        Bx, By = rotateV2(angle_rad, [_mag*(1+biasGain-0.01),0])
        bias = SVM.getCarrier(angle_rad)
        V = addV_bias(clarkeInv(Bx, By), _mag*(1+biasGain*bias))
        V = clip(V, 0,mag)
        return (V, bias)


if __name__ == "__main__":
    from math import pi
    import matplotlib.pyplot as plt
    from matLib import matrix

    svm = SVM()
    dr  = 0.01
    STEPS     = int(2*pi/dr +0.5)
    svmPhaseV = matrix(rows=STEPS, cols=3, val=0)
    bias      = [0]*STEPS
    svmPP     = [0]*STEPS
    sinPhaseV = matrix(rows=STEPS, cols=3, val=0)
    sinPP     = [0]*STEPS
    boost     = [0]*STEPS
    angle     = [0]*STEPS
    ang_r     = 0.0

    for frame in range(0, STEPS):
        svmV, bV = svm.getPhase(mag=1, angle_rad=ang_r, biasGain=0.155) #< 15.5% increase
        svmPhaseV[frame] = svmV
        svmPP[frame] = svmV[0] -svmV[1]
        bias[frame]   = bV
        sinV, sbV = svm.getPhase(mag=1, angle_rad=ang_r, biasGain=0.0)
        sinPhaseV[frame] = sinV
        sinPP[frame] = sinV[0] -sinV[1]
        boost[frame] = (svmPP[frame] / sinPP[frame]) -1.0
        angle[frame]  = ang_r
        ang_r += dr
        
    fig, (svmPlt, sinPlt) = plt.subplots(nrows=2, ncols=1)
    svmPlt.set_title('SVM')
    svmPlt.set_ylim(0, 1)
    svmPlt.plot(angle, svmPhaseV)
    svmPlt.plot(angle, boost)
    #svmPlt.plot(angle, svmPP)
    sinPlt.set_title('SIN')
    sinPlt.set_ylim(0, 1)
    sinPlt.plot(angle, sinPhaseV)
    #sinPlt.plot(angle, sinPP)
    #plt.plot(angle, bias)
    fig1, (svmPolar, sinPolar) = plt.subplots(nrows=1, ncols=2, subplot_kw={'projection': 'polar'})
    svmPolar.set_rmax(2), svmPolar.set_rmin(0.0)
    svmPolar.plot(angle, svmPP),
    sinPolar.set_rmax(2), sinPolar.set_rmin(0.0)
    sinPolar.plot(angle, sinPP),

    plt.show()
