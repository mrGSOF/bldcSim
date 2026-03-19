"""
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from matLib import MxV, T, DCM_V2

def park(ix, iy, theta_rad) -> list:
    return MxV(DCM_V2(theta), [ix, iy])

def parkInv(id, iq, theta) -> list:
    return MxV(T(DCM_V2(theta)), [id, iq])

if __name__ == "__main__":
    from math import pi
    ix, iy = (0.0, 1.0)
    theta = 0.0
    print("ix: %1.2f, iy: %1.2f, theta_r: %1.2f"%(ix, iy, theta))
    id, iq = park(ix, iy, theta)
    print("id: %1.2f, iq: %1.2f, theta_r: %1.2f"%(id, iq, theta))
    ix, iy = parkInv(id, iq, theta)
    print("ix: %1.2f, iy: %1.2f, theta_r: %1.2f\n"%(ix, iy, theta))

    ix, iy = (0.0, 1.0)
    theta = pi/2 #degToRad(90.0)
    print("ix: %1.2f, iy: %1.2f, theta_r: %1.2f"%(ix, iy, theta))
    id, iq = park(ix, iy, theta)
    print("id: %1.2f, iq: %1.2f, theta_r: %1.2f"%(id, iq, theta))
    ix, iy = parkInv(id, iq, theta)
    print("ix: %1.2f, iy: %1.2f, theta_r: %1.2f"%(ix, iy, theta))
