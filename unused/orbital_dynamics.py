purpose = '''
preload: preprocessed, clean, balanced data which is suitable for orbital dynamics 
inputs: dataset, Timestamp 
outputs: space object, Future position, Future Velocity, co-ordinates(x, y, z) } as a dataset  
'''

import pandas as pd
import numpy as np
import skyfield.api as sf
from datetime import datetime
import os
from skyfield.api import utc
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OrbitalDynamics:
    def __init__(self, timestamp,
                 tle_dataset="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/preprocessed_tle_dataset.csv",
                 output_directory="/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets"):
        self.timestamp = timestamp
        self.tle_dataset = pd.read_csv(tle_dataset)
        self.output_directory = output_directory
        self.invalid_entries = []  # Track invalid entries for analysis

    def validate_tle_lines(self, line1, line2):
        """
        Validate the TLE lines to ensure they are formatted correctly.
        Args:
            line1 (str): The first line of the TLE data.
            line2 (str): The second line of the TLE data.
        Returns:
            bool: True if both lines are valid, False otherwise.
        """
        if len(line1) != 69 or len(line2) != 69:
            return False
        return True

    def calculate_future_positions(self):
        """
        Calculate future positions, velocities, and other essential parameters for space objects.

        Returns:
            pd.DataFrame: Dataset with future positions, velocities, and other essential information.
        """
        # Load TLE data into Skyfield for orbital calculations
        ts = sf.load.timescale()
        t = ts.utc(datetime.strptime(self.timestamp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc))

        future_data = []
        for index, row in self.tle_dataset.iterrows():
            line1, line2 = str(row['line1']).strip(), str(row['line2']).strip()
            if not line1 or not line2 or pd.isna(line1) or pd.isna(line2):
                logging.warning(f"Skipping invalid TLE lines at index {index} (Missing values)")
                self.invalid_entries.append(index)
                continue  # Skip rows with invalid TLE lines

            # Validate the format of TLE lines
            if not self.validate_tle_lines(line1, line2):
                logging.warning(
                    f"Skipping invalid TLE lines at index {index} (Incorrect format): Line1: '{line1}', Line2: '{line2}'")
                self.invalid_entries.append(index)
                continue

            try:
                satellite = sf.EarthSatellite(line1, line2, name=row.get('object_name', f'object_{index}'))
                geocentric = satellite.at(t)
                position = geocentric.position.km
                velocity = geocentric.velocity.km_per_s

                # Validate position and velocity values
                if any(np.isnan(position)) or any(np.isnan(velocity)):
                    logging.warning(f"Skipping satellite at index {index} due to invalid position or velocity values")
                    self.invalid_entries.append(index)
                    continue

                future_data.append({
                    'object_name': satellite.name,
                    'x': position[0],
                    'y': position[1],
                    'z': position[2],
                    'vx': velocity[0],
                    'vy': velocity[1],
                    'vz': velocity[2]
                })
            except (ValueError, AttributeError) as e:
                logging.error(f"Error processing satellite at index {index}: {e}")
                self.invalid_entries.append(index)
                continue

        future_positions_df = pd.DataFrame(future_data)

        # Save the future positions dataset to the selected directory
        output_path = os.path.join(self.output_directory, 'future_positions.csv')
        if future_positions_df.empty:
            logging.error("No valid future positions were calculated. The output dataset is empty.")
        else:
            future_positions_df.to_csv(output_path, index=False)
            logging.info(f"Future positions dataset saved to {output_path}")

        # Log invalid entries for further analysis
        if self.invalid_entries:
            logging.info(f"Total invalid entries skipped: {len(self.invalid_entries)}. Indices: {self.invalid_entries}")

        return future_positions_df


# Example usage
if __name__ == "__main__":
    timestamp = "2024-10-28 12:00:00"
    orbital_dynamics = OrbitalDynamics(timestamp)
    future_positions = orbital_dynamics.calculate_future_positions()
    print(future_positions.head())