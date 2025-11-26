import puzzle_state
import copy


#converts the gird (which contains list) into all tuples to create hashable type
def createKey(state: puzzle_state) -> tuple[tuple[bool, int, str]]:
    currentState = copy.deepcopy(state)
    grid = currentState.grid
    return tuple(
                tuple((cell.exists, cell.weight, cell.description) for cell in row) 
            for row in grid)

