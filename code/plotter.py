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
    


def animate_passengers_scatter(passenger_hist, save=True, step=1):
    """
    passenger_hist: array of shape (T, R, 2)
        T = time steps
        R = rows
        col 0 = seat, col 1 = hallway
        values: 0 (empty), 1 (passenger)

    step: use every `step`-th frame to speed up saving (e.g. step=2 or 5)
    """
    T, R, C = passenger_hist.shape
    assert C == 2, "Expected 2 columns: [seat, hallway]"

    # Optionally subsample frames for speed
    frame_indices = np.arange(0, T, step)

    fig, ax = plt.subplots(figsize=(5, 8))

    # --- Background: all possible positions (seat + hallway) ---
    # x = 0 for seat, x = 1 for hallway
    xs_all = np.array([0, 1] * R)
    ys_all = np.repeat(np.arange(R), 2)

    ax.scatter(xs_all, ys_all, s=10, alpha=0.2, marker="s")

    # --- Foreground: passengers ---
    # Two scatters: one for seat passengers, one for hallway passengers
    scat_seat = ax.scatter([], [], s=40, marker="o", label="Seat")
    scat_aisle = ax.scatter([], [], s=40, marker="x", label="Hallway")

    # Axes formatting
    ax.set_xlim(-0.5, 1.5)          # two columns: 0 (seat), 1 (aisle)
    ax.set_ylim(R - 0.5, -0.5)      # invert y so row 0 is at the top
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Seat", "Hallway"])
    ax.set_ylabel("Row index")
    ax.set_title("Passenger positions over time")
    ax.set_aspect("equal")
    ax.legend(loc="upper right")

    def init():
        scat_seat.set_offsets(np.empty((0, 2)))
        scat_aisle.set_offsets(np.empty((0, 2)))
        return scat_seat, scat_aisle

    def update(frame_idx):
        grid = passenger_hist[frame_idx]      # shape (R, 2)

        # Seat passengers
        seat_mask = grid[:, 0] > 0
        ys_seat = np.where(seat_mask)[0]
        xs_seat = np.zeros_like(ys_seat)

        # Hallway passengers
        aisle_mask = grid[:, 1] > 0
        ys_aisle = np.where(aisle_mask)[0]
        xs_aisle = np.ones_like(ys_aisle)

        if xs_seat.size == 0:
            scat_seat.set_offsets(np.empty((0, 2)))
        else:
            scat_seat.set_offsets(np.column_stack([xs_seat, ys_seat]))

        if xs_aisle.size == 0:
            scat_aisle.set_offsets(np.empty((0, 2)))
        else:
            scat_aisle.set_offsets(np.column_stack([xs_aisle, ys_aisle]))

        ax.set_title(f"Passenger positions – t = {frame_idx}")
        return scat_seat, scat_aisle

    anim = FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=frame_indices,
        interval=50,   # ms between frames
        blit=True
    )

    plt.show()

    if save:
        anim.save(save_path + "passenger_hist_scatter.mp4", fps=1000/50)