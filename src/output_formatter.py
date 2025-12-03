import puzzle_state
import os
def outputPuzzle(finalPuzzleState: puzzle_state.PuzzleState, output_file_name: str):
    final_grid = finalPuzzleState.grid
    output_path = os.path.join(os.getcwd(), "output", output_file_name)
    os.makedirs(os.path.join(os.getcwd(), "output"), exist_ok = True)
    with open(output_path, 'w') as file:
        for row in range(8):
            for col in range(12):
                containerContents = final_grid[row][col]
                weight = containerContents.weight
                description = containerContents.description
                line = f"[{row+1:02d},{col+1:02d}], {{{weight:05d}}}, {description}"
                file.write(f"{line}\n") # each subsequent line is a node index
        # remove last newline character to match output format
        file.truncate(file.tell() - len(os.linesep))