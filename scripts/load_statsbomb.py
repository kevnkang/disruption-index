import json
from pathlib import Path
from collections import defaultdict
import pandas as pd

def load_match_events(events_dir: str, match_id: str) -> pd.DataFrame:
    """Load the events of a specific match and tag with match_id."""
    path = Path(events_dir) / f"{match_id}.json"
    with open(path, 'r', encoding='utf-8') as f:
        events = json.load(f)
    df = pd.json_normalize(events)
    df["match_id"] = match_id  # 🔥 Add this line
    return df


def load_all_match_ids(matches_dir: str) -> list:
    """Return a list of all match IDs from nested folders, ignoring empty/malformed files."""
    matches = []
    match_path = Path(matches_dir)
    for json_file in match_path.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for match in data:
                        if "match_id" in match:
                            matches.append(match["match_id"])
        except Exception as e:
            print(f"Skipping file {json_file} due to error: {e}")
    return matches

def load_player_minutes_and_positions(lineups_dir, match_ids):
    from pathlib import Path
    from collections import defaultdict

    player_data = defaultdict(lambda: {"minutes": 0, "positions": set()})
    
    for match_id in match_ids:
        file_path = Path(lineups_dir) / f"{match_id}.json"
        if not file_path.exists():
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for team in data:
                for player in team["lineup"]:
                    name = player["player_name"]
                    minutes = player.get("minutes", 0)
                    pos = player.get("position", {}).get("name", "")
                    player_data[name]["minutes"] += minutes
                    if pos:
                        player_data[name]["positions"].add(pos)

    # Convert to DataFrame
    rows = []
    for name, stats in player_data.items():
        rows.append({
            "player": name,
            "minutes": stats["minutes"],
            "position": ", ".join(stats["positions"])  # if multiple roles
        })

    return pd.DataFrame(rows)