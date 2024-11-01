import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
x0 = 45.964
y0 = 63.305
z0 = 0.0
velocity = 2800.0
angle_inclination = 0.8726646259971648  # radians
angle_azimuth = 0.9005898940290741     # radians

# Time values
t = np.linspace(0, 1, 100)

# Parametric equations for x(t), y(t), z(t)
x = x0 + velocity * t * np.cos(angle_inclination) * np.cos(angle_azimuth)
y = y0 + velocity * t * np.cos(angle_inclination) * np.sin(angle_azimuth)
z = z0 + velocity * t * np.sin(angle_inclination)

# Plotting the trajectory
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, label="Trajectory", color='b')
ax.scatter(x0, y0, z0, color='r', label="Starting Point")
ax.set_xlabel('X(t)')
ax.set_ylabel('Y(t)')
ax.set_zlabel('Z(t)')
ax.set_title("3D Trajectory Visualization")
ax.legend()

plt.show()
