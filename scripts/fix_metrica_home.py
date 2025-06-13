import pandas as pd
import numpy as np

def fix_home_tracking(input_path, output_path):
    raw = pd.read_csv(input_path, header=None, low_memory=False)
    data = raw.iloc[3:].reset_index(drop=True)

    num_columns = data.shape[1]
    column_names = ["Period", "Frame", "Time [s]"]

    player_index = 1
    while len(column_names) < num_columns:
        column_names.append(f"Home_{player_index}_x")
        if len(column_names) == num_columns:
            break
        column_names.append(f"Home_{player_index}_y")
        player_index += 1

    data.columns = column_names
    data = data.apply(pd.to_numeric, errors='coerce')
    data.to_csv(output_path, index=False)
    print(f"✅ Saved cleaned file to {output_path}")


if __name__ == "__main__":
    input_file = "../data/metrica-tracking-data/Sample_Game_1/Sample_Game_1_RawTrackingData_Home_Team.csv"
    output_file = "tracking_home_fixed.csv"
    fix_home_tracking(input_file, output_file)
