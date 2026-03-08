#!/usr/bin/python
"""
 * Demo_Demo_BLDC.py
 * Created on: 20 Aug 2025
 * Author:     Guy Soffer
 * Copyright (C) 2025 Guy Soffer
"""
import os
from math import pi
from Data import Data
from GSOF_Cockpit import DualIndicator as BLDC

from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

# Initialise screen.
BG_color = COLOR.DARK
screen_size=(500,500)
pos = (0, 0)
init()
screen = getScreen(screen_size)
fillScreen( screen, COLOR.WHITE )
   
# Initialise Dials.
path = './skin'
background = Text(  screen=screen, pos=pos, size=screen_size, color=BG_color, name='' )
bldc = BLDC.DualIndicator( screen=screen, pos=pos, size=screen_size,
                    bodyImage  = imageLoad('%s/BLDC_stator.png'%path),
                    handAImage = imageLoad('%s/BLDC_rotor.png'%path),
                    handBImage = imageLoad('%s/MagFieldArrow.png'%path),
                    inputAtoDeg = -180/pi,
                    inputBtoDeg = -180/pi,
                    offsetA_deg = 180.0,  #< Rotor position (North points up)
                    offsetB_deg = 0.0,    #< Stator magnetic field (North points right)
                    kp = 1,               #< No display filtering
                  )    

Telemetry = Data()
clock = Clock()

while True:
    ###Loop to update gauges
    newData = Telemetry.getData()
    bldc.update( newData['RX_rotor_rad'], newData['RX_stator_rad'] )
    bldc.draw()
    update()
    clock.tick(Fs=1.0)
