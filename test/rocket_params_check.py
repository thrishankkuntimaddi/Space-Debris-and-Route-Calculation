import pandas as pd
import re


class RocketParameters:
    def __init__(self, csv_path="/mnt/data/rocket_data.csv"):
        # Load the rocket dataset from CSV
        self.rocket_df = pd.read_csv(csv_path)
        # Ensure Max_Altitude_km column is numeric
        self.rocket_df['Max_Altitude_km'] = pd.to_numeric(self.rocket_df['Max_Altitude_km'], errors='coerce')
        # Ensure Fuel_Consumption_kg_per_km column is numeric
        self.rocket_df['Fuel_Consumption_kg_per_km'] = pd.to_numeric(self.rocket_df['Fuel_Consumption_kg_per_km'],
                                                                     errors='coerce')
        # Calculate the maximum possible altitude for any rocket
        self.max_possible_altitude = self.rocket_df['Max_Altitude_km'].max()

    def get_rockets_for_altitude(self, selected_altitude):
        """
        Get rockets capable of reaching the selected altitude.
        """
        if selected_altitude > self.max_possible_altitude:
            return f"The selected altitude of {selected_altitude} km exceeds the maximum possible altitude of {self.max_possible_altitude} km. Please choose a lower value."
        capable_rockets = self.rocket_df[self.rocket_df['Max_Altitude_km'] >= selected_altitude]
        if capable_rockets.empty:
            return f"No rockets available for the selected altitude of {selected_altitude} km."
        return capable_rockets

    def check_rocket_criteria(self, rocket_type, launch_site, selected_altitude):
        """
        Check if the rocket type and launch site are correct and if the rocket can reach the selected altitude.
        """
        # First, check if there are rockets available for the selected altitude
        altitude_check = self.get_rockets_for_altitude(selected_altitude)
        if isinstance(altitude_check, str):
            return altitude_check

        # Check if the rocket type and launch site are valid
        pattern = re.escape(launch_site)
        rocket = self.rocket_df[(self.rocket_df['Rocket_Type'] == rocket_type) & (
            self.rocket_df['Compatible_Launch_Sites'].str.contains(pattern, case=False, na=False))]
        if rocket.empty:
            return f"Rocket type '{rocket_type}' not found or not available at the selected launch site '{launch_site}'."

        # Check if the rocket can reach the selected altitude
        max_altitude = rocket['Max_Altitude_km'].values[0]
        if selected_altitude > max_altitude:
            return f"The rocket '{rocket_type}' cannot reach the selected altitude of {selected_altitude} km (Max: {max_altitude} km)."

        # Return rocket details if all criteria are met
        fuel_consumption = int(rocket['Fuel_Consumption_kg_per_km'].values[0])
        compatible_sites = rocket['Compatible_Launch_Sites'].values[0]
        return {
            "Rocket_Type": rocket_type,
            "Fuel_Consumption_kg_per_km": fuel_consumption,
            "Compatible_Launch_Sites": compatible_sites
        }


# Example usage
if __name__ == "__main__":
    rocket_parameters = RocketParameters()

    # Check rocket criteria based on user selection of rocket type, launch site, and altitude
    rocket_type = "Falcon 9"
    launch_site = "Cape Canaveral"
    selected_altitude = 200000
    rocket_details = rocket_parameters.check_rocket_criteria(rocket_type, launch_site, selected_altitude)
    print(rocket_details)