import puzzle_state
import move_operators
import search_nodes
import heapq
import hashing


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

'''
Perform uniform cost search to determine proper ordering of containers

Will have a priority queue containing (cost, puzzlestate, list of moves)

Parameter: 
    - startingState: gets the current puzzle state from the manifest
Return:
    coordinate = tuple[int , int]
    move = tuple[coordinate , coordinate]
    pathAndCost = tuple[int, finalPuzzleState, list[move]] 

'''
def uniformCostSearch(startingState: puzzle_state.PuzzleState) -> 'Path & Cost':
    #if starting state is the goal return an empty list. No moves required
    if valid_edgecase_initialContainers(startingState) == True:
        return ([], 0)
    hashMap = {}
    key = hashing.createKey(startingState)
    hashMap[key] = True
    #create crane position to calculate cost from crane to starting state
    cranePosition = [(0, 8), puzzle_state.Cell(exists=True, weight=0, description="UNUSED")]
    #start at cranePosition. leave destination as (0,0) for now
    move = [cranePosition[0], (0,0)]
    listofMoves = []
    listofMoves.append(move)
    priority_queue = []
    startAtCrane = True
    cranePosition = [(0, 8), puzzle_state.Cell(exists=True, weight=0, description="UNUSED")]
    #initalize a minheap and keep track of cost, puzzle state, list of moves
    heapq.heappush(priority_queue, (0, startingState, listofMoves))
    while priority_queue:
        currentCost, currentState, currentMoves =  heapq.heappop(priority_queue)
        ph,sh = getCurrentWeight(currentState)
        if isGoalState(currentState, ph, sh):
            numMoves = len(currentMoves)
            lastContainerCoord = currentMoves[numMoves - 1] #get the coordinate of the last container
            endX,endY = lastContainerCoord[1] #destination of the lastContainer
            finalContainerCell = currentState.grid[endX][endY]
            lastContainer = [(endX,endY), finalContainerCell] 
            cost = search_nodes.bfs(currentState, lastContainer, cranePosition) #get the cost from going from last container to cranePosition
            currentCost = currentCost + cost
            #add the move from last cotaniner back to crane position
            currentMoves.append([(endX,endY), (0,8)])
            return currentCost, currentState, currentMoves 
        #gets all the containers in the state
        containers = move_operators.getAllContainers(currentState)
        #filters and only get valid containers
        validContainers = move_operators.validContainers(currentState, containers)
        nextContainers = move_operators.getNextMoves(currentState)
        for container in validContainers:
            (startX, startY) , _ = container
            if startAtCrane: #need to intially add the cost going from the cranePosition to firstContainer as well as updating the current move
                currentMoves[0] = [(0,8), (startX,startY)]
                currentCost = currentCost + search_nodes.bfs(currentState, cranePosition, container)
            for nextC in nextContainers:
                (endX, endY), _ = nextC
                if(((startX + 1), startY) != (endX, endY)): #a final position can't move up 1. (gravity)
                        updateState = search_nodes.updatedState(currentState, container, nextC)
                        key = hashing.createKey(updateState)
                        if key not in hashMap: #only queue unique states
                            cost = search_nodes.bfs(currentState, container, nextC)
                            currentCost = currentCost + cost
                            currentMoves.append([(startX, startY), (endX, endY)])
                            heapq.heappush(priority_queue, (currentCost, updateState, listofMoves))
                            hashMap[key] = True #update hashMap
        #already accounted for the crane so set it to false
        startAtCrane = False
    return