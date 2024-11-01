
from skyfield.api import EarthSatellite, load

class OrbitalDynamics:
    def __init__(self):
        self.positions = []  # Stores calculated positions for TLE objects

    def calculate_positions(self, tle_data, timestamp):
        """
        Calculate the positions and velocities of TLE objects at a given timestamp.
        """
        ts = load.timescale()
        time = ts.utc(*[int(part) for part in timestamp.replace('T', '-').replace(':', '-').split('-') if part.isdigit()])

        positions = []
        for line1, line2 in tle_data:
            satellite = EarthSatellite(line1, line2, "TLE Object", ts)
            position = satellite.at(time)
            positions.append((position.position.km, position.velocity.km_per_s))

        return positions

