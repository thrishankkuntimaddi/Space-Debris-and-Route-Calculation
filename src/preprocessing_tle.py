import pandas as pd

def create_tle_dataset(file_path):
    df_tle_new = pd.read_csv(file_path)

    tle_data_cleaned = {
        "Object_ID": df_tle_new.iloc[::2, 1].values,  # Object ID from first line
        "x": pd.to_numeric(df_tle_new.iloc[::2, 3].values, errors='coerce'),
        # Epoch (approximating as initial x position)
        "y": pd.to_numeric(df_tle_new.iloc[1::2, 3].values, errors='coerce'),
        # Inclination (approximating as y position)
        "z": pd.to_numeric(df_tle_new.iloc[1::2, 4].values, errors='coerce'),
        # Eccentricity (approximating as z position)
        "vx": pd.to_numeric(df_tle_new.iloc[1::2, 5].values, errors='coerce'),
        # Argument of perigee (approximating as vx)
        "vy": pd.to_numeric(df_tle_new.iloc[1::2, 6].values, errors='coerce'),
        # Right ascension of ascending node (approximating as vy)
        "vz": pd.to_numeric(df_tle_new.iloc[1::2, 7].values, errors='coerce'),  # Mean anomaly (approximating as vz)
    }

    df_tle = pd.DataFrame(tle_data_cleaned)
    return df_tle

