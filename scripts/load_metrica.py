import pandas as pd

def load_metrica_tracking(filepath):
    raw = pd.read_csv(filepath, header=None, low_memory=False)

    team_row = raw.iloc[0]
    jersey_row = raw.iloc[1]
    coord_row = raw.iloc[2]

    columns = []
    for team, number, coord in zip(team_row, jersey_row, coord_row):
        if pd.isna(team) or pd.isna(number) or pd.isna(coord):
            columns.append(None)
        else:
            try:
                number_clean = str(int(float(number)))
                columns.append(f"{team}_{number_clean}_{coord}")
            except (ValueError, TypeError):
                columns.append(None)

    columns[:3] = ["Period", "Frame", "Time [s]"]

    df = raw.iloc[3:].copy()
    df.columns = columns
    df = df.reset_index(drop=True)
    df = df.apply(pd.to_numeric, errors='coerce')

    return df


