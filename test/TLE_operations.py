# Install required library
# !pip install skyfield

from skyfield.api import load, EarthSatellite
import numpy as np

# Example TLE lines (you can replace these with the actual ones from the dataset)
tle_lines = [
    '1 00011U 59001A 24298.83442 0.00001067  00000-0  53894-3 0 9997',
    '2 00011  32.8748 194.9711  1454712 243.8597 100.5343 11.88837969 00000'
]

# Load the TLE data into an EarthSatellite object
line1, line2 = tle_lines
satellite = EarthSatellite(line1, line2, 'Sample Satellite', load.timescale())
earth = load('de421.bsp')["earth"]

# Define the time for which to calculate position and velocity
ts = load.timescale()
time = ts.now()  # You can specify a future time here as well

# Calculate the position and velocity of the satellite
geometry = satellite.at(time)
position = geometry.position.km  # Position in kilometers
velocity = geometry.velocity.km_per_s  # Velocity in km/s

# Print the results
print(f"Position (km): {position}")
print(f"Velocity (km/s): {velocity}")

# Convert position to a 3D coordinate system centered at Earth (0, 0, 0)
eci_coordinates = np.array(position)
print(f"ECI Coordinates: {eci_coordinates}")
