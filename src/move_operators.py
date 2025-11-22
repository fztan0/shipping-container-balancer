import puzzle_state
'''
operators: return a list of moves to go to

1) anything row 1 that is unused 
2) anything that is one above an already occupied state

returns: A list of all valid moves 
'''
# def getValidMoves(state: puzzle_state.PuzzleState, startingContainer: tuple[int,int]) -> list[tuple[int,int]]:

#     return

# def validMove()


'''
parameter: takes in a current puzzle state
returns: A list of all containers via their coordinate points (x,y) in the 2d grid
'''
def getAllContainers(state: puzzle_state.PuzzleState) -> list[tuple[int,int]]:
    allContainers = []
    grid = state.grid
    for row in range(8):
        for col in range(12):
            cell_description = grid[row][col].description
            if cell_description != "UNUSED" and cell_description != "NAN":
                allContainers.append([row,col])
    return allContainers

# def valid_firstRows(state: puzzle_state.PuzzleState) -> list[puzzle_state.PuzzleState]:
#     grid = state.grid
#     new_state = state; 
#     for row in range(1):
#         for col in range(12):
#             cell_description = grid[row][col].description
#             if cell_description == "UNUSED":
#                 new_state = 
#     return


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
def costFunction(state: puzzle_state.PuzzleState, originPoint: tuple[int,int], destinationPoint: tuple[int,int]) -> int:
    return