import math
import numpy as np
import pandas as pd

class TrajectoryCalculator:
    def __init__(self, dataset_path="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/rocket_launch_parameters.csv"):
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
        - dict: A dictionary with lambda functions representing parametric trajectory equations.
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
        k = 0.1  # Constant controlling the rate of transition

        # Define the lambda functions for the trajectory equations
        trajectory_equations = {
            'x': f"lambda t, theta: {x0} + {v0} * t * np.cos(theta) * np.cos({phi})",
            'y': f"lambda t, theta: {y0} + {v0} * t * np.cos(theta) * np.sin({phi})",
            'z': f"lambda t, theta: {z0} + {v0} * t * np.sin(theta)",
            'theta': f"lambda t: {theta} * (1 - np.exp(-{k} * t))"
        }

        return trajectory_equations

# # Example usage
# if __name__ == "__main__":
#     trajectory_calculator = TrajectoryCalculator()
#     trajectory_equations = trajectory_calculator.calculate_trajectory(
#         rocket_type="Vega",
#         launch_site="Guiana Space Centre, French Guiana",
#         target_orbit=1900  # Example orbit radius in kilometers
#     )
#     print(trajectory_equations)
