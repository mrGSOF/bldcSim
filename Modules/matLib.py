## By: Guy Soffer (GSOF) 01/Sep/2025
__version__ = "1.0.0"
__author__ = "Guy Soffer"
__copyright__ = ""
__credits__ = [""]
__license__ = ""
__maintainer__ = ""
__email__ = "gsoffer@yahoo.com"
__status__ = "Development"

"""
A subset of my bigger library for MATRIX operations without any external depandancies.
I deliberately wrote (most) of the code in functional programming style.
I wrote the code as procedures to simplify migration to C.
"""

from math import cos, sin

def matrix(rows, cols, val=0) -> list:
    """ Returns the rows by cols matrix M filled with value val """
    M = [0]*rows
    for row in range(0,rows):
        M[row] = [val]*cols
    return M

def zeros(rows, cols) -> list:
    """ Returns the rows by cols zero matrix Z """
    return matrix(rows, cols, val=0)

def DCM_V2(rad) -> list:
    """ Return the 2D rotation matrix """
    cosA = cos(rad)
    sinA = sin(rad)
    return [[cosA,-sinA],[sinA,cosA]]

def rotateV2(rad, V) -> list:
    """Rotate the vector V by rad degrees"""
    return MxV(DCM_V2(rad), V)

def getCol(M, col) -> list:
    """ Returns a copy of column 'col' from the matrix 'M' """
    rows = len(M)
    V = [0]*rows
    for i, row in enumerate(M):
        V[i] = row[col]
    return V

def T(M) -> list:
    """ Returns the transposed Matrix of M """
    rows = len(M)
    try:
        cols = len(M[0])
    except:
        cols = rows
        rows = 1
        M = [M]
    O = [0]*cols
    for i in range(0,cols):
        O[i] = getCol(M,i)
    return O

def MxV(M,V) -> list:
    """
    Return the result of NxM matrix and M vector multiplication
    Matrix structure: M[row][col]
    """
    O = [0]*len(M)
    for r,row in enumerate(M):
        for m,v in zip(row,V):
            O[r] += m*v
    return O
