import puzzle_state

'''
Parameters:
state : the puzzle state 
p0 : original weight of the port side
s0: original weight of the starboard side

return:
either true or false if that current state is a goal

function does multiple checks
    1. |Ph - Sh| < (Sum (P0, S0) x 0.10)
    2. if both |Ph - Sh| is 0 then it is the goal
'''
def isGoalState(state: puzzle_state.PuzzleState, p0: int, s0:int) -> bool:
    ph, sh = getCurrentWeight(state)
    current_difference = abs(ph - sh)
    if current_difference == 0 or (current_difference <= (p0 + s0) * 0.10):
        return True
    else:
        return False

#Returns [Pr, Sr]. Pr represents sum of the all the weights on the port side
#Sr represents sum of all the weights in the starboard side 
def getCurrentWeight(state: puzzle_state.PuzzleState) -> tuple[int,int]:
    grid = state.grid
    total_p_weight = 0
    total_s_weight = 0
    #consider all the rows
    for _ in range(8):
        for col in range(12):
            cell_weight = grid[_][col].weight
            if(col <= 5):
                total_p_weight = total_p_weight + cell_weight
            else:
                total_s_weight = total_s_weight + cell_weight
    return total_p_weight, total_s_weight
