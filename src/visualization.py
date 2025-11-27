import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Optional
from puzzle_state import PuzzleState, Cell
import copy
import logger

def get_cell_color(cell: Cell, is_source: bool = False, is_target: bool = False) -> str:
    if is_source:
        return "#17DD1E"
    elif is_target:
        return "#CB1609"
    
    if not cell.exists:
        return "#3a3939"
    elif cell.description == "UNUSED":
        return "#e9e6e6"
    else:
        return "#d2b48c"
        
def visualize_state(state: PuzzleState, message: Optional[str] = None, source_location: Optional[List[tuple[int, int]]] = None, target_location: Optional[List[tuple[int, int]]] = None, fig = None, ax = None):
    if fig is None or ax is None:
        plt.ion()
        fig, ax = plt.subplots(figsize = (16,10))
    else:
        ax.clear()
    rows = len(state.grid)
    cols = len(state.grid[0])

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')

    source_set = set(source_location) if source_location else set()
    target_set = set(target_location) if target_location else set()

    for row in range(rows):
        for col in range(cols):
            cell = state.grid[row][col]
            color = get_cell_color(cell)

            is_source = (row, col) in source_set
            is_target = (row, col) in target_set
            color = get_cell_color(cell, is_source, is_target)

            rect = patches.Rectangle((col,row), 1, 1, linewidth = 1.5, edgecolor = 'black', facecolor = color)
            ax.add_patch(rect)
            y_pos = row + 0.5

            if not cell.exists:
                # nan
                ax.text(col + 0.5, y_pos, 'NAN', ha='center', va='center', fontsize = 9, fontweight = 'bold', color = 'white')
                ax.text(col + 0.5, y_pos - 0.2, f'{cell.weight}', ha='center', va = 'center', fontsize = 8, color = 'white')
            elif cell.description == "UNUSED":
                # unused
                ax.text(col + 0.5, y_pos, 'UNUSED', ha='center', va='center', fontsize = 9, fontweight = 'bold', color = '#666666')
                ax.text(col + 0.5, y_pos - 0.2, f'{cell.weight}', ha='center', va = 'center', fontsize = 8, color = 'black')
                # Note: will expand for source and target cells
            else:
                # containers
                desc = cell.description[:8] + "..." if len(cell.description) > 8 else cell.description
                ax.text(col + 0.5, y_pos + 0.2, desc, ha = 'center', va ='center', fontsize = 10, fontweight = 'bold', color = 'white')
                ax.text(col + 0.5, y_pos - 0.2, f'{cell.weight}', ha='center', va = 'center', fontsize = 8, color = 'white')

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
    plt.draw()
    plt.pause(0.001)
    return fig, ax

def visualize_steps(initial_state: PuzzleState, all_moves: List[List[tuple[int, int]]]):
    curr_state = copy.deepcopy(initial_state)
    state_tracker = {
        'move_index': -1,
        'all_moves': all_moves,
        'curr_state': curr_state,
        'fig': None,
        'ax': None,
        'finished': False
    }

    def on_key_press(event):
        if event.key == 'q':
            plt.close('all')
            state_tracker['finished'] = True
            return
        if event.key == 'enter' or event.key == ' ':
            state_tracker['move_index'] += 1

            # Last state
            if state_tracker['move_index'] >= len(state_tracker['all_moves']):
                visualize_state(state_tracker['curr_state'], "Final State (press q to quit)", fig=state_tracker['fig'], ax=state_tracker['ax'])
                return
            
            start_pos, end_pos = state_tracker['all_moves'][state_tracker['move_index']]
            start_x, start_y = start_pos
            end_x, end_y = end_pos
            prev_pos = (start_x + 1, start_y + 1)
            updated_pos = (end_x + 1, end_y + 1)

            # INITIAL MOVE
            if start_x == 8 and start_y == 0:
                source_locations = []
                target_locations = [end_pos]
                logger.log_message(f"[{prev_pos} was moved to [{updated_pos}]]")
            # FINAL MOVE
            elif end_x == 8 and end_y == 0:
                source_locations = [start_pos]
                target_locations = []
                logger.log_message(f"[{prev_pos} was moved to [{updated_pos}]]")
            # NORMAL MOVE
            else:
                logger.log_message(f"[{prev_pos} was moved to [{updated_pos}]]")
                container = state_tracker['curr_state'].grid[start_x][start_y]
                source_locations = [start_pos]
                target_locations = [end_pos]

                state_tracker['curr_state'].grid[end_x][end_y] = Cell(exists=True, weight=container.weight, description=container.description)
               
                # Clear prev position
                state_tracker['curr_state'].grid[start_x][start_y] = Cell(exists=True, weight=0, description="UNUSED")
            visualize_state(state_tracker['curr_state'], "", source_locations, target_locations, fig = state_tracker['fig'], ax=state_tracker['ax'])
                

    plt.ion()
    fig, ax = plt.subplots(figsize = (16,10))
    state_tracker['fig'] = fig
    state_tracker['ax'] = ax
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    visualize_state(curr_state, "Initial State - ENTER to continue", fig = fig, ax = ax)
    plt.show(block=True)
    plt.ioff()
