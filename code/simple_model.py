import numpy as np
from tqdm import tqdm

class SimplestPassengerModel():
    
    def __init__(self, rows, seat_cols_each_side, time_steps):
        """Baseline plane passenger exit model

        Args:
            rows (int): Number of rows in the plane.
            self.seat_cols_each_side (int): Number of columns of seats on each side of the hallway.
            time_steps (int): Time steps to run the simulation for.
        """
        self.rows = rows
        self.time_steps = time_steps
        self.seat_cols_each_side = seat_cols_each_side
        self.cols = 2 * self.seat_cols_each_side + 1  # 2 sets of seats plus the hallway in the middle
        self.left_seat_cols = np.arange(self.seat_cols_each_side)
        self.right_seat_cols = np.arange(self.seat_cols_each_side + 1, 2 * self.seat_cols_each_side + 1)
        self.hallway_col = self.seat_cols_each_side
        
        
    def _initialize_passengers(self):
        # All passengers start seated
        self.passengers = np.zeros((self.rows, self.cols))
        self.passengers[:, self.left_seat_cols] = 1
        self.passengers[:, self.right_seat_cols] = 1
        

    def _initialize_history_arrays(self):
        self.passengers_history = np.zeros((self.rows, self.cols, self.time_steps))  # Has to be 0s as may stop before all time steps have been taken.


    def _store_hist_values(self, time_index):
        self.passengers_history[:, :, time_index] = self.passengers * 1

    
    def _move_from_seat(self, x, y):
            # Seated in left seats
            if (y in self.left_seat_cols) and (self.passengers[x, y + 1] == 0):
                self.passengers[x, y] = 0
                self.passengers[x, y + 1] = 1
            
            # Seated in right seats
            elif (y in self.right_seat_cols) and (self.passengers[x, y - 1] == 0):
                self.passengers[x, y] = 0
                self.passengers[x, y - 1] = 1
        
    
    def _move_in_hallway(self, x, y):
        # Standing in the hallway
        if y == self.hallway_col:
            # If the chosen site is at the exit, remove the passenger
            if x == self.rows - 1:
                self.passengers[x, y] = 0
            else:
                if self.passengers[x + 1, y] == 0:
                    self.passengers[x, y] = 0
                    self.passengers[x + 1, y] = 1
    
    
    def _update(self):
        for _ in range(2 * self.seat_cols_each_side):
            x = np.random.randint(0, self.rows)
            y = np.random.randint(0, self.cols)
            
            # Check if there is a passenger at the chosen site
            if self.passengers[x, y] == 0:
                continue
            
            self._move_from_seat(x, y)
            self._move_in_hallway(x, y)
            
        
    def _simulate(self):
        # Setup
        self._initialize_passengers()
        self._initialize_history_arrays()
        self._store_hist_values(time_index=0)  # Store initial values
        
        # Continue until there are not more passengers or the max steps have been taken
        N_remaining_passengers = np.sum(self.passengers)
        self.time_steps_taken = 0
        while (self.time_steps_taken < self.time_steps - 1) and (N_remaining_passengers > 0):
            # Perform passenger update
            self._update()
            # Update loop metrics
            self.time_steps_taken += 1
            N_remaining_passengers = np.sum(self.passengers)
            # Store values
            self._store_hist_values(self.time_steps_taken)

        # If no remaining passengers, remove the remaining parts of passengers_history
        if N_remaining_passengers == 0:
            self.passengers_history = self.passengers_history[:, :, :self.time_steps_taken+1]
        else:
            print(f"Warning, reached {self.time_steps_taken} / {self.time_steps} time steps")
        

    def store_values(self, filename=""):
        # Simulate
        self._simulate()
        np.savez(f"./data/{filename}_model", self.passengers_history)
        print(f"Saved {filename}")
        
    
    def store_time_taken(self, N_repeat, filename=""):
        # Run the simulation N_repeat times
        times = np.empty(N_repeat)
        for i in tqdm(range(N_repeat)):
            self._simulate()
            times[i] = self.time_steps_taken
        np.savez(f"./data/{filename}_times_N{N_repeat}", times)
        print(f"Finished saving times to {filename} with N={N_repeat}")