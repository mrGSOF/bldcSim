## By: Guy Soffer (GSOF) 08/Mac/2026
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = ""
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

"""
Subset of my library for VECTOR (Linear-Algebra) operations without any external depandancies.
I deliberately wrote (most) of the code in functional programming style.
I wrote the code as procedures to simplify migration to C.
"""

from math import atan2, sqrt

def mag2V(V) -> float:
    """ Return the magnitude of a vector """
    dim = len(V)
    if dim == 2:
        return (V[0]**2) +(V[1]**2)
    if dim == 3:
        return (V[0]**2) +(V[1]**2) +(V[2]**2)
    mag2 = 0.0
    for v in V:
        mag2 += v**2
    return mag2

def absV(V) -> float:
    """ Return the magnitude of a vector """
    return sqrt(mag2V(V))

def subV( V1, V2 ) -> list:
    """Add two vectors""" 
    vectorOut = [0]*len(V1)
    for i, (v1, v2) in enumerate(zip(V1, V2)):
        vectorOut[i] = v1 -v2
    return vectorOut

def crossV3( V1, V2 ) -> list:
    """Computes the cross product of two vectors"""
    vectorOut = [0]*3
    vectorOut[0]= (V1[1]*V2[2]) - (V1[2]*V2[1])
    vectorOut[1]= (V1[2]*V2[0]) - (V1[0]*V2[2])
    vectorOut[2]= (V1[0]*V2[1]) - (V1[1]*V2[0])
    return vectorOut

def scaleV( V, scale ):
    """Multiply the vector by a scalar"""
    vectorOut = [0]*len(V)
    for i,v in enumerate(V):
        vectorOut[i] = v*scale
    return vectorOut


def angleV2(V) -> float:
    """ Return the angle of 2D vector """
    return atan2(V[1], V[0])

def polarV2(V) -> float:
    """ Return the polar coordinates of 2D vector """
    return [absV(V), angleV2(V)]
