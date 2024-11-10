purpose = '''
inputs: called from orbital_selection.py 
outputs: velocity to reach selected orbit
status: Fully Functional 

Orbital Velocity : It is the velocity needed for an object to stay in a stable orbit at a given altitude.
It is the speed required to balance gravitational pull and avoid falling back to Earth, assuming 
that the object is already at the specified altitude.  
'''

class VelocityCalculate:
    @staticmethod
    def calculate_orbital_velocity(target_orbit):
        """
        Calculates the verlocity required for the rocket to maintain the target orbit.
        """
        G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
        M = 5.972e24  # Mass of Earth, kg
        earth_radius = 6371 * 1000  # Earth's radius in meters
        R = earth_radius + (target_orbit * 1000)  # Convert km to m and add Earth's radius

        # Orbital velocity formula
        velocity = round((G * M / R) ** 0.5, 2)
        return velocity
