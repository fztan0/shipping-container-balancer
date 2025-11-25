import puzzle_state
from collections import deque

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
    #col can't go to the left of 0 and to the right of 11
    if row > -1 and row < 8 and col > -1 and col < 12:
        return True
    else:
        return False
    
def bfs(state: puzzle_state.PuzzleState, originPoint: list[tuple[int,int], puzzle_state.Cell], destinationPoint: list[tuple[int,int], puzzle_state.Cell]) -> int:
    #up,down,left right
    grid = state.grid
    #initilize 2d grid of [8][12] to keep track of the current distance and if a position has been visited or not
    visited = [[False] * 12 for _ in range(8)]
    adjacent_moves = [(0,1), (0,-1), (1,0), (-1,0)]
    currentContainer = originPoint[0]
    goalPoint = destinationPoint[0]
    queue = deque()
    #initilize 2d grid of [8][12] to keep track of the current distance and if a position has been visited or not
    visited = [[False] * 12 for _ in range(8)]
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
                if grid[rowNext][colNext].description == "UNUSED":
                    calculate_cost = currentCost + 1
                    queue.append([nextPosition, calculate_cost]) 
    return 0
        
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









# //output: longest distance from the exhibits to the best placement of the brochure place

# //bfs will return a pair(finalDestination, distance from the starting node)
# pair<int,int> bfs(vector<vector<int>> adjacentNodes, int startExibit){
#     queue<int> queue; //created a queue that will store the exibits 
#     int n = adjacentNodes.size();
#     while (!queue.empty()) {
#         queue.pop(); //ensures that if the queue was previously used it is empty
#     }
#     vector<bool> didVisit(n, false);
#     vector<int> distance(n, 0);
#     didVisit[startExibit] = true;
#     int farthestDistance = 0;
#     int farthestNode = startExibit;
#     //push the starting position into the queue and mark it visited
#     queue.push(startExibit);
#     while(!queue.empty()){ //continue until you exausted all options or you found the destination
#         int curr = queue.front();
#         queue.pop(); //pop the coordinate and determine either its the destination. if not then add in its valid neighbors
#         //calculate distances of going to the neighbors
#         for(const auto&node : adjacentNodes[curr]){
#             //checking if the new position has not been visited before
#             if(didVisit[node] == false){
#                 distance[node] = distance[curr] + 1;
#                 queue.push(node);
#                 didVisit[node] = true;
#                 if(distance[node] > distance[farthestNode]){
#                     farthestNode = node;
#                 }
#             }
#         }
#     }
#     return {distance[farthestNode], farthestNode}; //return farthest distance and farthestNode
# }