class Stage():
    """Rocket stage class"""
    def __init__(self, empty_mass, fuel_mass, active_time, drag_coefficient, surface_area, engine, parachute):
        self.empty_mass = empty_mass
        self.fuel_mass = fuel_mass
        self.active_time = active_time
        self.drag_coefficient = drag_coefficient
        self.surface_area = surface_area
        self.engine = engine
        self.parachute = parachute
        
