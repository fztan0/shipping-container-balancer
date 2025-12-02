def manhattan_distance_heuristic(state):
    total_distance = 0
    grid = state.grid

    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            cell = grid[row_index][column_index]
            if cell.weight > 0 and cell.description not in ("UNUSED", "NAN"):
                # calculate horizontal distance to opposite side only
                current_x = column_index
                target_x = 11 - current_x if current_x <= 5 else 5 - (current_x - 6)
                dx = abs(current_x - target_x)
                total_distance += dx

    return total_distance