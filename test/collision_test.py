import numpy as np
from skyfield.api import EarthSatellite, load
from scipy.spatial import distance


def tle_to_position(tle_line1, tle_line2, time):
    """
    Converts TLE lines into a position vector (x, y, z) at a given time.
    """
    satellite = EarthSatellite(tle_line1, tle_line2, 'debris', load.timescale())
    geocentric = satellite.at(time)
    position = geocentric.position.km  # Returns (x, y, z) in kilometers
    return np.array(position)


def trajectory_position(x_eq, y_eq, z_eq, t):
    """
    Evaluates the given trajectory equations for x, y, z at time t.
    """
    x = eval(x_eq.replace('t', str(t)))
    y = eval(y_eq.replace('t', str(t)))
    z = eval(z_eq.replace('t', str(t)))
    return np.array([x, y, z])


def check_collision(tle_data, trajectory_eq, time_range, threshold_distance=5.0):
    """
    Checks for possible collisions between a trajectory and TLE objects.

    Parameters:
        tle_data (list): List of tuples containing TLE lines.
        trajectory_eq (dict): A dictionary with 'x', 'y', and 'z' keys for trajectory equations.
        time_range (list): List of time points to evaluate.
        threshold_distance (float): Minimum distance considered as a collision (in km).

    Returns:
        list: List of collision events.
    """
    collisions = []
    ts = load.timescale()

    for t in time_range:
        time = ts.utc(2024, 11, 7, 0, 0, t)  # Example time - needs customization based on requirement
        traj_pos = trajectory_position(trajectory_eq['x'], trajectory_eq['y'], trajectory_eq['z'], t)

        for tle_line1, tle_line2 in tle_data:
            debris_pos = tle_to_position(tle_line1, tle_line2, time)

            # Calculate the Euclidean distance between the debris and trajectory point
            dist = distance.euclidean(traj_pos, debris_pos)
            if dist <= threshold_distance:
                collisions.append({
                    'time': time,
                    'debris_position': debris_pos,
                    'trajectory_position': traj_pos,
                    'distance': dist
                })
    return collisions


if __name__ == "__main__":
    # Example TLE data (replace with actual dataset)
    tle_data = [
        ("1 25544U 98067A   20333.54807870  .00001267  00000-0  29647-4 0  9995",
         "2 25544  51.6456  80.4486 0005542  40.3199  57.8884 15.48905227253849")
    ]

    # Provided trajectory equation (replace x(t), y(t), z(t) equations appropriately)
    trajectory_eq = {
        'x': '28.3922 + 56.0 * t * np.cos(0.7853981633974483) * np.cos(0.0)',
        'y': '-80.6077 + 56.0 * t * np.cos(0.7853981633974483) * np.sin(0.0)',
        'z': '0.0 + 56.0 * t * np.sin(0.7853981633974483)'
    }

    # Time range to evaluate
    time_range = range(0, 3600, 60)  # every minute in an hour

    # Check for collisions
    collisions = check_collision(tle_data, trajectory_eq, time_range)

    if collisions:
        for collision in collisions:
            print(f"Collision detected at {collision['time']}:")
            print(f"  Trajectory Position: {collision['trajectory_position']}")
            print(f"  Debris Position: {collision['debris_position']}")
            print(f"  Distance: {collision['distance']} km")
    else:
        print("No collisions detected.")
