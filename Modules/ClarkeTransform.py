from math import sqrt
from matLib import T, MxV
from vecLib import scaleV

"""
ib\               Iy|
   \ 120            |
    |----ia         |
   /                |
ic/                 +-------Ix
"""

ClarkeMat = [[1.0,    -0.5    ,     -0.5    ],
             [0.0, 0.5*sqrt(3), -0.5*sqrt(3)]]

_2div3 = 2/3
ClarkeInvMat = T(ClarkeMat)
##ClarkeInvMat = [[ClarkeMat[0][0], ClarkeMat[1][0]],
##                [ClarkeMat[0][1], ClarkeMat[1][1]],
##                [ClarkeMat[0][2], ClarkeMat[1][2]]]

def clarke(ia, ib, ic) -> list:
    return scaleV(MxV(ClarkeMat, [ia, ib, ic]), _2div3)

def clarkeInv(ix, iy) -> list:
    return MxV(ClarkeInvMat, [ix, iy])

if __name__ == "__main__":
    i = [1.0, -0.5, -0.5]
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f"%(i[0], i[1], i[2]))
    ix, iy = clarke(*i)
    print("ix: %1.2f, iy: %1.2f"%(ix, iy))
    i1, i2, i3 = clarkeInv(ix, iy)
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f\n"%(i1, i2, i3))

    i = [-0.5, 1.0, -0.5]
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f"%(i[0], i[1], i[2]))
    ix, iy = clarke(*i)
    print("ix: %1.2f, iy: %1.2f"%(ix, iy))
    i1, i2, i3 = clarkeInv(ix, iy)
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f\n"%(i1, i2, i3))

    i = [-0.5, -0.5, 1.0]
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f"%(i[0], i[1], i[2]))
    ix, iy = clarke(*i)
    print("ix: %1.2f, iy: %1.2f"%(ix, iy))
    i1, i2, i3 = clarkeInv(ix, iy)
    print("i1: %1.2f, i2: %1.2f, i2: %1.2f\n"%(i1, i2, i3))
