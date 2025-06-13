import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np

# === CONFIG ===
home_file = "tracking_home_fixed.csv"
away_file = "tracking_away_fixed.csv"
center_frame = 62792
frame_window = 300  # 300 before, 300 after
output_image = "decoy_run_snapshots.png"
output_video = "decoy_run_animation.mp4"

# === LOAD & CLEAN ===
home_df = pd.read_csv(home_file)
away_df = pd.read_csv(away_file)

home_df = home_df[home_df['Frame'] != 'Frame'].copy()
away_df = away_df[away_df['Frame'] != 'Frame'].copy()
home_df['Frame'] = home_df['Frame'].astype(int)
away_df['Frame'] = away_df['Frame'].astype(int)

clip_home = home_df[(home_df['Frame'] >= center_frame - frame_window) & (home_df['Frame'] <= center_frame + frame_window)].copy()
clip_away = away_df[(away_df['Frame'] >= center_frame - frame_window) & (away_df['Frame'] <= center_frame + frame_window)].copy()

# === HELPERS ===
def get_player_positions(df, frame):
    row = df[df['Frame'] == frame]
    positions = []
    for col in df.columns[3:]:  # Assuming cols 0-2 are Period, Frame, Time [s]
        try:
            val = float(row[col].values[0])
            positions.append(val)
        except:
            positions.append(np.nan)
    return np.array(positions).reshape(-1, 2)

def draw_pitch(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor('green')
    ax.plot([0.5, 0.5], [0, 1], color='white')
    center_circle = plt.Circle((0.5, 0.5), 0.09, color='white', fill=False)
    ax.add_patch(center_circle)
    ax.add_patch(Rectangle((0.0, 0.2), 0.1, 0.6, edgecolor='white', facecolor='none'))
    ax.add_patch(Rectangle((0.9, 0.2), 0.1, 0.6, edgecolor='white', facecolor='none'))
    ax.set_xticks([])
    ax.set_yticks([])

# === STATIC SNAPSHOTS ===
snapshot_frames = list(range(center_frame - frame_window, center_frame, 60))  # every ~2.4s
fig, axs = plt.subplots(1, len(snapshot_frames), figsize=(16, 4))
for i, frame in enumerate(snapshot_frames):
    ax = axs[i]
    draw_pitch(ax)
    home_pos = get_player_positions(clip_home, frame)
    away_pos = get_player_positions(clip_away, frame)
    ax.scatter(home_pos[:, 0], home_pos[:, 1], c='blue', s=20)
    ax.scatter(away_pos[:, 0], away_pos[:, 1], c='red', s=20)
    ax.set_title(f"Frame {frame}")
plt.tight_layout()
plt.savefig(output_image)
plt.close()

# === ANIMATION ===
fig, ax = plt.subplots(figsize=(8, 5))
draw_pitch(ax)
home_dots, = ax.plot([], [], 'bo', markersize=5)
away_dots, = ax.plot([], [], 'ro', markersize=5)

def init():
    home_dots.set_data([], [])
    away_dots.set_data([], [])
    return home_dots, away_dots

frames_range = list(range(center_frame - frame_window, center_frame))

def animate(i):
    frame = frames_range[i]
    home_pos = get_player_positions(clip_home, frame)
    away_pos = get_player_positions(clip_away, frame)
    home_dots.set_data(home_pos[:, 0], home_pos[:, 1])
    away_dots.set_data(away_pos[:, 0], away_pos[:, 1])
    ax.set_title(f"Frame {frame}")
    return home_dots, away_dots

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(frames_range), interval=50, blit=True)
ani.save(output_video, writer='ffmpeg')
plt.close()

print(f"✅ Saved: {output_image} and {output_video}")
