import numpy as np

class SimplestPassengerModel():
    
    def __init__(self, rows, time_steps):
        self.rows = rows
        self.time_steps = time_steps
        
        
    def _initialize_passengers(self):
        # All passengers start seated
        self.passengers = np.zeros((self.rows, 2))
        self.passengers[:, 0] = 1

    def _initialize_history_arrays(self):
        self.passengers_history = np.zeros((self.rows, 2, self.time_steps))  # Has to be 0s as may stop before all time steps have been taken.

    def _store_hist_values(self, time_index):
        self.passengers_history[:, :, time_index] = self.passengers * 1

    
    def _update(self):
        for _ in range(2 * self.rows):  # 2 columns
            x = np.random.randint(0, self.rows)
            y = np.random.randint(0, 2)
            
            if self.passengers[x, y] == 0:
                continue
            # Seated
            if y == 0:
                # If able to stand, do so. Otherwise do nothing
                if self.passengers[x, y + 1] == 0:
                    self.passengers[x, y] = 0
                    self.passengers[x, y + 1] = 1
            
            # Standing
            else:  # y == 1
                # If the chosen site is at the exit, remove the passenger
                if x == self.rows - 1:
                    self.passengers[x, y] = 0
                else:
                    if self.passengers[x + 1, y] == 0:
                        self.passengers[x, y] = 0
                        self.passengers[x + 1, y] = 1
        
    def _simulate(self):
        # Setup
        self._initialize_passengers()
        self._initialize_history_arrays()
        self._store_hist_values(time_index=0)  # Store initial values
        
        # Continue until there are not more passengers or the max steps have been taken
        N_remaining_passengers = np.sum(self.passengers)
        time_steps_taken = 0
        while (time_steps_taken < self.time_steps - 1) and N_remaining_passengers > 0:
            # Perform passenger update
            self._update()
            # Update loop metrics
            time_steps_taken += 1
            N_remaining_passengers = np.sum(self.passengers)
            # Store values
            self._store_hist_values(time_steps_taken)
        

    def store_values(self):
        # Simulate
        self._simulate()
        np.savez("./data/simple_model.npz", self.passengers_history)
        print("Saved simple model")
        
        
if __name__ == "__main__":
    rows = 30
    time_steps = 10
    Model = SimplestPassengerModel(rows, time_steps)
    Model.store_values()
