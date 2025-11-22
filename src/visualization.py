import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Optional
from puzzle_state import PuzzleState, Cell

def get_cell_color(cell: Cell, is_source: bool = False, is_target: bool = False) -> str:
    if is_source:
        return "#17DD1E"
    elif is_target:
        return "#CB1609"
    
    if not cell.exists:
        return "#3a3939"
    elif cell.weight == 0:
        return "#e9e6e6"
    else:
        return "#d2b48c"
        
def visualize_state(state: PuzzleState, message: Optional[str] = None, source_location: Optional[List[tuple[int, int]]] = None, target_location: Optional[List[tuple[int, int]]] = None):
    fig, ax = plt.subplots(figsize = (16,10))
    rows = len(state.grid)
    cols = len(state.grid[0])

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')

    for row in range(rows):
        for col in range(cols):
            cell = state.grid[row][col]
            color = get_cell_color(cell)

            rect = patches.Rectangle((col,row), 1, 1, linewidth = 1.5, edgecolor = 'black', facecolor = color)
            ax.add_patch(rect)
            y_pos = row + 0.5

            if not cell.exists:
                # nan
                ax.text(col + 0.5, y_pos, 'NAN', ha='center', va='center', fontsize = 8, fontweight = 'bold', color = 'white')
            elif cell.weight == 0:
                # unused
                ax.text(col + 0.5, y_pos, 'UNUSED', ha='center', va='center', fontsize = 7, fontweight = 'bold', color = '#666666')
                # Note: will expand for source and target cells
            else:
                # containers
                ax.text(col + 0.5, y_pos + 0.2, f'{cell.weight}', ha='center', va = 'center', fontsize = 8, fontweight = 'bold', color = 'white')
                desc = cell.description[:8] + '...' if len(cell.description) > 8 else cell.description
                ax.text(col + 0.5, y_pos - 0.2, desc, ha = 'center', va ='center', fontsize = 6, color = 'white', style = 'italic')

    ax.set_xticks([i + 0.5 for i in range(cols)])
    ax.set_xticklabels(range(1, cols + 1))
    ax.set_xlabel('Column', fontsize = 12, fontweight = 'bold')

    ax.set_yticks([i + 0.5 for i in range(rows)])
    ax.set_yticklabels(range(1, rows + 1))
    ax.set_ylabel('Row', fontsize = 12, fontweight = 'bold')

    title = 'Shipping Container Grid'
    if message:
        title += f'\n{message}'
    ax.set_title(title, fontsize = 14, fontweight = 'bold', pad = 20)

    plt.tight_layout()
    plt.grid(False)
    plt.show()

# TODO: function showing each state/move via every enter pressed