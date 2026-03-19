"""
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import sqrt, cos, sin
"""
ib\            Ibeta|
   \ 120            |
    |----ia         |
   /                |
ic/                 +-------Ialpha
"""

sqrt3 = sqrt(3)

def Clarke(ia, ib, ic) -> tuple:
    """Y to L transformation"""
    ib_ic = (ib -ic)
    Ialpha = ia*(2/3) -(1/3)*(ib_ic)
    Ibeta = (2/sqrt3)*(ib_ic)
    return (Ialpha, Ibeta)

def _Clarke(ia, ib, ic) -> tuple:
    """Y to L transformation, when 0 = ia +ib +ic"""
    Ialpha = ia
    Ibeta = (1/sqrt3)*(ia +2*ib)
    return (Ialpha, Ibeta)

def InvClarke(Ialpha, Ibeta) -> tuple:
    """L to Y transformation"""
    ia = Ialpha
    ib = (-Ialpha +sqrt3*Ibeta) * 0.5
    ic = (-Ialpha -sqrt3*Ibeta) * 0.5
    return (ia, ib, ic)

def Park(Ialpha, Ibeta, theta) -> tuple:
    cosT = cos(theta)
    sinT = sin(theta)
    Id = Ialpha*cosT +Ibeta*sinT
    Iq = Ibeta*cosT -Ialpha*sinT
    return (Id, Iq)

def InvPark(Id, Iq, theta) -> tuple:
    Ibeta, Ialpha = Park(Iq, Id, theta)
    return (Ialpha, Ibeta)

if __name__ == "__main__":
    ia = 1.0
    ib = -0.5
    ic = -0.5
    Ialpha, Ibeta = Clarke(ia, ib, ic)
    iaa, ibb, icc = InvClarke(Ialpha, Ibeta)
    print("\nInvClake(Clarke(ia, ib, ic))")
    print("Ialpha=%.2f, Ibeta=%.2f"%(Ialpha, Ibeta))
    print(ia, iaa)
    print(ib, ibb)
    print(ic, icc)

    Ialpha = 1.0
    Ibeta = 0.0
    theta = 0.0
    Id, Iq = Park(Ialpha, Ibeta, theta)
    Iaa, Ibb = InvPark(Id, Iq, theta)

    print("\nInvPark(Park(Ialpha, Ibeta))")
    print(Ialpha, Iaa)
    print(Ibeta, Ibb)
