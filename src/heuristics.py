import puzzle_state

def get_current_weight(state: puzzle_state.PuzzleState) -> tuple[int, int]:
    grid = state.grid

    total_p_weight = 0
    total_s_weight = 0

    # consider all the rows
    for _ in range(8):
        for col in range(12):
            cell_weight = grid[_][col].weight
            if col <= 5:
                total_p_weight += cell_weight
            else:
                total_s_weight += cell_weight
    return total_p_weight, total_s_weight


# standard manhattan distance is not feasible since we have a crane that can only move in certain ways
# it is used when a known container needs to be moved to a known position
# ideally we would calculate the actual cost to move each container to its target position
# but we do not have that kind of information in the heuristic function
# but we can use a simpler heuristic for A* that just considers the weight difference

# literally just the absolute weight difference between two sides of ship
# it does not estimate number of moves, distances, or anything spatial related within the puzzle's state
# h = |W_port - W_starboard|
# this heuristic only cares about how unbalanced the ship is at the moment and
# every unit of "imbalance" acts as if it takes 1 distance unit to fix
# containers are free to move anywhere, ignoring the cost of movement and only caring about reducing imbalance.
def heuristic(state: puzzle_state.PuzzleState) -> int:
    port, starboard = get_current_weight(state)
    imbalance = abs(port - starboard)
    if imbalance == 0:
        return 0

    # Find maximum container weight in the current state
    max_weight = 0
    for row in range(8):
        for col in range(12):
            cell = state.grid[row][col]
            if cell.weight > max_weight:
                max_weight = cell.weight

    if max_weight == 0:
        return 0

    # calculate minimum moves required (ceil division)
    min_moves = (imbalance + max_weight - 1) // max_weight

    # minimum cost per move (Manhattan distance between adjacent cells)
    min_cost_per_move = 2  # 1 move horizontal + 1 move vertical

    # admissible heuristic: never overestimates actual cost
    return min_moves * min_cost_per_move