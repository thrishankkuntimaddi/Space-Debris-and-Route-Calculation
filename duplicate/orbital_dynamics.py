class OrbitalDynamics:
    def __init__(self, target_orbit):
        self.target_orbit = target_orbit

    def calculate_orbital_velocity(self):
        """
        Calculates the velocity required for the rocket to maintain the target orbit.
        """
        G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
        M = 5.972e24  # Mass of Earth, kg
        R = self.target_orbit * 1000  # Convert km to m

        # Orbital velocity formula
        velocity = (G * M / R) ** 0.5
        return velocity
