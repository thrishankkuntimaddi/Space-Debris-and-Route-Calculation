import os
import pandas as pd
import numpy as np


def preprocess_and_format_tle(input_csv_path, output_directory):
    # Load dataset from input path
    data = pd.read_csv(input_csv_path, dtype=str)

    # Rename columns to ensure correct mapping if they are not named numerically
    data.columns = [str(i) for i in range(1, len(data.columns) + 1)]

    # Step 1: Filling missing values based on column data types and importance
    # Convert columns to numeric where necessary, handling errors by coercing invalid values to NaN
    data['4'] = pd.to_numeric(data['4'], errors='coerce')
    data['8'] = pd.to_numeric(data['8'], errors='coerce')
    data['9'] = pd.to_numeric(data['9'], errors='coerce')

    # Fill missing numerical values with median or interpolated values where applicable
    data['4'] = data['4'].fillna(data['4'].median())  # Epoch Year and Day
    data['5'] = data['5'].fillna('00000-0')  # Default value for mixed type column
    data['6'] = data['6'].fillna('00000-0')  # BSTAR Drag Term (fill with common default)
    data['7'] = data['7'].fillna(data['7'].mode()[0])  # Use mode for drag where default values apply
    data['8'] = data['8'].interpolate(method='linear', limit_direction='forward', axis=0)  # Interpolate for mean motion
    data['9'] = data['9'].fillna(9990)  # Fill missing values in column '9' with a common valid entry

    # Step 2: Split data into Line 1 and Line 2 segments
    # Ensure data in column '1' is of type string for correct comparison
    data['1'] = data['1'].astype(str)
    line1_data = data[data['1'] == '1'].reset_index(drop=True)
    line2_data = data[data['1'] == '2'].reset_index(drop=True)

    # Ensure that both Line 1 and Line 2 have the same number of entries
    min_length = min(len(line1_data), len(line2_data))
    line1_data = line1_data.iloc[:min_length]
    line2_data = line2_data.iloc[:min_length]

    # Step 3: Reformat data to TLE format
    tle_formatted = []
    for i in range(len(line1_data)):
        # Line 1 TLE
        line1 = f"1 {line1_data['2'][i]:<5} {line1_data['3'][i]:<8} {line1_data['4'][i]:<14.8f} {line1_data['5'][i]:<10} {line1_data['6'][i]:<8} {line1_data['7'][i]:<8} {int(float(line1_data['9'][i])):04d}"

        # Line 2 TLE
        line2 = f"2 {line2_data['2'][i]:<5} {line2_data['3'][i]:<8} {line2_data['4'][i]:<7} {line2_data['5'][i]:<8} {line2_data['6'][i]:<8} {line2_data['7'][i]:<8} {line2_data['8'][i]}"

        # Append both lines as a TLE entry
        tle_formatted.append(line1)
        tle_formatted.append(line2)

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define output file path
    output_file_path = os.path.join(output_directory, 'Preprocessed_Balanced_TLE_File.txt')

    # Save the formatted TLE data to the output directory
    with open(output_file_path, 'w') as file:
        if tle_formatted:  # Ensure there is data to write
            file.write("\n".join(tle_formatted))
        else:
            file.write("No valid TLE data found.")

    print(f"TLE file saved successfully at: {output_file_path}")


def convert_tle_txt_to_csv(input_txt_path, output_csv_path):
    # Load TLE text file
    with open(input_txt_path, 'r') as file:
        lines = file.readlines()

    # Process lines into structured data
    data = []
    for i in range(0, len(lines), 2):
        if i + 1 < len(lines):
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()

            # Parse line 1
            line1_data = [
                line1[0],  # Line number
                line1[2:7].strip(),  # Satellite number
                line1[9:17].strip(),  # International designator
                line1[18:32].strip(),  # Epoch year and day
                line1[33:43].strip(),  # First derivative of mean motion
                line1[44:52].strip(),  # Second derivative of mean motion
                line1[53:61].strip(),  # BSTAR drag term
                line1[62:63].strip(),  # Ephemeris type
                line1[64:68].strip(),  # Element set number
            ]

            # Parse line 2
            line2_data = [
                line2[0],  # Line number
                line2[2:7].strip(),  # Satellite number
                line2[8:16].strip(),  # Inclination (degrees)
                line2[17:25].strip(),  # RAAN (degrees)
                line2[26:33].strip(),  # Eccentricity (decimal)
                line2[34:42].strip(),  # Argument of perigee (degrees)
                line2[43:51].strip(),  # Mean anomaly (degrees)
                line2[52:63].strip(),  # Mean motion (revolutions per day)
                line2[63:68].strip(),  # Revolution number at epoch
            ]

            # Append parsed line data to main data list
            data.append(line1_data + line2_data)

    # Define column names
    columns = [
        'Line1_Num', 'Satellite_Num', 'Intl_Designator', 'Epoch_Year_Day', 'First_Derivative',
        'Second_Derivative', 'BSTAR', 'Ephemeris_Type', 'Element_Set_Num',
        'Line2_Num', 'Satellite_Num_2', 'Inclination_deg', 'RAAN_deg', 'Eccentricity',
        'Argument_of_Perigee_deg', 'Mean_Anomaly_deg', 'Mean_Motion', 'Rev_at_Epoch'
    ]

    # Convert to DataFrame
    tle_df = pd.DataFrame(data, columns=columns)

    # Save DataFrame to CSV
    tle_df.to_csv(output_csv_path, index=False)
    print(f"CSV file saved successfully at: {output_csv_path}")


# Example usage
preprocess_and_format_tle('/Users/thrishank/Desktop/2024-10-24--2024-10-25-Previous.csv',
                          '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user')
convert_tle_txt_to_csv(
    '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/choice_of_tle_by_user/Preprocessed_Balanced_TLE_File.txt',
    '/Users/thrishank/Documents/Projects/Project_Space_Debris_&_Route_Calculation/Space-Debris-and-Route-Calculation/datasets/tle_data.csv')
