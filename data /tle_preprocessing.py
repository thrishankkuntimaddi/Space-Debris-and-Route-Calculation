import pandas as pd
import numpy as np


def load_data(filepath):
    """Loads TLE data from a CSV file."""
    return pd.read_csv(filepath)


def analyze_data(data):
    """Analyzes data for missing values and duplicates."""
    missing = data.isnull().sum()
    duplicates = data.duplicated().sum()
    return missing, duplicates


def fill_missing_values(data):
    """Fills missing values to maintain data consistency without dropping rows."""
    # Convert columns to numeric where applicable, coercing errors to NaN for proper handling
    data['4'] = pd.to_numeric(data['4'], errors='coerce')  # Epoch Year and Day
    data['5'] = pd.to_numeric(data['5'], errors='coerce')  # 1st Derivative of Mean Motion
    data['6'] = pd.to_numeric(data['6'], errors='coerce')  # 2nd Derivative of Mean Motion
    data['7'] = pd.to_numeric(data['7'], errors='coerce')  # BSTAR Drag Term
    data['9'] = pd.to_numeric(data['9'], errors='coerce')  # Element Set Number

    # Fill numerical columns with median
    data['4'] = data['4'].fillna(data['4'].median())
    data['5'] = data['5'].fillna(data['5'].median())
    data['6'] = data['6'].fillna(data['6'].median())
    data['7'] = data['7'].fillna(data['7'].median())
    data['9'] = data['9'].fillna(data['9'].median())

    return data


def merge_duplicates(data):
    """Merges duplicates by averaging numerical values and keeping consistent categorical values."""
    # Group by relevant columns and aggregate numerical columns by mean
    data_grouped = data.groupby(['2', '3', '4', '5', '6', '7', '9'], as_index=False).agg({
        '8': 'mean'  # Averaging mean motion for duplicate entries
    })
    return data_grouped


def reformat_to_tle(data):
    """Reformats data to a structured CSV format with each entry in a single row."""
    # Ensure column '1' exists and convert it to numeric for filtering
    data['1'] = pd.to_numeric(data['1'], errors='coerce')
    line1_data = data[data['1'] == 1].reset_index(drop=True)
    line2_data = data[data['1'] == 2].reset_index(drop=True)

    tle_data = pd.DataFrame({
        "Satellite_Number": line1_data['2'],
        "International_Designator": line1_data['3'],
        "Epoch_Year_and_Day": line1_data['4'],
        "1st_Derivative_Mean_Motion": line1_data['5'],
        "2nd_Derivative_Mean_Motion": line1_data['6'],
        "BSTAR_Drag_Term": line1_data['7'],
        "Ephemeris_Type": line1_data['1'],
        "Element_Set_Number": line1_data['9'],
        "Inclination_deg": line2_data['3'],
        "RAAN_deg": line2_data['4'],
        "Eccentricity": line2_data['5'],
        "Argument_of_Perigee_deg": line2_data['6'],
        "Mean_Anomaly_deg": line2_data['7'],
        "Mean_Motion": line2_data['8'],
        "Revolution_Number_at_Epoch": line2_data['2']
    })
    return tle_data


def save_to_csv(data, filepath):
    """Saves the structured TLE data to a CSV file."""
    data.to_csv(filepath, index=False)


def process_tle_file(input_path, output_path):
    """Processes a TLE file by loading, cleaning, reformatting, and saving it."""
    data = load_data(input_path)
    missing, duplicates = analyze_data(data)
    print("Missing values:", missing)
    print("Duplicate rows:", duplicates)

    data_filled = fill_missing_values(data)
    data_merged = merge_duplicates(data_filled)
    structured_tle = reformat_to_tle(data_merged)
    save_to_csv(structured_tle, output_path)
    print(f"TLE data successfully processed and saved to {output_path}")


# Run with paths for the input and output CSV files
if __name__ == "__main__":
    input_file = "/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/2024-10-24--2024-10-25-Previous.csv"
    output_file = "/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/preprocessed.csv"
    process_tle_file(input_file, output_file)
