import random
from datetime import datetime, timedelta
import os
import csv


class LEOTLEGenerator:
    def __init__(self, num_objects, directory, timestamp):
        self.num_objects = num_objects
        self.directory = directory
        self.timestamp = timestamp
        self.epoch_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%y%j")  # Current year and day of year for epoch

    def generate_tle(self, satellite_id):
        """
        Generate a TLE entry for a given satellite ID and epoch date.
        """
        # Line 1 values
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"

        # Line 2 values (random within realistic LEO parameters)
        inclination = random.uniform(0, 90)  # Inclination in degrees
        raan = random.uniform(0, 360)  # Right ascension of ascending node
        eccentricity = random.randint(0, 100000)  # Eccentricity in scientific notation
        arg_perigee = random.uniform(0, 360)  # Argument of perigee
        mean_anomaly = random.uniform(0, 360)  # Mean anomaly
        mean_motion = random.uniform(11, 15)  # Mean motion for LEO
        rev_number = random.randint(1, 99999)  # Revolution number at epoch

        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"

        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

    def generate_tle_dataset(self):
        """
        Generate a TLE dataset with the specified number of objects and save it to the desired directory.
        """
        file_path = os.path.join(self.directory, f"leo_tle_dataset.csv")

        # Check if the directory exists; if not, create it
        os.makedirs(self.directory, exist_ok=True)

        # Open the CSV file for writing TLE data
        with open(file_path, "w", newline='') as csvfile:
            fieldnames = [
                "Satellite_ID", "Line1", "Line2", "Inclination", "RAAN", "Eccentricity",
                "Arg_Perigee", "Mean_Anomaly", "Mean_Motion", "Rev_Number"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(1, self.num_objects + 1):
                line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number = self.generate_tle(
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

        print(f"TLE dataset saved to {file_path}")


# # Example usage
# if __name__ == "__main__":
#     # Specify the number of objects and desired directory
#     num_objects = 20000
#     directory = "/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user"
#     timestamp = "2024-10-28 12:00:00"
#
#     tle_generator = LEOTLEGenerator(num_objects, directory, timestamp)
#     tle_generator.generate_tle_dataset()
