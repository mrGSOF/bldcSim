#!/usr/bin/python
"""
 * Demo_Demo_BLDC.py
 * Created on: 8 Mar 2026
 * Author:     Guy Soffer (gsoffer@yahoo.com)
 * Copyright (C) 2026 Guy Soffer
"""
import os, sys
from pathlib import Path
# Add the absolute path of the Modules folder to sys.path
sys.path.append(os.path.join(Path.cwd(), 'Modules'))

from math import pi
from Modules.EM_model import BLDC
from Modules.Load_constant import Load_const as Load
from Modules.Controller_closedloop_svm import Controller
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
encCounts = 4096
_2pi = 2*pi
bldc = BLDC(inertia_kgm2=0.000002, friction_Nm=0.0003, viscosity_Nm_rps=0.00002,
            coilImpedance_Ohm=1.67, Kv_rpm_v=258,
            load=Load(inertia=0.0, viscosity=0.0, friction=0.0, torque=0.000),
            #load=Load(inertia=0.01, viscosity=0.0, friction=0.0, torque=0.000),
            encoderLines=encCounts,
            )

ctrl = Controller(setBldcPhaseV = bldc.setPhaseV,
                  getEncoder    = bldc.getEncoderCount,
                  encCntToRad   = _2pi/encCounts,
                  dt=dt
                  )

bldcView = BLDC_VIEW.DualIndicator( screen=screen, pos=pos, size=screen_size,
                    bodyImage  = imageLoad('%s/BLDC_stator.png'%path),
                    handAImage = imageLoad('%s/BLDC_rotor_2pole.png'%path),
                    handBImage = imageLoad('%s/MagFieldArrow.png'%path),
                    inputAtoDeg = -180/pi,
                    inputBtoDeg = -180/pi,
                    offsetA_deg = 0.0,  #< Rotor position (North points up)
                    offsetB_deg = 0.0,    #< Stator magnetic field (North points right)
                    kp = 1,               #< No display filtering
                  )    

clock = Clock()

while True:
    for i in range(0,5):
        ctrl.step(ctrlV=0.2, dt=dt) #< Step the controller
        bldc.step(dt=dt)            #< Step the BLDC motor
    #print(bldc.getPhaseA())
    #print(bldc.getPhaseBemf())
    ###Loop to update gauges
    bldcView.update( bldc.getRotor_rad(), bldc.getStatorField_rad() )
    bldcView.draw()
    update()
    clock.tick(Fs=100)
