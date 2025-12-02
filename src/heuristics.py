def getCurrentWeight(state):
    grid = state.grid
    total_p_weight = 0
    total_s_weight = 0
    for _ in range(8):
        for col in range(12):
            cell_weight = grid[_][col].weight
            if(col <= 5):
                total_p_weight += cell_weight
            else:
                total_s_weight += cell_weight
    return total_p_weight, total_s_weight

def manhattan_distance_heuristic(state):
    total_distance = 0
    grid = state.grid
    port_weight, starboard_weight = getCurrentWeight(state)
    imbalance = port_weight - starboard_weight

    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            cell = grid[row_index][column_index]
            if cell.weight > 0 and cell.description not in ("UNUSED", "NAN"):
                current_x = column_index
                # Only move containers that help reduce imbalance
                if imbalance > 0 and current_x <= 5:  # Port side container
                    target_x = 6 + (current_x % 3)  # Move to starboard
                    dx = abs(current_x - target_x)
                    total_distance += dx
                elif imbalance < 0 and current_x >= 6:  # Starboard container
                    target_x = (current_x - 6) % 3  # Move to port
                    dx = abs(current_x - target_x)
                    total_distance += dx
    return total_distance