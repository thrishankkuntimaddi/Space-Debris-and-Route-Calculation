import math
import pandas as pd
import numpy as np
from sgp4.api import Satrec
from datetime import datetime


class TrajectoryCalculator:
    def __init__(self, dataset_path):
        """
        Initializes the TrajectoryCalculator with a dataset.

        Parameters:
        - dataset_path (str): The file path to the dataset containing rocket parameters.
        """
        self.dataset = pd.read_csv(dataset_path)

    def calculate_trajectory(self, rocket_type, launch_site, target_orbit):
        """
        Calculates the trajectory equation for a rocket to reach a specified circular orbit.

        Parameters:
        - rocket_type (str): The type of the rocket (e.g., 'Soyuz')
        - launch_site (str): Name of the launch site (e.g., 'Baikonur Cosmodrome')
        - target_orbit (float): The radius of the target orbit in kilometers from Earth's center

        Returns:
        - str: Parametric trajectory equations as a string.
        """

        # Find the rocket data for the specified rocket type and launch site
        rocket_data = self.dataset[(self.dataset['Rocket_Type'] == rocket_type) &
                                   (self.dataset['Launch_Site'] == launch_site)]

        if rocket_data.empty:
            return "Rocket type or launch site not found in dataset."

        # Extract necessary parameters
        launch_site_coordinates = rocket_data['Launch_Site_Coordinates_(x0,y0,z0)'].iloc[0]
        x0, y0, z0 = map(float, launch_site_coordinates.strip('()').split(','))
        v0 = float(rocket_data['Initial_Velocity_v0_m_per_s'].iloc[0])
        theta = math.radians(float(rocket_data['Launch_Angle_theta_deg'].iloc[0]))  # convert to radians
        phi = math.radians(float(rocket_data['Inclination_Angle_phi_deg'].iloc[0]))  # convert to radians

        # Define theta as a function of time to simulate the gradual transition from vertical to horizontal
        k = 0.1  # Constant controlling the rate of transition (can be adjusted)

        theta_equation = "theta(t) = {} * (1 - exp(-{} * t))".format(theta, k)

        # Define the trajectory equations
        x_equation = "x(t) = {} + {} * t * cos(theta(t)) * cos({})".format(x0, v0, phi)
        y_equation = "y(t) = {} + {} * t * cos(theta(t)) * sin({})".format(y0, v0, phi)
        z_equation = "z(t) = {} + {} * t * sin(theta(t))".format(z0, v0)

        # Combine into a single output string for the trajectory equation
        trajectory_equation = (
            "Trajectory Equation:\n"
            f"  {x_equation}\n"
            f"  {y_equation}\n"
            f"  {z_equation}\n\n"
            "Theta Transition Function:\n"
            f"  {theta_equation}"
        )

        return trajectory_equation

    def check_collision(self, debris_coordinates, x_t, y_t, z_t, time_range):
        """
        Checks if there is a collision with space debris within a given time range.

        Parameters:
        - debris_coordinates (list of tuples): List of debris coordinates as (x, y, z).
        - x_t, y_t, z_t (functions): Functions representing the x, y, and z trajectory equations.
        - time_range (tuple): The time range to check for collision (start, end).

        Returns:
        - bool: True if a collision is detected, False otherwise.
        """

        collision_detected = False
        for t in np.linspace(time_range[0], time_range[1], num=1000):  # Check at 1000 time steps in the range
            rocket_position = (round(x_t(t), 3), round(y_t(t), 3), round(z_t(t), 3))
            print(f"Checking rocket position at t={t:.2f}: {rocket_position}")  # Debugging statement
            for debris in debris_coordinates:
                debris_rounded = (round(debris[0], 3), round(debris[1], 3), round(debris[2], 3))
                print(f"Comparing with debris position: {debris_rounded}")  # Debugging statement
                if np.allclose(rocket_position, debris_rounded, atol=5):  # Increased tolerance to 5 units
                    print(f"Collision detected at t={t:.2f} with debris at {debris_rounded}")  # Debugging statement
                    collision_detected = True
                    break
            if collision_detected:
                break
        if not collision_detected:
            print("No collision detected in the given time range.")
        return collision_detected

    def tle_to_xyz(self, tle_line1, tle_line2, time_range):
        """
        Converts TLE data to Cartesian coordinates for a given time range.

        Parameters:
        - tle_line1 (str): The first line of TLE data.
        - tle_line2 (str): The second line of TLE data.
        - time_range (tuple): The time range to generate coordinates for (start, end).

        Returns:
        - list: A list of (x, y, z) coordinates for the specified time range.
        """
        satellite = Satrec.twoline2rv(tle_line1, tle_line2)
        jd, fr = satellite.jdsatepoch, satellite.jdsatepochF  # Use epoch from TLE
        coordinates = []

        for t in np.linspace(time_range[0], time_range[1], num=100):
            e, r, v = satellite.sgp4(jd, fr + t / 86400.0)
            if e == 0:
                coordinates.append((r[0], r[1], r[2]))
                print(f"Debris position at t={t:.2f}: {tuple(round(coord, 3) for coord in r)}")  # Debugging statement

        return coordinates


# Example usage
if __name__ == "__main__":
    try:
        # Load the dataset
        file_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/rocket_launch_parameters.csv'

        # Instantiate the class with the dataset path
        trajectory_calculator = TrajectoryCalculator(dataset_path=file_path)

        # Test the calculate_trajectory method
        trajectory_equation = trajectory_calculator.calculate_trajectory(
            rocket_type="Soyuz",
            launch_site="Baikonur Cosmodrome, Kazakhstan",
            target_orbit=2001  # Example orbit radius in kilometers
        )

        if isinstance(trajectory_equation, str):
            print(trajectory_equation)
        else:
            # Print the trajectory equation
            print(trajectory_equation)

            # ISS TLE data
            tle_line1 = "1 25544U 98067A   24276.42875240  .00000774  00000-0  21667-4 0  9994"
            tle_line2 = "2 25544  51.6455  69.2137 0008337 273.0653 235.6571 15.50147641399066"
            time_range = (0, 500)  # Check for collision in the first 500 seconds

            # Convert TLE to Cartesian coordinates
            debris_coordinates = trajectory_calculator.tle_to_xyz(tle_line1, tle_line2, time_range)

            # Create functions for x(t), y(t), z(t)
            k = 0.1
            theta = math.radians(float(trajectory_calculator.dataset['Launch_Angle_theta_deg'].iloc[0]))
            phi = math.radians(float(trajectory_calculator.dataset['Inclination_Angle_phi_deg'].iloc[0]))
            x0, y0, z0 = map(float, trajectory_calculator.dataset['Launch_Site_Coordinates_(x0,y0,z0)'].iloc[0].strip('()').split(','))
            v0 = float(trajectory_calculator.dataset['Initial_Velocity_v0_m_per_s'].iloc[0])

            def theta_t(t):
                return theta * (1 - np.exp(-k * t))

            def x_t(t):
                return x0 + v0 * t * np.cos(theta_t(t)) * np.cos(phi)

            def y_t(t):
                return y0 + v0 * t * np.cos(theta_t(t)) * np.sin(phi)

            def z_t(t):
                return z0 + v0 * t * np.sin(theta_t(t))

            # Check for collision using the generated functions
            collision_detected = trajectory_calculator.check_collision(debris_coordinates, x_t, y_t, z_t, time_range)

            if collision_detected:
                print("Collision detected with ISS!")
            else:
                print("No collision detected with ISS.")
    except FileNotFoundError:
        print("Error: The dataset file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
