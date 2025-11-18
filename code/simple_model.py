import numpy as np

class SimplestPassengerModel():
    
    def __init__(self, rows, prob_move, time_steps):
        self.rows = rows
        self.prob_move = prob_move
        self.time_steps = time_steps
        
        
    def _initialize_passengers(self):
        # Everyone starts in the left column (i.e. seated), with velocity 0.
        self.x = np.arange(self.rows)
        self.y = np.zeros(size=self.rows)
        self.vx = np.zeros_like(self.y)
        self.vy = np.zeros_like(self.y)
        self.N_remaining_passengers = self.x.size

        
    def _accelerate(self):
        self.v = np.min(self.v + 1, 1)

    def _blocking_passagers(self):
        self.v = np.min(self.v, )
    
    def _random_stop(self):
        pass
    
    def _leave_seat(self):
        pass
    
    def _perform_move(self):
        pass
    
    
    def _update(self):
        # # Standing passagers
        # self._accelerate()
        # self._blocking_passagers()
        # self._random_stop()
        # # Seated passengers
        # self._leave_seat()
        # # All
        # self._perform_move()
        
        for i in range(self.N_remaining_passengers):
            xi = self.x[i]
            yi = self.y[i]
            vxi = self.vx[i]
            vyi = self.vy[i]
            
            # Standing
            if yi == 1:
                # Accelerate
                vxi = np.min(vxi + 1, 1)
                # Passenger blocking
                vxi = np.min(vxi, self.x[i+1] - xi - 1)
                # Random stop
                if np.random.uniform() > 1 - self.prob_move: 
                    vxi = np.max(vxi - 1, 0)
                # Store the updated velocity
                self.vx[i] = vxi            
                
            # Seated
            else:  # yi == 0
                vyi = 0
                if np.count_nonzero(self.x == xi) == 2:  # If two passengers share x value they are next to each other
                    vyi = 1
                # Store the updated velocity
                self.vy[i] = vyi
            
        # Perform move update
        self.x += self.vx
        self.y += self.vy
        
        self.vy[:] = 0  # Reset y speed (vx stays the same)
        
        
    def _simulate(self):
        pass
    
    
    
    
    def _update_TASEP():
        
        
        return 