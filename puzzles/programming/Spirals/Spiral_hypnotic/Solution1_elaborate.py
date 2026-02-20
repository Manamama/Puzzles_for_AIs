import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgb

# ────────────────────────────────────────────────
# Parameters
# ────────────────────────────────────────────────
fps = 30
duration_per_stage = 4.0          # seconds per growth phase (before adding new arms)
rotation_speed_deg_per_sec = 18.0 # calm hypnotic speed (~20 s per full rotation)
points_per_arm = 140

arm_colors = [
    '#ff0040', '#ff8800', '#ddff00', '#00ff88',
    '#0088ff', '#6600ff', '#ff00aa', '#ff0066',
    '#ff4400', '#88ff00', '#00ffcc', '#0044ff'
]

# ────────────────────────────────────────────────
# Timing & stages
# ────────────────────────────────────────────────
total_stages = 4  # center → 3 → 6 → 12 arms
total_growth_time = duration_per_stage * (total_stages - 1)
total_time = total_growth_time + 12.0  # extra pure-rotation time before loop
frames = int(total_time * fps)

# ────────────────────────────────────────────────
# Figure setup
# ────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
ax.set_aspect('equal')
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.05, 1.05)
ax.axis('off')

scatter = ax.scatter([], [], s=[], c='white', alpha=0.75)

# ────────────────────────────────────────────────
# Helper to determine number of arms at time t
# ────────────────────────────────────────────────
def get_n_arms(t):
    if t < duration_per_stage:
        return 0
    elif t < 2 * duration_per_stage:
        return 3
    elif t < 3 * duration_per_stage:
        return 6
    else:
        return 12

# ────────────────────────────────────────────────
# Update function
# ────────────────────────────────────────────────
def update(frame):
    t = frame / fps
    n_arms = get_n_arms(t)

    if n_arms == 0:
        # Initial single white dot at center
        scatter.set_offsets([[0, 0]])
        scatter.set_sizes([60])
        scatter.set_facecolors([[1,1,1]])  # white
        return scatter,

    # ── Global growth progress (never resets) ──
    growth_t = t - duration_per_stage               # start growth after first stage
    growth = np.clip(growth_t / total_growth_time, 0, 1)

    # When we reach full growth, keep it at 1 (pure rotation phase)
    growth = min(growth, 1.0)

    # Spiral parameters (gentle wide spiral)
    theta_max = 6.0          # ~0.95 turns at full growth
    theta = np.linspace(0.05, theta_max, points_per_arm)

    r = theta * 0.18 * growth   # scale radius with growth

    # Rotation (continuous from moment arms appear)
    rot = np.deg2rad(rotation_speed_deg_per_sec * max(0, t - duration_per_stage))

    x_all, y_all, sizes_all, colors_all = [], [], [], []

    theta_offsets = np.linspace(0, 2 * np.pi, n_arms, endpoint=False)

    for i in range(n_arms):
        theta_rot = theta + theta_offsets[i] + rot

        xi = r * np.cos(theta_rot)
        yi = r * np.sin(theta_rot)

        # Size increases with radius (stronger effect near tips)
        size_factor = 2.5 + 28 * (r / (theta_max * 0.18 + 1e-6))
        sizes_i = size_factor * 1.4

        x_all.extend(xi)
        y_all.extend(yi)
        sizes_all.extend(sizes_i)

        # Color per arm (cycled if >12, but we have exactly 12)
        col = arm_colors[i % len(arm_colors)]
        colors_all.extend([col] * len(xi))

    # Update scatter
    scatter.set_offsets(np.column_stack((x_all, y_all)))
    scatter.set_sizes(sizes_all)

    rgb_colors = np.array([to_rgb(c) for c in colors_all])
    scatter.set_facecolors(rgb_colors)

    return scatter,

# ────────────────────────────────────────────────
# Create & run animation
# ────────────────────────────────────────────────
ani = animation.FuncAnimation(
    fig, update, frames=frames,
    interval=1000/fps, blit=False, repeat=True
)

#plt.show()

# To save (requires ffmpeg installed):
#ani.save('fixed_spiral_arms_growth.mp4', writer='ffmpeg', fps=fps, dpi=120)

#This seems to OOM stuff, as '-rw-rw-r--   1 zezen zezen 52450015 Feb 16 11:36  fixed_spiral_arms_growth.2.gif' : 
ani.save('fixed_spiral_arms_growth.2.gif', writer='pillow', fps=fps, dpi=120)
