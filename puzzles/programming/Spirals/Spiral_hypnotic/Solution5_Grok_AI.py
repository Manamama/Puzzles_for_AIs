import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgb
import os
from pymediainfo import MediaInfo


# ── Parameters ──────────────────────────────────────────────────
fps                  = 30
duration_per_stage   = 1.2           # longer → dot visible longer, gentler build
rotation_speed_deg_per_sec = 10.0    # very calm hypnotic feel
points_per_arm       = 70            # denser for smoother arms

arm_colors = [
    '#ff0040', '#ff8800', '#ddff00', '#00ff88',
    '#0088ff', '#6600ff', '#ff00aa', '#ff0066',
    '#ff4400', '#88ff00', '#00ffcc', '#0044ff'
]

total_stages     = 4
total_growth_time = duration_per_stage * (total_stages - 1)
total_time       = total_growth_time + 3.0
frames           = 180

# ── Figure ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(3, 3), facecolor='black')
ax.set_aspect('equal')
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.axis('off')

scatter = ax.scatter([], [], s=[], c='white', alpha=0.88)

# ── Helpers ─────────────────────────────────────────────────────
def get_n_arms(t):
    if t < duration_per_stage:          return 0
    elif t < 2 * duration_per_stage:    return 3
    elif t < 3 * duration_per_stage:    return 6
    else:                               return 12

def update(frame):
    t = frame / fps
    n_arms = get_n_arms(t)

    if n_arms == 0:
        scatter.set_offsets([[0, 0]])
        scatter.set_sizes([65])
        scatter.set_facecolors([[1,1,1]])
        return scatter,

    growth_t = t - duration_per_stage
    growth   = min(np.clip(growth_t / total_growth_time, 0, 1), 1.0)

    theta_max = 6.2                  # slightly wider spiral
    theta     = np.linspace(0.04, theta_max, points_per_arm)

    r = theta * 0.175 * growth       # 0.175 → bit tighter than 0.18

    rot = np.deg2rad(rotation_speed_deg_per_sec * max(0, t - duration_per_stage))

    x_all, y_all, sizes_all, colors_all = [], [], [], []

    theta_offsets = np.linspace(0, 2 * np.pi, n_arms, endpoint=False)

    for i in range(n_arms):
        theta_rot = theta + theta_offsets[i] + rot
        xi = r * np.cos(theta_rot)
        yi = r * np.sin(theta_rot)

        # size grows stronger toward tips
        size_factor = 2.8 + 32 * (r / (theta_max * 0.175 + 1e-6))
        sizes_i = size_factor * 1.35

        x_all.extend(xi)
        y_all.extend(yi)
        sizes_all.extend(sizes_i)
        col = arm_colors[i % len(arm_colors)]
        colors_all.extend([col] * len(xi))

    scatter.set_offsets(np.column_stack((x_all, y_all)))
    scatter.set_sizes(sizes_all)
    rgb_colors = np.array([to_rgb(c) for c in colors_all])
    scatter.set_facecolors(rgb_colors)

    return scatter,

# ── Animation & Save ────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig, update, frames=frames,
    interval=1000/fps, blit=False, repeat=True
)


file_path='tiny_spiral.gif'
file_path='tiny_spiral.mp4'

#This sets DPI:
#ani.save(file_path, writer='pillow', dpi=400)
ani.save(file_path, writer='ffmpeg', dpi=400)

#So: pixel_width  = figsize_width  × dpi, pixel_height = figsize_height × dpi


print(f"Saved {file_path}")

media_info = MediaInfo.parse(file_path)




for track in media_info.tracks:
    print(f"\nTrack type: {track.track_type}")
    for attr, value in track.to_data().items():
        if value is not None:
            print(f"{attr}: {value}")
            
            
