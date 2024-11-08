import random
from datetime import datetime
import os
import csv

# Common directory for storing TLE data
dataset_directory = "/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user"

class DataPreparation:
    def __init__(self, timestamp, orbit_type):
        self.timestamp = timestamp
        self.orbit_type = orbit_type
        self.num_objects = int(input("Enter the number of objects: "))
        self.file_path = self.generate_tle_data()

    def generate_tle_data(self):
        if self.orbit_type == "Low Earth Orbit (LEO)":
            generator = LEOTLEGenerator(self.num_objects, dataset_directory, self.timestamp)
        elif self.orbit_type == "Medium Earth Orbit (MEO)":
            generator = MEOTLEGenerator(self.num_objects, dataset_directory, self.timestamp)
        elif self.orbit_type == "Geostationary Orbit (GEO)":
            generator = GEOTLEGenerator(self.num_objects, dataset_directory, self.timestamp)
        elif self.orbit_type == "High Earth Orbit (HEO)":
            generator = HEOTLEGenerator(self.num_objects, dataset_directory, self.timestamp)
        else:
            raise ValueError("Invalid orbit type provided.")

        generator.generate_tle_dataset()
        return generator.file_path

    # def __str__(self):
    #     return f"{self.file_path}"

class BaseTLEGenerator:
    def __init__(self, num_objects, directory, timestamp):
        self.num_objects = num_objects
        self.directory = directory
        self.timestamp = timestamp
        self.epoch_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%y%j")  # Current year and day of year for epoch
        self.file_path = os.path.join(self.directory, f"user_tle_dataset.csv")

    def get_file_prefix(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def generate_tle(self, satellite_id):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def generate_tle_dataset(self):
        # Open the CSV file for writing TLE data
        with open(self.file_path, "w", newline='') as csvfile:
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

        # print(f"TLE dataset successfully saved at: {self.file_path}")

class LEOTLEGenerator(BaseTLEGenerator):
    def get_file_prefix(self):
        return "leo"

    def generate_tle(self, satellite_id):
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"
        inclination = random.uniform(0, 90)
        raan = random.uniform(0, 360)
        eccentricity = random.randint(0, 100000)
        arg_perigee = random.uniform(0, 360)
        mean_anomaly = random.uniform(0, 360)
        mean_motion = random.uniform(11, 15)
        rev_number = random.randint(1, 99999)
        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"
        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

class MEOTLEGenerator(BaseTLEGenerator):
    def get_file_prefix(self):
        return "meo"

    def generate_tle(self, satellite_id):
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"
        inclination = random.uniform(0, 70)
        raan = random.uniform(0, 360)
        eccentricity = random.randint(0, 500000)
        arg_perigee = random.uniform(0, 360)
        mean_anomaly = random.uniform(0, 360)
        mean_motion = random.uniform(2, 6)
        rev_number = random.randint(1, 99999)
        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"
        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

class GEOTLEGenerator(BaseTLEGenerator):
    def get_file_prefix(self):
        return "geo"

    def generate_tle(self, satellite_id):
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"
        inclination = random.uniform(0, 5)
        raan = random.uniform(0, 360)
        eccentricity = random.randint(0, 10000)
        arg_perigee = random.uniform(0, 360)
        mean_anomaly = random.uniform(0, 360)
        mean_motion = 1.0027
        rev_number = random.randint(1, 99999)
        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"
        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

class HEOTLEGenerator(BaseTLEGenerator):
    def get_file_prefix(self):
        return "heo"

    def generate_tle(self, satellite_id):
        line1 = f"1 {satellite_id:05d}U 23067A   {self.epoch_date}  .00000123  00000-0  12034-4 0  9999"
        inclination = random.uniform(45, 90)
        raan = random.uniform(0, 360)
        eccentricity = random.randint(500000, 900000)
        arg_perigee = random.uniform(0, 360)
        mean_anomaly = random.uniform(0, 360)
        mean_motion = random.uniform(0.5, 2)
        rev_number = random.randint(1, 99999)
        line2 = f"2 {satellite_id:05d} {inclination:8.4f} {raan:8.4f} {eccentricity:07d} {arg_perigee:8.4f} {mean_anomaly:8.4f} {mean_motion:11.8f} {rev_number:05d}"
        return line1, line2, inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion, rev_number

# # Example usage
# if __name__ == "__main__":
#     timestamp = "2024-10-28 12:00:00"
#     orbit_type = "Low Earth Orbit (LEO)"
#     prepare = DataPreparation(timestamp, orbit_type)
#     print(f"TLE data saved in directory: {prepare.file_path}")
