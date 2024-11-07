import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict
import re


class TrajectoryVisualizer:
    def __init__(self, equations: Dict[str, str], t_range: tuple, num_points: int = 500):
        """
        Initialize the TrajectoryVisualizer with trajectory equations.

        Parameters:
        - equations: A dictionary containing parametric equations for x(t), y(t), z(t), and theta(t).
        - t_range: A tuple specifying the start and end time (t_min, t_max).
        - num_points: Number of points to sample in the time range.
        """
        self.equations = equations
        self.t_values = np.linspace(t_range[0], t_range[1], num_points)

        # Parse the equations
        self.x_func = self._parse_equation(equations['x'])
        self.y_func = self._parse_equation(equations['y'])
        self.z_func = self._parse_equation(equations['z'])
        self.theta_func = self._parse_equation(equations['theta'])

    def _parse_equation(self, equation_str: str) -> Callable[[float], float]:
        """
        Convert a string equation to a callable function of time (t).

        Parameters:
        - equation_str: A string representing the equation.

        Returns:
        - A callable function that takes t as input and returns the computed value.
        """
        # Extract the equation part after the equals sign
        equation_str = equation_str.split('=')[1].strip()
        # Replace 't' with '{t}' for formatting
        equation_str = equation_str.replace('t', '{t}')

        # Define a function that evaluates the equation for a given t
        def func(t):
            # Use eval to evaluate the equation, replacing '{t}' with the current value of t
            return eval(equation_str.format(t=t), {"np": np, "exp": np.exp, "cos": np.cos, "sin": np.sin})

        return func

    def plot_trajectory(self):
        """Generates a 2D plot of the trajectory based on the input equations."""
        # Calculate x, y, z values based on the given functions
        x = np.array([self.x_func(t) for t in self.t_values])
        y = np.array([self.y_func(t) for t in self.t_values])
        z = np.array([self.z_func(t) for t in self.t_values])
        theta = np.array([self.theta_func(t) for t in self.t_values])

        # Apply theta rotation to x, y, z coordinates to add angular effect
        x_rot = x * np.cos(theta) - y * np.sin(theta)
        y_rot = x * np.sin(theta) + y * np.cos(theta)
        z_rot = z  # z remains the same as theta is a horizontal rotation

        # Create a 2D plot to represent the spiral trajectory
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.plot(x_rot, y_rot, label='Trajectory', color='b', linewidth=2)
        ax.plot(x_rot, y_rot, linestyle='--', color='black', linewidth=1, alpha=0.5, label='Selected Orbit')

        # Plot Earth as a small circle at the origin
        earth_radius = 10
        earth = plt.Circle((0, 0), earth_radius, color='blue', alpha=0.5, label='Earth')
        ax.add_patch(earth)

        # Adjust the trajectory to start from Earth's surface
        x_rot -= x_rot[0] - earth_radius * np.cos(0.0)  # Shift x to start from Earth's surface
        y_rot -= y_rot[0] - earth_radius * np.sin(0.0)  # Shift y to start from Earth's surface

        # Labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('2D Trajectory Visualization with Selected Orbit')
        ax.axis('equal')
        ax.legend()

        plt.show()


# Example usage
if __name__ == "__main__":
    # Define trajectory equations with offsets
    equations = {
        'x': 'x(t) = 5.236 + 5.5 * t * np.cos(0.7853981633974483) * np.cos(0.0)',
        'y': 'y(t) = -52.768 + 5.5 * t * np.cos(0.7853981633974483) * np.sin(0.0)',
        'z': 'z(t) = 0.0 + 5.5 * t * np.sin(0.7853981633974483)',
        'theta': 'theta(t) = 0.7853981633974483 * (1 - np.exp(-0.1 * t))'
    }

    # Create an instance of TrajectoryVisualizer with the trajectory equations
    visualizer = TrajectoryVisualizer(equations=equations, t_range=(0, 10))
    # Plot the trajectory
    visualizer.plot_trajectory()
