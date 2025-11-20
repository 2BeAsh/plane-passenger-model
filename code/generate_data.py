from simple_model import SimplestPassengerModel
from full_move_model import FullMovePassengerModel


# Parameters
rows = 25
seat_cols_each_side = 2
time_steps = 1000
max_move = 4
N_repeat = 40

fname_baseline = "baseline"
fname_fullmove = "fullmove"

if __name__ == "__main__":
    # Create instance and run the simulation
    SimplestModel = SimplestPassengerModel(rows, seat_cols_each_side, time_steps)
    FullMoveModel = FullMovePassengerModel(rows, seat_cols_each_side, time_steps, max_move)
    
    run_sim = False
    if run_sim:
        SimplestModel.store_values(filename=fname_baseline)
        FullMoveModel.store_values(filename=fname_fullmove)

    run_times = True
    if run_times:
        SimplestModel.store_time_taken(N_repeat, fname_baseline)
        FullMoveModel.store_time_taken(N_repeat, fname_fullmove)
    
    
    
