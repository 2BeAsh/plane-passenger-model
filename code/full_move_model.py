import numpy as np
from simple_model import SimplestPassengerModel


class FullMovePassengerModel(SimplestPassengerModel):
    
    def __init__(self, rows, seat_cols_each_side, time_steps, max_move):
        super().__init__(rows, seat_cols_each_side, time_steps)
        self.max_move = max_move
        
        
    def _move_in_hallway(self, x, y):
        """Overwrite the baseline model to add that passengers move the full distance to the nearest passenger"""        
        if y == self.hallway_col:
            # Find the distance to the nearest passenger.
            hallway_passengers = self.passengers[:, self.hallway_col]  # Remove seated passengers
            position_of_hallway_passengers = np.where(hallway_passengers == 1)[0]  # Any site with a 1 has a passenger. Get idx (i.e. position) of these
            dist_all = position_of_hallway_passengers - x  # Distance to all other passengers in the hallway
            dist_closer_to_exit = dist_all[dist_all > 0]  # Distance to passengers closer to the exit than the chosen one
        
            # If the chosen site has no passengers closer to the exit, attempt to move outside the plane
            if len(dist_closer_to_exit) == 0:
                self.passengers[x, y] = 0
                dist_move_out_of_plane = self.rows - x  # Distane to move outside the plane. rows - x is the last spot inside the plane.
                if dist_move_out_of_plane > self.max_move:
                    self.passengers[x + self.max_move, y] = 1
                
            else:
                # Find the distance to the closest passenger
                dist_nearest = dist_closer_to_exit[0]
                dist_to_move = int(dist_nearest - 1)  # Stand right behind the passenger. 
                self.passengers[x, y] = 0
                self.passengers[x + dist_to_move, y] = 1
                # In case dist_to_move == 0, no change will be made as first the passenger is removed at (x, y) and then readded at (x+0, y).