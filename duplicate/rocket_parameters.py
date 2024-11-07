import pandas as pd
import re


class RocketParameters:
    def __init__(self, csv_path="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/rocket_data.csv"):
        # Load the rocket dataset from CSV
        self.rocket_df = pd.read_csv(csv_path)
        # Ensure Max_Altitude_km column is numeric
        self.rocket_df['Max_Altitude_km'] = pd.to_numeric(self.rocket_df['Max_Altitude_km'], errors='coerce')
        # Calculate the maximum possible altitude for any rocket
        self.max_possible_altitude = self.rocket_df['Max_Altitude_km'].max()

    def get_rockets_for_range(self, selected_altitude, altitude_range, orbit_type):
        """
        Get rockets capable of reaching the selected altitude within the specified range and orbit type.
        """
        min_range, max_range = altitude_range
        if not (min_range <= selected_altitude <= max_range):
            return f"The selected altitude of {selected_altitude} km is not within the specified range of {min_range} to {max_range} km. Please choose a valid altitude within the range."

        capable_rockets = self.rocket_df[(self.rocket_df['Max_Altitude_km'] >= selected_altitude) &
                                         (self.rocket_df['Max_Altitude_km'] >= min_range) &
                                         (self.rocket_df['Max_Altitude_km'] <= max_range)]

        if capable_rockets.empty:
            return f"No rockets available for the selected altitude of {selected_altitude} km within the specified range."

        # Prepare the result with required columns
        result = capable_rockets[['Rocket_Type', 'Launch_Site', 'Launch_Site_Coordinates_latitude_and_longitude']].to_dict(orient='records')
        return result

    def check_rocket_criteria(self, selected_altitude, altitude_range, orbit_type):
        """
        Allow the user to dynamically input rocket type based on the available rockets.
        """
        # Get the list of rockets for the given altitude and range
        rockets_list = self.get_rockets_for_range(selected_altitude, altitude_range, orbit_type)
        if isinstance(rockets_list, str):
            return rockets_list

        # Display available rockets
        print("\nAvailable rockets for the selected altitude and range:\n")
        for i, rocket in enumerate(rockets_list):
            print(
                f"{i + 1}: {rocket['Rocket_Type']}")

        # Allow user to select rocket type dynamically
        rocket_type = input("\nEnter the rocket type from the list above: ")

        # Filter rockets by the provided rocket type
        rocket = [r for r in rockets_list if r['Rocket_Type'] == rocket_type]
        if not rocket:
            return f"Rocket type '{rocket_type}' not found."

        # Output selected rocket details with additional orbit coordinates
        selected_orbit_coordinates = f"Coordinates for {orbit_type} at {selected_altitude} km"
        rocket[0]['Selected_Orbit_Coordinates'] = selected_orbit_coordinates

        # Prepare summary output
        summary = {
            "Rocket_Type": rocket[0]['Rocket_Type'],
            "Launch_Site": rocket[0]['Launch_Site'],
            "Launch_Site_Coordinates": rocket[0]['Launch_Site_Coordinates_latitude_and_longitude'],
            "Orbit_Coordinates": rocket[0]['Selected_Orbit_Coordinates']
        }

        return summary

# # Example usage
# if __name__ == "__main__":
#     rocket_parameters = RocketParameters()
#
#     # Get rockets capable of reaching a specific altitude within a specified range and orbit type
#     selected_altitude = 222
#     altitude_range = [200, 2000]
#     orbit_type = 'Low Earth Orbit (LEO)'
#     rockets_for_range = rocket_parameters.get_rockets_for_range(selected_altitude, altitude_range, orbit_type)
#     print(rockets_for_range)
#
#     # Check rocket criteria based on user dynamic input of rocket type
#     rocket_details = rocket_parameters.check_rocket_criteria(selected_altitude, altitude_range, orbit_type)
#     print(rocket_details)
