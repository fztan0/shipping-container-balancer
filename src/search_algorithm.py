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

'''
Two borderline cases for goal state check (based on inital manifest):
    1. if there are only two containers specifically (one on port side and other on starboard side) return true
    2. if there is just only one container in either the port side or starboard side return true
    3. If there are no containers at all
    4. If there are containers but all have 0 weights except for 1 container
everything else return false 
'''
def valid_edgecase_initialContainers(state: puzzle_state.PuzzleState) -> bool:
    grid = state.grid
    total_p_containers = 0
    total_s_containers = 0
    #consider all the rows
    noContainersP = True
    noContainersS = True
    everyWeightZero = True
    validPuzzle = False

    for _ in range(8):
        for col in range(12):
            cell_description = grid[_][col].description
            cell_weight = grid[_][col].weight
            if(col <= 5):
                if(cell_description != "UNUSED" and cell_description != "NAN" and cell_weight != 0):
                    total_p_containers = total_p_containers + 1
                if(cell_weight != 0):
                    everyWeightZero = False
            else:
                if(cell_description != "UNUSED" and cell_description != "NAN" and cell_weight != 0):
                    total_s_containers = total_s_containers + 1
                if(cell_weight != 0):
                    everyWeightZero = False
    total_non_zero_Containers = total_p_containers + total_s_containers
    #does checks 1-3 for <=2 containers
    if total_non_zero_Containers <= 2 and total_p_containers <= 1 and total_s_containers <=1 and noContainersP and noContainersS:
        validPuzzle = True
    #does checks 4. if all weights are zero then ship is perfectly balanced return true
    if validPuzzle or everyWeightZero or total_non_zero_Containers <= 1:
        return True
    return False
