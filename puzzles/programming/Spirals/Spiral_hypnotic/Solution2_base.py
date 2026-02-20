import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import hsv_to_rgb

# Parameters
fps = 30
omega = 2 * np.pi / 20  # Rotation period of 20 seconds for calm speed
b = 1.0  # Spiral constant (adjusted for gentle wide spiral)
R = 10.0  # Approximate max radius to fill frame
theta_max_full = 2 * np.pi * 1.5  # 1.5 turns for gentle spiral
b = R / theta_max_full  # Recalculate b for precision
dtheta = 0.2  # Step in theta for discrete dots (adjust for discreteness)
s0 = 5  # Base dot size (pixels)
c = 20 / R  # Size increase factor, so at r=R, size ~25
alpha_dot = 0.7  # Slight transparency for overlap

# Timing (in seconds)
t1 = 2.0  # End of initial phase
t_add_second_group = t1 + 3.0  # Add second set of arms
t_add_third_group = t_add_second_group + 3.0  # Add third set
t_full = t_add_third_group + 3.0  # Reach full extension
theta_rate = theta_max_full / (t_full - t1)  # Theta growth rate per second

# Arm angles in radians (12 arms at 30° intervals)
arm_offsets = np.arange(0, 360, 30) * np.pi / 180.0

# Colors: rainbow hues
num_arms = 12
colors = [hsv_to_rgb((k / num_arms, 1, 1)) for k in range(num_arms)]

# Arm groups
group1 = [0, 4, 8]  # 0°, 120°, 240°
group2 = [2, 6, 10]  # 60°, 180°, 300°
group3 = [1, 3, 5, 7, 9, 11]  # 30°, 90°, 150°, 210°, 270°, 330°

# Figure setup
fig = plt.figure(figsize=(8, 8), facecolor='black')
ax = plt.axes()
ax.set_facecolor('black')
ax.axis('off')
ax.set_xlim(-R * 1.1, R * 1.1)
ax.set_ylim(-R * 1.1, R * 1.1)
ax.set_aspect('equal')

scat = None
center_scat = None

def update(frame):
    global scat, center_scat
    t = frame / fps
    theta_rot = omega * t

    # Clear previous scatters
    if scat is not None:
        scat.remove()
        scat = None
    if center_scat is not None:
        center_scat.remove()
        center_scat = None

    if t < t1:
        # Initial phase: single white dot at center
        center_scat = ax.scatter(0, 0, s=s0 * 2, color='white', alpha=1.0)
        return (center_scat,)

    # Determine active arms
    if t < t_add_second_group:
        active_indices = group1
    elif t < t_add_third_group:
        active_indices = group1 + group2
    else:
        active_indices = group1 + group2 + group3

    # Current max theta (growth stops at full)
    current_theta_max = min(theta_rate * (t - t1), theta_max_full)

    # Collect all dot positions, sizes, colors
    x_all = []
    y_all = []
    s_all = []
    c_all = []

    for k in active_indices:
        arm_offset = arm_offsets[k]
        color = colors[k]

        # Thetas starting slightly off center to avoid exact overlap at r=0
        num_steps = int((current_theta_max) / dtheta) + 1
        thetas_spiral = np.linspace(dtheta / 2, current_theta_max, num_steps)

        rs = b * thetas_spiral
        thetas_pos = thetas_spiral + arm_offset + theta_rot
        xs = rs * np.cos(thetas_pos)
        ys = rs * np.sin(thetas_pos)
        sizes = s0 + c * rs

        x_all.extend(xs)
        y_all.extend(ys)
        s_all.extend(sizes)
        c_all.extend([color] * len(xs))

    # Plot all dots
    scat = ax.scatter(x_all, y_all, s=s_all, c=c_all, alpha=alpha_dot)
    return (scat,)

# Create animation (runs indefinitely with repeat)
ani = animation.FuncAnimation(fig, update, interval=1000 / fps, blit=False)


# To save as GIF (e.g., first 600 frames ~20 sec, loops on rotation phase if viewed in loop)
ani.save('pinwheel_animation.gif', writer='pillow', fps=fps)

# To display: 
plt.show()

# Note: If running in a script, uncomment plt.show() to view live instead of saving.


