#import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgb
import os
from pymediainfo import MediaInfo


fps = 15
duration_per_stage = 2.0
rotation_speed_deg_per_sec = 18.0
points_per_arm = 40

arm_colors = [
    '#ff0040', '#ff8800', '#ddff00', '#00ff88',
    '#0088ff', '#6600ff', '#ff00aa', '#ff0066'
]

total_stages = 4
total_growth_time = duration_per_stage * (total_stages - 1)
total_time = total_growth_time + 3.0
frames = int(total_time * fps)

#This sets 4 inch resolution, the lower, the tighter the arms: 
fig, ax = plt.subplots(figsize=(5, 5), facecolor='black')
ax.set_aspect('equal')
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.axis('off')

scatter = ax.scatter([], [], s=[], c='white', alpha=0.78)



def init():

    scatter.set_offsets(np.empty((0, 2)))

    scatter.set_sizes([])

    scatter.set_facecolors(np.empty((0, 4)))

    return scatter,



def update(frame):
    t = frame / fps
    n_arms = 0
    if t >= duration_per_stage:
        n_arms = 3
    if t >= 2 * duration_per_stage:
        n_arms = 6
    if t >= 3 * duration_per_stage:
        n_arms = 8  # reduced from 12 to make smaller

    if n_arms == 0:
        scatter.set_offsets([[0, 0]])
        scatter.set_sizes([40]) # Keeping original size for now
        scatter.set_facecolors([[1,1,1]]) # RGB for white
        return scatter,
    else:
        growth_t = t - duration_per_stage
        growth = np.clip(growth_t / total_growth_time, 0, 1)
        growth = min(growth, 1.0)

        theta_max = 6.0
        theta = np.linspace(0.05, theta_max, points_per_arm)

        r = theta * 0.18 * growth

        rot = np.deg2rad(rotation_speed_deg_per_sec * max(0, t - duration_per_stage))

        x_all, y_all, sizes_all, colors_all = [], [], [], []

        theta_offsets = np.linspace(0, 2 * np.pi, n_arms, endpoint=False)

        for i in range(n_arms):
            theta_rot = theta + theta_offsets[i] + rot

            xi = r * np.cos(theta_rot)
            yi = r * np.sin(theta_rot)

            sizes_for_current_arm = (2.5 + 28 * (r / (theta_max * 0.18 + 1e-6))) * 1.4

            x_all.extend(xi)
            y_all.extend(yi)
            sizes_all.extend(sizes_for_current_arm.tolist())

            col = arm_colors[i % len(arm_colors)]
            colors_all.extend([col] * len(xi))

        offsets = np.column_stack((x_all, y_all)) if x_all else np.empty((0, 2))
        sizes = sizes_all if sizes_all else []
        rgb_colors = np.array([to_rgb(c) for c in colors_all]) if colors_all else np.empty((0, 3)) # Use RGB directly

    scatter.set_offsets(offsets)
    scatter.set_sizes(sizes)
    scatter.set_facecolors(rgb_colors) # Use RGB directly

    return scatter,

ani = animation.FuncAnimation(
    fig, update, init_func=init, frames=frames,
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
            
            

#print(f"Exists?", os.path.exists('tiny_spiral.gif'))
