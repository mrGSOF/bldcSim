"""
 * Data.py
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
from sys import exit
import pygame

class Data():
    """Data source to drive gauges screen"""
    def __init__(self):
        self.frame    = 0
        self.step_rad = 2*pi / 6
        self.phaseV   = [[0, 0, 1],
                         [1, 0, 1],
                         [1, 0, 0],
                         [1, 1, 0],
                         [0, 1, 0],
                         [0, 1, 1]
                        ]
        self.rotor_rad  = 0.0
        self.stator_rad = 0.0
        self.hall       = 0.0

    def getData(self) -> dict:
        """Generate and return new set of data"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting....')
                exit()   # end program.

        # We have data.
        self.frame      += 1
        self.rotor_rad  += self.step_rad         #< Comutation step
        self.stator_rad  = self.rotor_rad +pi/2  #< 90 deg to rotor
        phaseV           = self.phaseV[self.frame%len(self.phaseV)]
        hall             = phaseV

        return {'RX_time':      self.frame,
                'RX_rotor_rad': self.rotor_rad,
                'RX_stator_rad':self.stator_rad,
                'RX_phaseV':    phaseV,
                 'RX_Hall':     hall,
               }
