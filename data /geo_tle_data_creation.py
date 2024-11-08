import random
from datetime import datetime, timedelta
import os
import csv


class GEOTLEGenerator:
    def __init__(self, num_objects, directory, timestamp):
        self.num_objects = num_objects
        self.directory = directory
        self.timestamp = timestamp
        self.epoch_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%y%j")
        self.file_path = os.path.join(directory, "geo_tle_dataset.csv")

    def generate_geo_tle(self, satellite_id):
        """
        Generate a TLE entry for a given satellite ID and epoch date for Geostationary Earth Orbit (GEO).
        """
        # Line 1 values
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"

        # Line 2 values (random within realistic GEO parameters)
        inclination = random.uniform(0, 5)  # Inclination in degrees, GEO is near equatorial
        raan = random.uniform(0, 360)  # Right ascension of ascending node
        eccentricity = random.randint(0, 10000)  # Eccentricity, almost circular orbit
        arg_perigee = random.uniform(0, 360)  # Argument of perigee
        mean_anomaly = random.uniform(0, 360)  # Mean anomaly
        mean_motion = 1.0027  # Mean motion for GEO (~1 orbit per day)
        rev_number = random.randint(1, 99999)  # Revolution number at epoch

        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"

        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

    def generate_dataset(self):
        """
        Generate a TLE dataset with the specified number of objects for GEO and save it to the desired directory.
        """
        # Check if the directory exists; if not, create it
        os.makedirs(self.directory, exist_ok=True)

        # Open the CSV file for writing TLE data
        with open(self.file_path, "w", newline='') as csvfile:
            fieldnames = [
                "Satellite_ID", "Line1", "Line2", "Inclination", "RAAN", "Eccentricity",
                "Arg_Perigee", "Mean_Anomaly", "Mean_Motion", "Rev_Number"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(1, self.num_objects + 1):
                line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number = self.generate_geo_tle(
                    satellite_id=i)
                writer.writerow({
                    "Satellite_ID": i,
                    "Line1": line1,
                    "Line2": line2,
                    "Inclination": inclination,
                    "RAAN": raan,
                    "Eccentricity": eccentricity,
                    "Arg_Perigee": arg_perigee,
                    "Mean_Anomaly": mean_anomaly,
                    "Mean_Motion": mean_motion,
                    "Rev_Number": rev_number
                })

        print(f"TLE dataset saved to {self.file_path}")


# # Example usage
# if __name__ == "__main__":
#     # Specify the number of objects, desired directory, and timestamp
#     num_objects = 10000
#     directory = "/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user"
#     timestamp = input("Enter the epoch timestamp (format YYYY-MM-DD HH:MM:SS): ")
#
#     tle_generator = GEOTLEGenerator(num_objects, directory, timestamp)
#     tle_generator.generate_dataset()
