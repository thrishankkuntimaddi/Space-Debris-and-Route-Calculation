purpose = "Visualization"

import matplotlib.pyplot as plt
import numpy as np

class TrajectoryVisualization:
    def visualize_trajectory(self, initial_trajectory, adjusted_trajectory, optimized_trajectory, tle_positions):
        """
        Visualize the initial, adjusted, and optimized trajectories along with space debris.
        """
        plt.figure(figsize=(10, 6))

        # Plot initial trajectory (projectile motion)
        x = np.linspace(0, 10, 100)
        y = -0.05 * (x - 5) ** 2 + 25  # Example parabolic path
        plt.plot(x, y, label='Initial Trajectory', linestyle='--')

        # Plot adjusted trajectory if collision detected
        if adjusted_trajectory['collision_detected']:
            y_adjusted = y + 2  # Example adjustment
            plt.plot(x, y_adjusted, label='Adjusted Trajectory', linestyle='-.')

        # Plot optimized trajectory
        y_optimized = y + 1  # Example optimization
        plt.plot(x, y_optimized, label='Optimized Trajectory', linestyle='-')

        # Plot space debris (current and future positions)
        for position, _ in tle_positions:
            plt.scatter(position[0], position[1], color='red', marker='o', s=20, label='Space Debris' if 'Space Debris' not in plt.gca().get_legend_handles_labels()[1] else "")

        plt.xlabel('X Position (km)')
        plt.ylabel('Y Position (km)')
        plt.title('Rocket Trajectories and Space Debris')
        plt.legend()
        plt.grid(True)
        plt.show()