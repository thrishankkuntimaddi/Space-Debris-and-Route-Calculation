import numpy as np
import math
import pandas as pd
from skyfield.api import Loader, EarthSatellite


class CollisionDetection:
    def __init__(self, timestamp, trajectory_equation, rocket_type, launch_sites, launch_coordinates, altitude,
                 altitude_range, orbit_type, time_selected, tle_data_path, collision_threshold=1.0):
        # Define a threshold distance for collision detection (e.g., within 1 kilometer)
        self.collision_threshold = collision_threshold
        self.timestamp = timestamp
        self.trajectory_equation = trajectory_equation
        self.rocket_type = rocket_type
        self.launch_sites = launch_sites
        self.launch_coordinates = launch_coordinates
        self.altitude = altitude
        self.altitude_range = altitude_range
        self.orbit_type = orbit_type
        self.time_selected = time_selected
        self.tle_data = pd.read_csv(tle_data_path)
        self.loader = Loader('~/.skyfield')
        self.ts = self.loader.timescale()

    def rocket_position(self, t):
        try:
            # Replace 't' in the trajectory equations with the actual value of t
            x_equation = self.trajectory_equation['x'].replace('t', str(t))
            y_equation = self.trajectory_equation['y'].replace('t', str(t))
            z_equation = self.trajectory_equation['z'].replace('t', str(t))
            theta_equation = self.trajectory_equation['theta'].replace('t', str(t))

            # Evaluate the equations to get the positions
            x = eval(x_equation.split('=')[1], {'cos': math.cos, 'sin': math.sin, 'exp': math.exp})
            y = eval(y_equation.split('=')[1], {'cos': math.cos, 'sin': math.sin, 'exp': math.exp})
            z = eval(z_equation.split('=')[1], {'cos': math.cos, 'sin': math.sin, 'exp': math.exp})
            theta = eval(theta_equation.split('=')[1], {'cos': math.cos, 'sin': math.sin, 'exp': math.exp})

            # Check for NaN values
            if any(np.isnan([x, y, z])):
                raise ValueError("Rocket position calculation resulted in NaN values.")

            return np.array([x, y, z]), theta
        except Exception as e:
            print(f"Error calculating rocket position at time {t}: {e}")
            return np.array([np.nan, np.nan, np.nan]), np.nan

    def satellite_positions(self, t):
        positions = []
        for index, row in self.tle_data.iterrows():
            try:
                satellite_name = row['Satellite_Number']
                line1 = row['Line1']  # Adjust column names to match your dataset
                line2 = row['Line2']  # Adjust column names to match your dataset

                # Create satellite object
                satellite = EarthSatellite(line1, line2, satellite_name, self.ts)
                time = self.ts.utc(self.timestamp.year, self.timestamp.month, self.timestamp.day, self.timestamp.hour,
                                   self.timestamp.minute, self.timestamp.second + t)
                position = satellite.at(time).position.km

                # Check for NaN values in satellite positions
                if any(np.isnan(position)):
                    raise ValueError(
                        f"Satellite position calculation resulted in NaN values for satellite {satellite_name}.")

                positions.append(position)
            except KeyError:
                print("The TLE dataset must contain 'Line1' and 'Line2' columns for TLE data.")
            except Exception as e:
                print(f"Error calculating satellite position for index {index} at time {t}: {e}")
                positions.append(np.array([np.nan, np.nan, np.nan]))
        return positions

    def calculate_distance(self, position1, position2):
        # Calculate distance between two positions
        if any(np.isnan(position1)) or any(np.isnan(position2)):
            return np.nan
        return np.linalg.norm(position1 - position2)

    def check_collision(self, t):
        # Calculate rocket position
        rocket_pos, rocket_theta = self.rocket_position(t)

        # Calculate satellite positions
        satellite_positions = self.satellite_positions(t)

        # Debugging print to see rocket and satellite positions
        print(f"Time: {t} seconds, Rocket Position: {rocket_pos}, Satellite Positions: {satellite_positions}")

        # Check each satellite position for collision
        for satellite_pos in satellite_positions:
            distance = self.calculate_distance(rocket_pos, satellite_pos)
            if not np.isnan(distance) and distance <= self.collision_threshold:
                return rocket_pos, satellite_pos, distance, True

        return rocket_pos, None, None, False

    def optimize_trajectory(self):
        # Iterate over a range of time to find an optimal trajectory
        time_step = 10  # Example time step in seconds
        for t in range(0, 3600, time_step):  # Iterate over the first hour
            rocket_pos, satellite_pos, distance, collision = self.check_collision(t)
            if not collision:
                # No collision detected, return the optimized trajectory and time
                optimized_trajectory = self.trajectory_equation
                return optimized_trajectory, t

        return None, None


if __name__ == "__main__":
    # Example trajectory equation and timestamp
    timestamp = pd.Timestamp("2024-11-09 12:00:05")  # Slightly adjusted time to induce collision
    trajectory_equation = {
        'x': 'x(t) = 45.964 + 51.6 * t * cos(0.7853981633974483) * cos(0.0)',
        'y': 'y(t) = 63.305 + 51.6 * t * cos(0.7853981633974483) * sin(0.0)',
        'z': 'z(t) = 0.0 + 51.6 * t * sin(0.7853981633974483)',
        'theta': 'theta(t) = 0.7853981633974483 * (1 - exp(-0.1 * t))'
    }
    rocket_type = "Falcon 9"
    launch_sites = ["Cape Canaveral", "Vandenberg"]
    launch_coordinates = (28.5623, -80.5774)
    altitude = 2000
    altitude_range = 500
    orbit_type = "LEO"
    time_selected = "2024-11-09 12:00:00"

    # Path to TLE dataset
    tle_data_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data.csv'

    # Test the collision calculation and optimization
    collision_detector = CollisionDetection(timestamp, trajectory_equation, rocket_type, launch_sites,
                                            launch_coordinates, altitude, altitude_range, orbit_type, time_selected,
                                            tle_data_path, collision_threshold=1.0)
    optimized_trajectory, optimized_time = collision_detector.optimize_trajectory()

    if optimized_trajectory:
        print(f"Optimized Trajectory: {optimized_trajectory}")
        print(f"Optimized Launch Time (seconds after selected time): {optimized_time}")
    else:
        print("No optimized trajectory found within the given time frame.")
