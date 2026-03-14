from Load_base import Load_base, LoadState

class Load_const(Load_base):
    """"""
    def __init__(self, inertia=0.0, viscosity=0.0, friction=0.0, torque=0.0):
        self.inertia   = inertia
        self.viscosity = friction
        self.friction  = friction
        self.torque    = torque
        
    def step(self, dt) -> dict:
        return LoadState(self.inertia, self.viscosity, self.friction, self.torque)
