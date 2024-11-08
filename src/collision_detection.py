purpose = '''
inputs: space object, Future position, Future Velocity, co-ordinates(x, y, z) } as a dataset;  Trajectory equations utilising timestamp as main source 
outputs: 

    possibility 1: if collision detected - go to trajectory_optimizer.py
                    i/p: Trajectory Equation, TimeStamp
                    o/p: optimized Trajectory Equation 

                    ƒor more report: calling impact_analysis.py 
                    
    possibility 2: if no collision detected - go to mission_report.py 

'''

import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from preprocessing_tle import create_tle_dataset
import re
import os
from math import cos, sin, exp

class SpaceDebrisCollisionDetector:
    def __init__(self, tle_csv_path, launch_time, trajectory_equation):
        self.df_tle = create_tle_dataset(tle_csv_path)
        self.launch_time = launch_time
        self.trajectory_equation = trajectory_equation
        print("TLE Dataset:")
        # print(self.df_tle.head())

    def parse_trajectory_equation(self, equation, t):
        # Parse the trajectory equation string and evaluate it for the given time t
        equation = equation.split('=')[1].strip()  # Extract the equation part after '='
        equation = re.sub(r'\bt\b', f'({t})', equation)
        try:
            return eval(equation, {"__builtins__": None}, {"cos": cos, "sin": sin, "exp": exp})
        except Exception as e:
            raise ValueError(f"Error evaluating equation '{equation}': {e}")

    def predict_position_velocity(self, tle_row, t):
        # Simple linear prediction using current velocity
        x = tle_row['x'] + tle_row['vx'] * t
        y = tle_row['y'] + tle_row['vy'] * t
        z = tle_row['z'] + tle_row['vz'] * t
        return x, y, z

    def rocket_trajectory(self, current_time):
        # Calculate time in seconds since launch
        delta_t = (current_time - self.launch_time).total_seconds()
        if delta_t < 0:
            raise ValueError("Current time is before the launch time.")

        print(f"Delta time (seconds) since launch: {delta_t}")  # Debugging info

        x = self.parse_trajectory_equation(self.trajectory_equation['x'], delta_t)
        y = self.parse_trajectory_equation(self.trajectory_equation['y'], delta_t)
        z = self.parse_trajectory_equation(self.trajectory_equation['z'], delta_t)
        return x, y, z

    def detect_collision(self, time_horizon=500, threshold=1000):
        collision_detected = False
        for t in range(time_horizon):
            current_time = self.launch_time + timedelta(seconds=t)
            try:
                rocket_pos = self.rocket_trajectory(current_time)
            except ValueError as e:
                print(e)
                continue

            for _, tle_row in self.df_tle.iterrows():
                tle_pos = self.predict_position_velocity(tle_row, t)
                distance = np.sqrt((rocket_pos[0] - tle_pos[0]) ** 2 +
                                   (rocket_pos[1] - tle_pos[1]) ** 2 +
                                   (rocket_pos[2] - tle_pos[2]) ** 2)
                # print(f"Time {current_time}: Distance to object {tle_row['Object_ID']} is {distance:.2f}")  # Debugging info
                if distance < threshold:
                    print(f"Collision detected at time {current_time} with object {tle_row['Object_ID']}")
                    collision_detected = True
                    break
            if collision_detected:
                break
        if not collision_detected:
            print("No Collision detected")

# if __name__ == "__main__":
#     launch_time = datetime(2024, 10, 28, 12, 0, 0)
#     trajectory_equation = {
#         'x': 'x(t) = 13.719 + 98.0 * t * cos(0.7853981633974483) * cos(0.0)',
#         'y': 'y(t) = 80.2304 + 98.0 * t * cos(0.7853981633974483) * sin(0.0)',
#         'z': 'z(t) = 0.0 + 98.0 * t * sin(0.7853981633974483)',
#         'theta': 'theta(t) = 0.7853981633974483 * (1 - exp(-0.1 * t))'
#     }
#     tle_csv_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user/user_tle_dataset.csv'
#     detector = SpaceDebrisCollisionDetector(tle_csv_path, launch_time, trajectory_equation)
#     detector.detect_collision()