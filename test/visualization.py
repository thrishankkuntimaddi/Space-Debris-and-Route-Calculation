import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from skyfield.api import load, EarthSatellite


# Rocket Trajectory Equations
def trajectory(t):
    theta = theta_transition(t)
    x = 45.964 + 2800.0 * t * np.cos(theta) * np.cos(0.9005898940290741)
    y = 63.305 + 2800.0 * t * np.cos(theta) * np.sin(0.9005898940290741)
    z = 0.0 + 2800.0 * t * np.sin(theta)
    return np.array([x, y, z])


# Theta Transition Function
def theta_transition(t):
    return 0.8726646259971648 * (1 - np.exp(-0.1 * t))


# Example TLE data (modified for guaranteed collision scenario)
tle_lines_list = [
    (
        "1 25544U 98067A   24298.83357940  .00000641  00000-0  18852-4 0  9993",
        "2 25544  51.6435 218.0124 0007817  36.8750  85.1486 15.50029393391706"
    ),
    (
        "1 12345U 12345A   24298.83357940  .00000273  00000-0  10239-4 0  9995",
        "2 12345  32.8748 194.9711 0000001 243.8597 100.5343 15.50000000000000"
    )
]

# Load timescale for calculations
ts = load.timescale()


# Collision Detection Function
def check_collision(tle_lines_list, threshold_distance=50.0, max_altitude=20000):
    collisions = []

    for tle_lines in tle_lines_list:
        line1, line2 = tle_lines
        satellite = EarthSatellite(line1, line2, 'Sample Satellite', ts)

        # Define the time for which to calculate position
        time = ts.now()  # You can specify a future time here as well

        # Calculate the position of the satellite
        geometry = satellite.at(time)
        satellite_position = geometry.position.km  # Position in kilometers

        # Iterate over different times to check for collision
        for t in np.linspace(0, 20, num=200):  # Time range and steps
            rocket_position = trajectory(t)
            distance = euclidean(rocket_position, satellite_position)
            altitude = np.linalg.norm(rocket_position)  # Altitude of the rocket

            # Debugging log
            print(f"Time: {t:.2f}s, Distance: {distance:.2f} km, Altitude: {altitude:.2f} km")

            # Check if altitude exceeds maximum altitude
            if altitude > max_altitude:
                break

            # Check for collision
            if distance < threshold_distance:
                collisions.append((t, satellite.name, distance))
                break  # Exit loop if collision is detected

    return collisions


# Perform Collision Detection
collisions = check_collision(tle_lines_list)

# Display the results
if collisions:
    for collision in collisions:
        t, satellite_name, distance = collision
        print(f"Collision detected at t={t:.2f}s with {satellite_name} at a distance of {distance:.2f} km.")
else:
    print("No collisions detected.")

# Generate data points for the trajectory
time_values = np.linspace(0, 20, num=200)
trajectory_points = np.array([trajectory(t) for t in time_values])

# Plot the trajectory in 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Extract x, y, z components
x_vals = trajectory_points[:, 0]
y_vals = trajectory_points[:, 1]
z_vals = trajectory_points[:, 2]

ax.plot(x_vals, y_vals, z_vals, label='Rocket Trajectory', color='b')

# Plotting target orbit
target_altitude = 2500
orbit_radius = target_altitude
theta_vals = np.linspace(0, 2 * np.pi, 100)
orbit_x = 45.964 + orbit_radius * np.cos(theta_vals)
orbit_y = 63.305 + orbit_radius * np.sin(theta_vals)
orbit_z = np.zeros_like(theta_vals)

ax.plot(orbit_x, orbit_y, orbit_z, label='Target Orbit (MEO)', color='r', linestyle='--')

# Labels and legend
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Rocket Trajectory to Medium Earth Orbit')
ax.legend()

plt.show()