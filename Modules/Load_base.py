class LoadState():
    def __init__(self, inertia=0.0, viscosity=0.0, friction=0.0, torque=0.0):
        self.inertia = inertia
        self.viscosity = viscosity
        self.friction = friction
        self.torque = torque

class Load_base():
    """"""
    def __init__(self, getInertia=None, getFriction=None, getTorque=None):
        self.getInertia  = getInertia
        self.getFriction = getFriction
        self.getTorque   = getTorque
        
    def step(self, dt) -> dict:
        inertia = self.getInertia(dt) if self.getInertia != None else 0.0
        viscosity, friction = self.getTorue(dt) if self.getTorque != None else (0.0, 0.0)
        torque = self.getTorue(dt) if self.getTorque != None else 0.0
        return LoadState(inertia, viscosity, friction, torque)
