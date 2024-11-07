import matplotlib.pyplot as plt
import numpy as np

class TrajectoryVisualization:
    def __init__(self, trajectory_equations):
        self.trajectory_equations = trajectory_equations

    def plot_trajectory(self):
        """
        Plots the trajectory of the rocket based on the parametric equations.
        """
        t_values = np.linspace(0, 1000, num=500)
        x_values = [eval(self.trajectory_equations['x'])(t, 0) for t in t_values]
        y_values = [eval(self.trajectory_equations['y'])(t, 0) for t in t_values]
        z_values = [eval(self.trajectory_equations['z'])(t, 0) for t in t_values]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x_values, y_values, z_values, label='Rocket Trajectory')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        ax.legend()
        plt.show()
