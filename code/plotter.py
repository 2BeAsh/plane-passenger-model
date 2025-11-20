import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

save_path = "./images/"


def animate_passengers(passenger_hist):
    # time_steps, _, _ = passenger_hist.shape
    _, _, time_steps = passenger_hist.shape
    fig, ax = plt.subplots(figsize=(8, 10))
    
    # Initial image
    im = ax.matshow(passenger_hist[:, :, 0], cmap="Grays", vmin=0, vmax=1)
    fig.colorbar(im)
    
    def animate(i):
        im.set_array(passenger_hist[:, :, i])
    
    anim = FuncAnimation(fig, animate, interval=250, frames=time_steps)
    plt.draw()
    plt.show()
    anim.save(save_path + "passenger_hist.mp4")
    

def animate_passengers_scatter(passenger_hist, save=True, step=1, interval_ms=100, fname_add=""):
    """
    passenger_hist: array of shape (R, C, T)
        R = rows
        C = columns (any number of seat/hallway columns)
        T = time steps
        values: 0 (empty), 1 (passenger)

    step: use every `step`-th frame to speed up saving (e.g. step=2 or 5)
    """
    R, C, T = passenger_hist.shape

    # Use every `step`th time point for speed, frames are actual time indices
    frame_indices = np.arange(0, T, step)

    fig, ax = plt.subplots(figsize=(5, 8))

    # --- Background: all possible positions (static) ---
    # Full R x C grid
    xs_all, ys_all = np.meshgrid(np.arange(C), np.arange(R))  # xs: 0..C-1, ys: 0..R-1
    ax.scatter(xs_all.ravel(), ys_all.ravel(), s=12, alpha=0.2, marker="s")

    # --- Foreground: all passengers (single marker style) ---
    scat = ax.scatter([], [], s=40, color="black")

    # Axes formatting
    ax.set_xlim(-0.5, C - 0.5)
    ax.set_ylim(R - 0.5, -0.5)  # invert so row 0 is at the top
    ax.set_xticks(np.arange(C))
    # If you know which column index is hallway, you can customize labels here.
    ax.set_xticklabels([str(i) for i in range(C)], rotation=45)
    ax.set_ylabel("Row")
    ax.set_title("Passenger positions over time")
    ax.set_aspect("equal")

    def init():
        scat.set_offsets(np.empty((0, 2)))
        return scat,

    def update(t):
        # t is the actual time index from frame_indices
        grid = passenger_hist[:, :, t]       # shape (R, C)

        # Positions where there is a passenger
        rows, cols = np.where(grid == 1)     # rows: 0..R-1, cols: 0..C-1

        if rows.size == 0:
            scat.set_offsets(np.empty((0, 2)))
        else:
            coords = np.column_stack([cols, rows])  # (x, y)
            scat.set_offsets(coords)

        ax.set_title(f"Passenger positions, t = {t}")
        return scat,

    anim = FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=frame_indices,
        interval=interval_ms,   # ms between frames
        blit=True
    )

    plt.show()

    if save:
        anim.save(save_path + fname_add + "passenger_hist_scatter.mp4", fps=1000/50)
        
        
def time_distribution(times, Nbins=None):
    if Nbins is None:
        Nbins = int(np.sqrt(times.size))
    fig, ax = plt.subplots(dpi=150)
    ax.hist(times, bins=Nbins)
    ax.set(xlabel="Time steps to empty plane", ylabel="Counts")
    ax.grid()
    plt.show()