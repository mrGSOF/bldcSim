#!/usr/bin/python
"""
 * Demo_Demo_BLDC.py
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""
import os, sys
from pathlib import Path
# Add the absolute path of the Modules folder to sys.path
sys.path.append(os.path.join(Path.cwd(), 'Modules'))

from math import pi
from Modules.EM_model import BLDC
from Modules.Controller_openloop import Controller_openloop
from GSOF_Cockpit import DualIndicator as BLDC_VIEW

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


dt = 0.001
#ctrl = Controller_openloop(Type="ideal", dt=dt) #< "step" or "ideal"
#ctrl = Controller_openloop(Type="step_svm", dt=dt) #< "step" or "ideal"
#ctrl = Controller_openloop(Type="step_6com", dt=dt) #< "step" or "ideal"
ctrl = Controller_openloop(Type="step_12com", dt=dt) #< "step" or "ideal"

bldc = BLDC(inertia_kgm2=0.000002, friction_Nm=0.0003, viscosity_Nm_rps=0.00002,
               coilImpedance_Ohm=1.67, Kv_rpm_v=258)

bldcView = BLDC_VIEW.DualIndicator( screen=screen, pos=pos, size=screen_size,
                    bodyImage  = imageLoad('%s/BLDC_stator.png'%path),
                    handAImage = imageLoad('%s/BLDC_rotor.png'%path),
                    handBImage = imageLoad('%s/MagFieldArrow.png'%path),
                    inputAtoDeg = -180/pi,
                    inputBtoDeg = -180/pi,
                    offsetA_deg = 180.0,  #< Rotor position (North points up)
                    offsetB_deg = 0.0,    #< Stator magnetic field (North points right)
                    kp = 1,               #< No display filtering
                  )    

clock = Clock()

while True:
    for i in range(0,5):
        ### Step the controller
        phaseV = ctrl.step()

        ### Step the BLDC motor
        bldc.step( *phaseV, dt=dt )

    ###Loop to update gauges
    bldcView.update( bldc.rotor.theta_rad, bldc.stator.magField_rad )
    bldcView.draw()
    update()
    clock.tick(Fs=100)
