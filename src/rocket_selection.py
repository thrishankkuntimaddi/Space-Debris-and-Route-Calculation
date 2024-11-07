import pandas as pd
import re

purpose = '''
preload: Dataset contains rocket type, launch site, max_altitude, launch site co-ordinates(lat, lon)
inputs: target_altitude (in km)
outputs: Type of Rocket, Launch Site, Launch Coordinates  
'''

class RocketSelector:
    def __init__(self, csv_path="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/rocket_data.csv"):
        # Load the rocket dataset from CSV
        self.rocket_df = pd.read_csv(csv_path)
        # Ensure Max_Altitude_km column is numeric
        self.rocket_df['Max_Altitude_km'] = pd.to_numeric(self.rocket_df['Max_Altitude_km'], errors='coerce')
        # Calculate the maximum possible altitude for any rocket
        self.max_possible_altitude = self.rocket_df['Max_Altitude_km'].max()

    def get_orbit_range(self, orbit_type):
        """
        Get the altitude range for a specific orbit type.
        """
        orbit_ranges = {
            'Low Earth Orbit (LEO)': [200, 2000],
            'Medium Earth Orbit (MEO)': [2000, 35785],
            'Geostationary Orbit (GEO)': [35786, 35786],
            'High Earth Orbit (HEO)': [35787, 40000]
        }
        return orbit_ranges.get(orbit_type, None)

    def get_rockets_for_orbit_and_altitude(self, target_altitude, orbit_type):
        """
        Get rockets capable of reaching the specified target altitude within the selected orbit type.
        """
        altitude_range = self.get_orbit_range(orbit_type)
        if altitude_range is None:
            return f"Invalid orbit type: {orbit_type}. Please choose a valid orbit type."

        min_range, max_range = altitude_range
        if not (min_range <= target_altitude <= max_range):
            return f"The selected altitude of {target_altitude} km is not within the specified range of {min_range} to {max_range} km for {orbit_type}. Please choose a valid altitude within the range."

        # Filter rockets that can reach the selected orbit type range
        rockets_in_orbit = self.rocket_df[(self.rocket_df['Max_Altitude_km'] >= min_range) & (self.rocket_df['Max_Altitude_km'] <= max_range)]

        # Further filter rockets that can reach the target altitude
        suitable_rockets = rockets_in_orbit[rockets_in_orbit['Max_Altitude_km'] >= target_altitude]

        if suitable_rockets.empty:
            return f"No rockets available for the specified target altitude of {target_altitude} km within the selected orbit type {orbit_type}."

        # Sort rockets by max altitude
        suitable_rockets = suitable_rockets.sort_values(by='Max_Altitude_km')

        # Prepare the result with required columns
        result = suitable_rockets[['Rocket_Type', 'Launch_Site', 'Launch_Site_Coordinates_latitude_and_longitude', 'Max_Altitude_km']].to_dict(orient='records')
        return result

    def check_rocket_criteria(self, target_altitude, orbit_type):
        """
        Allow the user to dynamically input rocket type based on the available rockets for the specified target altitude and orbit type.
        """
        # Get the list of rockets for the given target altitude and orbit type
        rockets_list = self.get_rockets_for_orbit_and_altitude(target_altitude, orbit_type)
        if isinstance(rockets_list, str):
            return rockets_list

        # Display available rockets
        print("\nAvailable rockets for the specified target altitude and orbit type:")
        for i, rocket in enumerate(rockets_list):
            print(f"{i + 1}: {rocket['Rocket_Type']}")

        # Allow user to select rocket type dynamically
        rocket_type = input("\nEnter the rocket type from the list above: ")

        # Filter rockets by the provided rocket type
        rocket = [r for r in rockets_list if r['Rocket_Type'] == rocket_type]
        if not rocket:
            return f"Rocket type '{rocket_type}' not found."

        # Output selected rocket details with additional orbit coordinates
        selected_orbit_coordinates = f"Coordinates for target altitude {target_altitude} km"
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
#     rocket_selector = RocketSelector()
#
#     # Select target altitude and orbit type
#     target_altitude = 35786
#     orbit_type = 'Geostationary Orbit (GEO)'
#     rockets_for_target_altitude = rocket_selector.get_rockets_for_orbit_and_altitude(target_altitude, orbit_type)
#     print("Rockets for Target Altitude and Orbit Type:", rockets_for_target_altitude)
#
#     # Check rocket criteria based on user dynamic input of rocket type
#     rocket_details = rocket_selector.check_rocket_criteria(target_altitude, orbit_type)
#     if isinstance(rocket_details, str):
#         print(rocket_details)
#     else:
#         rocket_type, launch_sites, launch_coordinates = rocket_details['Rocket_Type'], rocket_details['Launch_Site'], rocket_details['Launch_Site_Coordinates']
#         print(f"Rocket Type: {rocket_type}")
#         print(f"Launch Site: {launch_sites}")
#         print(f"Launch Site Coordinates: {launch_coordinates}")