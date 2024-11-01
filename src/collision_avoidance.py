import numpy as np
from scipy.spatial.distance import euclidean
from skyfield.api import load, EarthSatellite
import pandas as pd
import json


class CollisionDetection:
    def __init__(self, max_altitude, trajectory_equations, tle_file_path="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data_dummy.json", threshold_distance=150.0):
        self.threshold_distance = threshold_distance
        self.max_altitude = max_altitude
        self.trajectory_equations = trajectory_equations
        self.ts = load.timescale()

        # Load TLE dataset from JSON file
        with open(tle_file_path, 'r') as file:
            tle_data = json.load(file)['tle_data']
        self.tle_dataframe = pd.DataFrame(tle_data)

    def theta_transition(self, t):
        # Use the provided theta transition equation
        return eval(self.trajectory_equations['theta'])(t)

    def trajectory(self, t):
        # Use the provided trajectory equations
        theta_value = self.theta_transition(t)
        x = eval(self.trajectory_equations['x'])(t, theta_value)
        y = eval(self.trajectory_equations['y'])(t, theta_value)
        z = eval(self.trajectory_equations['z'])(t, theta_value)
        return np.array([x, y, z])

    def check_collision(self):
        collisions = []

        for index, row in self.tle_dataframe.iterrows():
            line1 = row['line_1']
            line2 = row['line_2']
            satellite = EarthSatellite(line1, line2, f'Satellite_{index}', self.ts)

            # Define the time for which to calculate position
            time = self.ts.now()  # You can specify a future time here as well

            # Calculate the position of the satellite
            geometry = satellite.at(time)
            satellite_position = geometry.position.km  # Position in kilometers

            # Iterate over different times to check for collision
            for t in np.linspace(0, 20, num=200):  # Time range and steps
                rocket_position = self.trajectory(t)
                distance = euclidean(rocket_position, satellite_position)
                altitude = np.linalg.norm(rocket_position)  # Altitude of the rocket

                # Debugging log :
                # print(f"Time: {t:.2f}s, Distance: {distance:.2f} km, Altitude: {altitude:.2f} km")

                # Check if altitude exceeds maximum altitude
                if altitude > self.max_altitude:
                    break

                # Check for collision
                if distance < self.threshold_distance:
                    collisions.append((t, satellite.name, distance))
                    break  # Exit loop if collision is detected

        return collisions


# # Example usage of the module
# if __name__ == "__main__":
#     # Input parameters
#     tle_file_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data_dummy.json'
#     max_altitude = 20000
#     trajectory_equations = {
#         'x': "lambda t, theta: 45.964 + 2800.0 * t * np.cos(theta) * np.cos(0.9005898940290741)",
#         'y': "lambda t, theta: 63.305 + 2800.0 * t * np.cos(theta) * np.sin(0.9005898940290741)",
#         'z': "lambda t, theta: 0.0 + 2800.0 * t * np.sin(theta)",
#         'theta': "lambda t: 0.8726646259971648 * (1 - np.exp(-0.1 * t))"
#     }
#
#     # Create an instance of the CollisionDetection class
#     collision_detector = CollisionDetection(tle_file_path, max_altitude, trajectory_equations)
#
#     # Perform Collision Detection
#     collisions = collision_detector.check_collision()
#
#     # Display the results
#     if collisions:
#         for collision in collisions:
#             t, satellite_name, distance = collision
#             print(f"Collision detected at t={t:.2f}s with {satellite_name} at a distance of {distance:.2f} km.")
#     else:
#         print("No collisions detected.")