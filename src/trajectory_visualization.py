purpose = "Visualization"

import matplotlib.pyplot as plt
import numpy as np

class TrajectoryVisualization:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Initialize plot figure and axis for visualization
    def visualize_collision_trajectory(self, initial_trajectory, adjusted_trajectory, optimized_trajectory, tle_positions):
        """
        Visualize the initial, adjusted, and optimized trajectories along with space debris when a collision is detected.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Plot initial trajectory (half projectile motion from ground to selected orbit)
        x = np.linspace(0, 500, 100)  # Example x values in km
        y = -0.002 * (x - 500) ** 2 + 800  # Example half parabolic path (projectile motion to selected orbit)
        self.ax.plot(x, y, label='Initial Trajectory', linestyle='--', color='blue')

        # Plot selected orbit as a horizontal line
        self.ax.axhline(y=800, color='black', linestyle=':', label='Selected Orbit')

        # Plot adjusted trajectory if collision detected
        if adjusted_trajectory['collision_detected']:
            y_adjusted = y + 50  # Example adjustment to avoid collision
            self.ax.plot(x, y_adjusted, label='Adjusted Trajectory', linestyle='-.', color='orange')
            collision_x, collision_y = x[50], y[50]  # Example collision point
            self.ax.scatter(collision_x, collision_y, color='red', marker='x', s=100, label='Point of Collision')

        # Plot optimized trajectory
        y_optimized = y + 25  # Example optimization to avoid collision
        self.ax.plot(x, y_optimized, label='Optimized Trajectory', linestyle='-', color='green')

        # Plot space debris (current and future positions)
        for i, (position, _) in enumerate(tle_positions):
            # Adjust space debris to better match the visualization scale
            debris_x = position[0] / 10  # Scale down X position for visualization
            debris_y = position[1] / 10  # Scale down Y position for visualization
            self.ax.scatter(debris_x, debris_y, color='red', marker='o', s=20, label='Space Debris' if i == 0 else "")

        self.ax.set_xlabel('X Position (km)')
        self.ax.set_ylabel('Y Position (km)')
        self.ax.set_title('Rocket Trajectories and Space Debris (Collision Detected)')
        self.ax.legend()
        self.ax.grid(True)
        plt.show()

    def visualize_no_collision_trajectory(self, initial_trajectory, optimized_trajectory):
        """
        Visualize the initial and optimized trajectories when no collision occurs after optimization.
        """
        self.fig, self.ax = plt.subplots(figsize=(10, 6))

        # Plot initial trajectory (half projectile motion from ground to selected orbit)
        x = np.linspace(0, 500, 100)  # Example x values in km
        y = -0.002 * (x - 500) ** 2 + 800  # Example half parabolic path (projectile motion to selected orbit)
        self.ax.plot(x, y, label='Initial Trajectory', linestyle='--', color='blue')

        # Plot selected orbit as a horizontal line
        self.ax.axhline(y=800, color='black', linestyle=':', label='Selected Orbit')

        # Plot optimized trajectory (assuming no collision adjustment was needed)
        y_optimized = y  # Example path without collision adjustment
        self.ax.plot(x, y_optimized, label='Optimized Trajectory', linestyle='-', color='green')

        self.ax.set_xlabel('X Position (km)')
        self.ax.set_ylabel('Y Position (km)')
        self.ax.set_title('Rocket Trajectories (No Collision Detected)')
        self.ax.legend()
        self.ax.grid(True)
        plt.show()
