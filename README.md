# BLDC Motor Simulation
Simple physics simulation of Brush-Less Direct Current (BLDC) motor. Demostrating movement of rotor.
Sit back and enjoy developing your BLDC controller in a fully software simulated enviorement.

## Theory of operation
Excellent tutorial by **Jentzen Lee** is below. It inspired me to write this simulation:\
https://www.youtube.com/playlist?list=PLaBr_WzeIAixidGwqfcrQlwKZX4RZ2E7D

https://www.youtube.com/@jtlee1108

https://guy.soffer.tech/tutorials/bldc-motor-control

## Why?
1. To be an interactive tool and support tutorials on BLDC motor opration.
2. To interact with the controller during development (Software In The Loop). This eliminates the needs for any hardware during early stages of controller develop.

## What does it simulate / demonstrate
- Rotor and stator magnetic fields and interaction.
- Mechanical motion of the rotor.
- Clarke and inverse Clarke transformations.
- Kv, Kt, resistance, phase-voltage, rotor-inertia, viscosity and friction coeficiants.
- Simplified electrical solver for currents in 3-phase half H-bridge acounting for back-emf in the DC domain.
- Hall sensors output.
- Encoder output.
- Support exteranl load and disturbance (currently constant).
- Demonstrate smooth and step movement of the rotor by using various techniques:
    - 6, 12 steps commutation using 2 and 3 active phases.
    - Sinusoidal modulation.
    - Space Vector Modulation SVM.

### Open loop with smooth motion (Sinusoidal 72 steps, 5 deg each)
![alt text](./figures/BLDCopenloopsmooth_SIN.gif "Open loop with smooth SIN motion (72 steps, 5 deg each)")

### Open loop with smooth motion (Sinusoidal 6 steps, 3 active phase)
![alt text](./figures/BLDCopenloopsmooth_6step.gif "Open loop with smooth motion (3 active phase)")

### Open loop with 12 steps commutation (combined 2 and 3 active phase)
![alt text](./figures/BLDCopenloop_12step.gif "Open loop with 12 steps commutation (3 active phase)")

### Open loop with 6 steps commutation (3 active phase)
![alt text](./figures/BLDCopenloop_6step_3phase.gif "Open loop with 6 steps commutation (3 active phase)")

### Open loop with 6 steps commutation (2 active phase)
![alt text](./figures/BLDCopenloop_6step_2phase.gif "Open loop with 6 steps commutation (2 active phase)")

## Future plans
- Configurable number of poles to motor.
- Option to change the external load parameters in run time.
- Read motor parameters from .json file.
- Demonstration of automatic commutation algorithm.
- More examples of controllers such as:
  - Closed-loop 6 step commutation.
  - Closed-loop Field Oriented Control (FOC) with SVM.
  - Closed-loop sensorless 6 step commutation.

Requires Python to run the EM_model (inclues dedicated unit-test). For visual support install pyGame and GSOF_Cockpit as well.

http://python.org/

http://www.pygame.org

https://github.com/mrGSOF/GSOF_Cockpit

## Running instructions
- Install requirements `pip install -r requirements.txt`
- Clone and install GSOF_Cockpit (`pip setup.py`)
- Clone bldcSim
- run `python Demo_BLDC_openloop.py`

Interactive operation isn't supported yet.
