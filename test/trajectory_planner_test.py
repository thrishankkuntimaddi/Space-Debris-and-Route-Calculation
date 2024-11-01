import math
import pandas as pd

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
        k = 0.1  # Constant controlling the rate of transition

        # Define theta as a function of time to simulate the gradual transition from vertical to horizontal
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

# Example usage
if __name__ == "__main__":
    dataset_path = '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/rocket_launch_parameters.csv'  # Replace with the correct path to your dataset
    trajectory_calculator = TrajectoryCalculator(dataset_path=dataset_path)
    trajectory_equation = trajectory_calculator.calculate_trajectory(
        rocket_type="Vega",
        launch_site="Guiana Space Centre, French Guiana",
        target_orbit=1900  # Example orbit radius in kilometers
    )
    print(trajectory_equation)