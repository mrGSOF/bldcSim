from math import sin
from matLib import rotateV2
from vecLib import addV, addV_bias

def clip(val, Min, Max) -> float:
    if val < Min:
        return Min
    if val > Max:
        return Max
    return val

from ClarkeTransform import clarkeInv

class SVM():
    @staticmethod
    def getCarrier(angle_rad) -> float:
        return -sin(3*angle_rad +pi/2)

    @staticmethod
    def getPhaseNorm(mag, angle_rad, biasGain=0.155) -> list:
        bias = SVM.getCarrier(angle_rad)
        ix, iy = rotateV2(angle_rad, [mag*(1+biasGain-0.01),0])
        ia,ib,ic = addV_bias(clarkeInv(ix, iy), biasGain*bias)
        ia = clip(ia, -1,1)
        ib = clip(ib, -1,1)
        ic = clip(ic, -1,1)
        return ((ia, ib, ic), bias)


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
        svmV, bV = svm.getPhaseNorm(mag=1, angle_rad=ang_r, biasGain=0.155) #< 15.5% increase
        svmPhaseV[frame] = svmV
        svmPP[frame] = svmV[0] -svmV[1]
        bias[frame]   = bV
        sinV, sbV = svm.getPhaseNorm(mag=1, angle_rad=ang_r, biasGain=0.0)
        sinPhaseV[frame] = sinV
        sinPP[frame] = sinV[0] -sinV[1]
        boost[frame] = (svmPP[frame] / sinPP[frame]) -1.0
        angle[frame]  = ang_r
        ang_r += dr
        
    fig, (svmPlt, sinPlt) = plt.subplots(nrows=2, ncols=1)
    svmPlt.set_title('SVM')
    svmPlt.set_ylim(-1, 1)
    svmPlt.plot(angle, svmPhaseV)
    svmPlt.plot(angle, boost)
    #svmPlt.plot(angle, svmPP)
    sinPlt.set_title('SIN')
    sinPlt.set_ylim(-1, 1)
    sinPlt.plot(angle, sinPhaseV)
    #sinPlt.plot(angle, sinPP)
    #plt.plot(angle, bias)
    plt.show()
