import puzzle_state

'''
Operations:
    - need to check if position above current contains a container (if so can't move)
    - can move [0, +1] (right), [0, -1](left). 
    if there is a neighboring container when trying to move left or right need to adjust
    - must move [1, 0] or [-1,0] and check if it can move left or right
    - apply gravity. so if current block is at a position where there are no blocks right below but keep moving down until it is reached
'''

'''
Obstacles:
    - need to check if position above current contains a container (if so can't move)
    - can move [0, +1] (right), [0, -1](left)
'''



'''
return a list of moves to go to

apprach: go row by row starting at row 1 and check if valid position

A valid position can be: 
1) Any position that is unused
    - strictly row 0 or if col below has a container occupied

Dont need to consider a starting point will handle that when calculating the cost 

returns: A list of all valid moves (gives coordinates to the potential destination of the container)
'''
def getNextMoves(state: puzzle_state.PuzzleState) -> list[list[tuple[int,int], puzzle_state.Cell]]:
    nextMoves = []
    grid = state.grid
    for row in range(8):
        for col in range(12):
            cell_description = grid[row][col].description
            if cell_description == "UNUSED":
                if row == 0: #if unused any position at row 0 is valid
                    nextMoves.append([[row,col], grid[row][col]])
                elif grid[row-1][col].description != "UNUSED": 
                    nextMoves.append([[row,col], grid[row][col]])
    return nextMoves

'''
parameter: takes in a current puzzle state
returns: A list of all containers via their coordinate points (x,y) in the 2d grid
'''
def getAllContainers(state: puzzle_state.PuzzleState) -> list[list[tuple[int,int], puzzle_state.Cell]]:
    allContainers = []
    grid = state.grid
    for row in range(8):
        for col in range(12):
            cell_description = grid[row][col].description
            if cell_description != "UNUSED" and cell_description != "NAN":
                allContainers.append(((row,col), grid[row][col]))
    return allContainers

'''
parameter: takes in all containers in the current puzzle state
    purpose:
        - reject any containers that have something above it. (can't move it)

returns: A list of valid containers that can be moved to a set of next moves. (note: this function does not take into account gravity. just accept if it can move "freely")
'''
def validContainers(state: puzzle_state.PuzzleState, currentContainers: list[list[tuple[int,int], puzzle_state.Cell]]) -> list[list[tuple[int,int], puzzle_state.Cell]]:
    allValidContainers = []
    grid = state.grid
    for container in currentContainers:
        (row, col), _ = container
        containerAbove_description = grid[row + 1][col].description
        #as long as there is no container above the current container then it is valid and can "move" to other states
        if containerAbove_description == "UNUSED":
            allValidContainers.append(((row,col), grid[row][col]))
    return allValidContainers

'''
Need to know the valid moves
    1) anything row 1 that is unused 
    2) anything that is one above an already occupied state

parameter: 
    1)takes in a current puzzle state with respect to originPoint
    2) The original position of the container
    3)The new position that the container will be moved to
returns: The actual cost from the original container to the new position 
'''
def costFunction(state: puzzle_state.PuzzleState, originPoint: list[tuple[int,int], puzzle_state.Cell], destinationPoint: list[tuple[int,int], puzzle_state.Cell]) -> int:

    return
