import numpy as np
import math
import pandas as pd
import random
from skyfield.api import Loader, EarthSatellite
from skyfield.elementslib import osculating_elements_of
from skyfield.api import Topos
import tensorflow as tf
from tensorflow.keras import layers, optimizers

class CollisionDetectionDeep:
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
        self.altitude_range = [200, 2000]
        self.orbit_type = orbit_type
        self.time_selected = time_selected
        self.tle_data = pd.read_csv(tle_data_path, low_memory=False)
        self.loader = Loader('~/.skyfield')
        self.ts = self.loader.timescale()
        eph = self.loader('de421.bsp')
        self.earth = eph['earth']

        # Parameters for Deep Q-Learning
        self.state_size = 3  # e.g., time, x_offset, y_offset
        self.action_size = 4  # Number of possible actions
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

        # Define possible actions
        self.actions = [(0, 0), (10, 0), (0, 10), (-10, 0)]  # Adjustments for time and y-offset

    def _build_model(self):
        # Neural network for Deep Q-Learning
        model = tf.keras.Sequential()
        model.add(layers.Input(shape=(self.state_size,)))  # Use Input layer instead of input_dim
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        return model

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
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state)[0]
        return np.argmax(q_values)

    def replay(self, memory, batch_size):
        # Experience replay to train the model
        minibatch = random.sample(memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def optimize_trajectory(self, episodes=5, batch_size=32):
        memory = []  # Replay memory for storing experiences
        for episode in range(episodes):
            print(f"Starting episode {episode + 1}/{episodes}")
            state = np.array([[0, 0, 0]])  # Initial state (e.g., time, x_offset, y_offset)
            total_reward = 0

            for t in range(0, 90, 30):  # Increased time step to 30 seconds for faster execution
                print(f"Time step {t} seconds")
                action = self.choose_action(state)
                t_adjust, y_adjust = self.actions[action]

                # Update cumulative adjustments
                x_cumulative_adjust = t_adjust
                y_cumulative_adjust = y_adjust

                # Check for collision
                collision, distance = self.check_collision(t)
                print(f"Action taken: {action}, Collision: {collision}, Distance: {distance}")
                reward = -100 if collision else 10  # Negative reward for collision, positive for staying safe
                total_reward += reward

                # Get next state
                next_state = np.array([[t + t_adjust, y_adjust, distance if collision else 0]])
                done = collision

                # Store experience in memory
                memory.append((state, action, reward, next_state, done))
                state = next_state

                # If collision, break and reset trajectory
                if collision:
                    break

                # Train the model using replay
                if len(memory) > batch_size:
                    self.replay(memory, batch_size)

            # Decay exploration rate more aggressively
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        # Apply cumulative adjustments to the trajectory equation
        self.trajectory_equation[
            'x'] = f"x(t) = 45.964 + 51.6 * t * cos(0.7853981633974483) * cos(0.0) + {x_cumulative_adjust} * t"
        self.trajectory_equation[
            'y'] = f"y(t) = 63.305 + 51.6 * t * cos(0.7853981633974483) * sin(0.0) + {y_cumulative_adjust} * t"

        # Return the optimized trajectory after training
        return self.trajectory_equation

# if __name__ == "__main__":
#     # Example trajectory equation and timestamp
#     timestamp = pd.Timestamp("2024-11-09 12:00:05")  # Slightly adjusted time to induce collision
#     trajectory_equation = {
#         'x': 'x(t) = 45.964 + 51.6 * t * cos(0.7853981633974483) * cos(0.0)',
#         'y': 'y(t) = 63.305 + 51.6 * t * cos(0.7853981633974483) * sin(0.0)',
#         'z': 'z(t) = 0.0 + 51.6 * t * sin(0.7853981633974483)',
#         'theta': 'theta(t) = 0.7853981633974483 * (1 - exp(-0.1 * t))'
#     }
#     rocket_type = "Falcon 9"
#     launch_sites = ["Cape Canaveral", "Vandenberg"]
#     launch_coordinates = (28.5623, -80.5774)
#     altitude = 2000
#     altitude_range = [200, 2000]
#     orbit_type = "LEO"
#     time_selected = "2024-11-09 12:00:00"
#
#     # Path to TLE dataset
#     tle_data_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data.csv'
#
#     # Test the collision calculation and optimization
#     collision_detector = CollisionDetection(timestamp, trajectory_equation, rocket_type, launch_sites,
#                                             launch_coordinates, altitude, altitude_range, orbit_type, time_selected,
#                                             tle_data_path)
#
#     # Optimize the trajectory to avoid collisions
#     optimized_trajectory = collision_detector.optimize_trajectory(episodes=1, batch_size=32)
#     print(f"Optimized Trajectory: {optimized_trajectory}")
