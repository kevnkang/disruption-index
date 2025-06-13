from Metrica_IO import tracking_data, to_metric_coordinates

DATADIR = '../data/metrica-tracking-data'  # or wherever your Sample_Game_1 folder is
game_id = 1  # NOT 'Sample_Game_1' — just the number 1

# Load tracking data from raw CSVs
tracking_home = tracking_data(DATADIR, game_id, 'Home')
tracking_away = tracking_data(DATADIR, game_id, 'Away')

# Convert to metric coordinates
tracking_home = to_metric_coordinates(tracking_home)
tracking_away = to_metric_coordinates(tracking_away)



