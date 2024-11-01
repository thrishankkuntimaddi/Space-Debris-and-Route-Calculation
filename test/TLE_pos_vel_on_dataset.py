# Install required library
# !pip install skyfield

from skyfield.api import load, EarthSatellite
import pandas as pd
import numpy as np

# Load the dataset provided by the user
file_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/2024-10-25--2024-10-26-Actual.csv'
dataset = pd.read_csv(file_path)

# Redefine lists to store converted TLE data
tle_lines_list = []

# Iterate through rows in the dataset and convert them to TLE format
for i in range(0, len(dataset), 2):
    # Extracting Line 1
    if i + 1 < len(dataset):
        line1 = dataset.iloc[i]
        line2 = dataset.iloc[i + 1]

        # Handle NaN values by replacing with appropriate default values
        line1_filled = line1.fillna(0)
        line2_filled = line2.fillna(0)

        # Format line 1
        tle_line1 = f"1 {line1_filled[1]:<5} {line1_filled[2]} {line1_filled[3]} {line1_filled[4]:>10} {line1_filled[5]:>8} {line1_filled[6]:>8} 0 {int(line1_filled[8]):04}"

        # Format line 2
        tle_line2 = f"2 {line2_filled[1]:<5} {line2_filled[2]:>8} {line2_filled[3]:>8} {line2_filled[4]:>8} {line2_filled[5]:>8} {line2_filled[6]:>8} {line2_filled[7]:>11} {int(line2_filled[8]):05}"

        # Append formatted TLE lines
        tle_lines_list.append((tle_line1, tle_line2))

# Load timescale for calculations
ts = load.timescale()

# Iterate through the first few TLE sets and calculate position and velocity
positions = []
velocities = []

for tle_lines in tle_lines_list[:5]:  # Limiting to first 5 sets for demonstration
    line1, line2 = tle_lines
    satellite = EarthSatellite(line1, line2, 'Sample Satellite', ts)

    # Define the time for which to calculate position and velocity
    time = ts.now()  # You can specify a future time here as well

    # Calculate the position and velocity of the satellite
    geometry = satellite.at(time)
    position = geometry.position.km  # Position in kilometers
    velocity = geometry.velocity.km_per_s  # Velocity in km/s

    # Store the results
    positions.append(position)
    velocities.append(velocity)

# Display the calculated positions and velocities
for idx, (pos, vel) in enumerate(zip(positions, velocities)):
    print(f"Satellite {idx + 1} Position (km): {pos}")
    print(f"Satellite {idx + 1} Velocity (km/s): {vel}")
