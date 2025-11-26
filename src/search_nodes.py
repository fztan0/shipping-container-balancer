import puzzle_state
import copy
from collections import deque


def updatedState(state: puzzle_state.PuzzleState, originPoint: list[tuple[int,int], puzzle_state.Cell], destinationPoint: list[tuple[int,int], puzzle_state.Cell]) -> puzzle_state.PuzzleState:
    updateState = copy.deepcopy(state)
    grid = updateState.grid
    (startX, startY), startCell = originPoint
    (endX, endY), endCell = destinationPoint
    grid[startX][startY] = endCell
    grid[endX][endY] = startCell
    return updateState

def calculatePoint(start: tuple[int,int], final: tuple[int,int]) -> tuple[int,int]:
    x0 = start[0]
    y0 = start[1]
    x1 = final[0]
    y1 = final[1]
    calculateX = abs(x0 - x1)
    calculateY = abs(y0 - y1)
    return (calculateX, calculateY)

def isBoundsValid(point: tuple[int,int]) -> bool:
    row = point[0]
    col = point[1]
    #note this is zero indexing
    #row can't go below 0 
    #col can't go to the left of 0 and to the right of 11. row is 9 since need to account for the parked configuration
    if row > -1 and row < 9 and col > -1 and col < 12:
        return True
    else:
        return False

def bfs(state: puzzle_state.PuzzleState, originPoint: list[tuple[int,int], puzzle_state.Cell], destinationPoint: list[tuple[int,int], puzzle_state.Cell]) -> int:
    #need to make a deep copy so any changes to the grid doesn't affect the main puzzle state
    grid = copy.deepcopy(state.grid)
    new_row = [puzzle_state.Cell(exists=True, weight=0, description="UNUSED") for _ in range(12)]
    grid.append(new_row)
    #initilize 2d grid of [9][12] to keep track of the current distance and if a position has been visited or not
    visited = [[False] * 12 for _ in range(9)] #need to add an extra row for the "crane position". Row 9 will be only for the crane movements
    adjacent_moves = [(0,1), (0,-1), (1,0), (-1,0)]
    currentContainer = originPoint[0]
    goalPoint = destinationPoint[0]
    queue = deque()
    #queue contains coordinate and current cost
    queue.append([currentContainer,0])
    while len(queue) > 0:
        #removing an item from the front of the queue
        container = queue.popleft() #queue contains point + current cost
        currentPoint = container[0]
        currentCost = container[1]
        (rowCurrent, colCurrent) = currentPoint
        (rowGoal, colGoal) = goalPoint
        visited[rowCurrent][colCurrent] = True
        #check the goal state
        if rowCurrent == rowGoal and colCurrent == colGoal:
            return currentCost
        for move in adjacent_moves:
            nextPosition = calculatePoint(currentPoint, move)
            rowNext, colNext = nextPosition
            #need to check if the next position is valid and unvisted
            if isBoundsValid((rowNext, colNext)) and visited[rowNext][colNext] == False:
                if grid[rowNext][colNext].description == "UNUSED" or (rowNext, colNext) == goalPoint: #might need to adjust this later for a state that "is in the air" above the state
                    calculate_cost = currentCost + 1
                    queue.append([nextPosition, calculate_cost]) 
    return 0
        