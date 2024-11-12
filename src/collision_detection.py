import numpy as np
import math
import pandas as pd
import random
from skyfield.api import Loader, EarthSatellite
from skyfield.elementslib import osculating_elements_of
from skyfield.api import Topos


class CollisionDetection:
    def __init__(self, time_selected, trajectory_equation, rocket_type, launch_sites, launch_coordinates, altitude,
                 altitude_range, orbit_type, tle_data_path, collision_threshold=1.0):
        # Define a threshold distance for collision detection (e.g., within 1 kilometer)
        self.collision_threshold = collision_threshold
        self.timestamp = pd.Timestamp(time_selected)
        self.trajectory_equation = trajectory_equation
        self.rocket_type = rocket_type
        self.launch_sites = launch_sites
        self.launch_coordinates = launch_coordinates
        self.altitude = altitude
        self.altitude_range = altitude_range
        self.orbit_type = orbit_type
        self.time_selected = time_selected
        self.tle_data = pd.read_csv(tle_data_path, low_memory=False)
        self.loader = Loader('~/.skyfield')
        self.ts = self.loader.timescale()
        eph = self.loader('de421.bsp')
        self.earth = eph['earth']

        # Parameters for Q-Learning
        self.q_table = {}  # State-action values
        self.actions = [(-0.01, 0), (0, -0.01), (0.01, 0), (0, 0.01)]  # Example trajectory adjustments
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995

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
                # Extract the necessary orbital parameters from the dataset
                inclination = row['Inclination_deg']
                raan = row['RAAN_deg']
                eccentricity = row['Eccentricity'] * 1e-7  # Scale as needed
                arg_perigee = row['Argument_of_Perigee_deg']
                mean_anomaly = row['Mean_Anomaly_deg']
                mean_motion = row['Mean_Motion']

                # Approximate TLE-like data using extracted parameters
                line1 = f'1 {index:05d}U 58002B   {self.timestamp.strftime("%y%j.%f")}  .00000000  00000-0  00000-0 0  9998'
                line2 = f'2 {index:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:7.7f} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f}    99'

                # Create satellite object
                satellite = EarthSatellite(line1, line2, f'Satellite {index}', self.ts)
                time = self.ts.utc(self.timestamp.year, self.timestamp.month, self.timestamp.day, self.timestamp.hour,
                                   self.timestamp.minute, self.timestamp.second + t)
                position = satellite.at(time).position.km

                # Check for NaN values in satellite positions
                if any(np.isnan(position)):
                    raise ValueError(f"Satellite position calculation resulted in NaN values for satellite {index}.")

                positions.append((position, f'Satellite {index}'))
            except KeyError as e:
                print(f"Missing key in dataset: {e}")
            except Exception as e:
                print(f"Error calculating satellite position for index {index} at time {t}: {e}")
                positions.append((np.array([np.nan, np.nan, np.nan]), f'Satellite {index}'))
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

        # Check each satellite position for collision
        for satellite_pos, satellite_id in satellite_positions:
            distance = self.calculate_distance(rocket_pos, satellite_pos)
            if not np.isnan(distance) and distance <= self.collision_threshold:
                print(
                    f"Collision detected at time {t} seconds! Rocket Position: {list(rocket_pos)}, Satellite Position: {list(satellite_pos)}, Distance: {distance}, Satellite ID: {satellite_id}")
                return True, distance

        return False, None

    def choose_action(self, state):
        # Epsilon-greedy policy for action selection
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get,
                       default=random.choice(self.actions))

    def update_q_table(self, state, action, reward, next_state):
        # Update Q-value using the Q-learning update rule
        current_q = self.q_table.get(state, {}).get(action, 0)
        max_future_q = max(self.q_table.get(next_state, {}).values(), default=0)
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (
                    reward + self.discount_factor * max_future_q)
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

    def optimize_trajectory(self):
        # Ask user for episodes, total seconds, and step seconds
        episodes = int(input("Enter the number of episodes for training: "))
        total_seconds = int(input("Enter the total number of seconds to simulate: "))
        step_seconds = int(input("Enter the time step in seconds: "))

        for episode in range(episodes):
            print(f"Starting episode {episode + 1}/{episodes}")
            state = (0, 0, 0)  # Initial state (e.g., t, x_offset, y_offset)
            total_reward = 0

            # Track cumulative adjustments
            x_cumulative_adjust = 0
            y_cumulative_adjust = 0

            for t in range(0, total_seconds, step_seconds):
                print(f"Time step {t} seconds")
                action = self.choose_action(state)
                t_adjust, y_adjust = action

                # Update cumulative adjustments
                x_cumulative_adjust += t_adjust
                y_cumulative_adjust += y_adjust

                # Check for collision
                collision, distance = self.check_collision(t)
                print(f"Action taken: {action}, Collision: {collision}, Distance: {distance}")
                reward = -1 if collision else 10  # Negative reward for collision, positive for staying safe
                total_reward += reward

                # Update Q-table
                next_state = (t + t_adjust, y_adjust, distance if collision else 0)
                self.update_q_table(state, action, reward, next_state)
                state = next_state

                # If collision, break and reset trajectory
                if collision:
                    break

            # Decay exploration rate more aggressively
            self.exploration_rate *= self.exploration_decay

        # Apply cumulative adjustments to the trajectory equation
        # Update x and y components with the cumulative adjustments dynamically
        self.trajectory_equation['x'] = f"{self.trajectory_equation['x']} + {x_cumulative_adjust} * t"
        self.trajectory_equation['y'] = f"{self.trajectory_equation['y']} + {y_cumulative_adjust} * t"

        # Return the optimized trajectory after training
        return self.trajectory_equation


if __name__ == "__main__":
    # Example updated inputs
    time_selected = "2024-12-01 10:00:00"
    trajectory_equation = {
        'x': 'x(t) = 30.0 + 40.0 * t * cos(1.047) * cos(0.523)',
        'y': 'y(t) = 50.0 + 40.0 * t * cos(1.047) * sin(0.523)',
        'z': 'z(t) = 0.0 + 40.0 * t * sin(1.047)',
        'theta': 'theta(t) = 1.047 * (1 - exp(-0.05 * t))'
    }
    rocket_type = "Delta IV"
    launch_sites = ["Kennedy Space Center", "Baikonur Cosmodrome"]
    launch_coordinates = (45.9203, 63.3421)
    altitude = 1500
    altitude_range = [200, 1500]
    orbit_type = "MEO"
    tle_data_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data.csv'

    # Test the collision calculation and optimization
    collision_detector = CollisionDetection(time_selected, trajectory_equation, rocket_type, launch_sites,
                                            launch_coordinates, altitude, altitude_range, orbit_type, tle_data_path)
    optimized_trajectory = collision_detector.optimize_trajectory()
    print(f"Optimized Trajectory: {optimized_trajectory}")
