import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Optional
from puzzle_state import PuzzleState, Cell
import copy
import logger
from matplotlib.widgets import TextBox, Button
import manifest_io
import search_algorithm
from output_formatter import outputPuzzle
import os

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
        
def visualize_state(state: PuzzleState, message: Optional[str] = None, source_location: Optional[List[tuple[int, int]]] = None, 
                    target_location: Optional[List[tuple[int, int]]] = None, fig = None, ax = None, 
                    logger_message: Optional[str] = None, manifest_name: Optional[str] = None, 
                    colored_message_parts: Optional[dict] = None):
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
            elif cell.description == "UNUSED":
                # unused
                ax.text(col + 0.5, y_pos, 'UNUSED', ha='center', va='center', fontsize = 9, fontweight = 'bold', color = '#666666')
            else:
                # containers
                desc = cell.description[:8] + "..." if len(cell.description) > 8 else cell.description
                ax.text(col + 0.5, y_pos, desc, ha = 'center', va ='center', fontsize = 10, fontweight = 'bold', color = 'white')

    ax.set_xticks([i + 0.5 for i in range(cols)])
    ax.set_xticklabels(range(1, cols + 1))
    ax.set_xlabel('Column', fontsize = 12, fontweight = 'bold')

    ax.set_yticks([i + 0.5 for i in range(rows)])
    ax.set_yticklabels(range(1, rows + 1))
    ax.set_ylabel('Row', fontsize = 12, fontweight = 'bold')

    title = manifest_name
    if message:
        title += f'\n{message}'
    ax.set_title(title, fontsize = 18, fontweight = 'bold', pad = 30)

    if colored_message_parts:
        render_colored_message(ax, colored_message_parts)
    elif logger_message:
        ax.text(0.5, 1.02, logger_message, transform = ax.transAxes, ha = 'center', va = 'bottom', fontsize = 14, fontweight = 'normal')

    plt.tight_layout()
    plt.grid(False)
    plt.draw()
    plt.pause(0.001)
    return fig, ax

def render_colored_message(ax, parts):
    fontsize = 12
    y_pos = 1.02
    full_text = parts.get('counter', '') + parts. get('source', '') + parts.get('action', '') + parts.get('target', '') + parts.get('duration', '')
    fig = ax.get_figure()
    renderer = fig.canvas.get_renderer()

    text_to_measure = ax.text(0,0, full_text, fontsize = fontsize, transform = ax.transAxes)
    bounds = text_to_measure.get_window_extent(renderer = renderer)
    text_to_measure.remove()

    bounds_axes = bounds.transformed(ax.transAxes.inverted())
    total_width = bounds_axes.width
    x_start = 0.5 - total_width / 2
    x_pos = x_start
    
    text_parts = [
        (parts.get('counter', ''), 'black'),
        (parts.get('source', ''), '#17DD1E'),
        (parts.get('action', ''), 'black'),
        (parts.get('target', ''), '#CB1609'),
        (parts.get('duration', ''), 'black'),
    ]

    for text, color in text_parts:
        if text:
            t = ax.text(x_pos, y_pos, text, transform = ax.transAxes, ha = 'left', va = 'bottom', fontsize = fontsize, fontweight = 'normal', color = color)
            bounds = t.get_window_extent(renderer=renderer)
            bounds_axes = bounds.transformed(ax.transAxes.inverted())
            x_pos += bounds_axes.width

def visualize_steps(initial_state: PuzzleState, all_moves: List[List[tuple[int, int]]], all_cost: List[float], on_complete_callback = None, num_moves: int = 0, duration: float = 0.0):
    curr_state = copy.deepcopy(initial_state)
    manifest_name = manifest_io.MANIFEST_FILENAME
    is_balanced = num_moves == 0
    state_tracker = {
        'move_index': -1,
        'all_moves': all_moves,
        'curr_state': curr_state,
        'fig': None,
        'ax': None,
        'text_box': None,
        'text_box_ax': None,
        'input_mode': False,
        'initial_state': initial_state,
        'on_complete': on_complete_callback,
        'current_logger_message': None,
        'solution_message': "" if is_balanced else f"Balance solution found, it will require {num_moves} moves/{duration} minute(s).",
        'manifest_name': manifest_name,
        'total_moves': len(all_moves),
        'is_balanced': is_balanced,
        'all_cost': all_cost,
        'outbound_written': False,
    }
    def write_outbound_file():
        if not state_tracker['outbound_written']:
            base_name = os.path.splitext(manifest_io.MANIFEST_FILENAME)[0]
            outbound_filename = base_name + "OUTBOUND.txt"
            outputPuzzle(state_tracker['curr_state'], outbound_filename)
            state_tracker['outbound_written'] = True

    def on_text_submit(text):
        if text.strip():
            logger.log_message(text.strip())
        hide_text_input()

    def show_text_input():
        state_tracker['text_box_ax'] = state_tracker['fig'].add_axes([0.3, 0.02, 0.4, 0.04])
        state_tracker['text_box'] = TextBox(state_tracker['text_box_ax'], 'Log Entry:', initial ='')
        state_tracker['text_box'].on_submit(on_text_submit)
        state_tracker['input_mode'] = True
        state_tracker['fig'].canvas.draw()

    def hide_text_input():
        if state_tracker['text_box_ax'] is not None:
            state_tracker['text_box_ax'].remove()
            state_tracker['text_box_ax'] = None
            state_tracker['text_box'] = None
            state_tracker['input_mode'] = False
            state_tracker['fig'].canvas.draw()

    def on_key_press(event):
        if state_tracker['input_mode']:
            if event.key == 'escape':
                hide_text_input()
            return
        
        if event.key == 'r':
            hide_text_input()
            logger.log_finish_operation()
            logger.write_logger_to_desktop()
            state_tracker['fig'].canvas.mpl_disconnect(state_tracker.get('key_handler_id'))
            if state_tracker['on_complete']:
                state_tracker['on_complete']()
            return
        
        if event.key == 'p':
            show_text_input()
            return
        if state_tracker['is_balanced']:
            if event.key == 'enter' or event.key ==' ':
                write_outbound_file()
                visualize_state(state_tracker['curr_state'], "Updated Manifest - 'q' to quit, 'p' to log, 'r' to load new manifest", fig=state_tracker['fig'], ax=state_tracker['ax'], manifest_name=state_tracker['manifest_name'])
                ax.text(0.5, 1.02, "Reminder: Email file in output folder to captain", transform = ax.transAxes, ha = 'center', va = 'bottom', fontsize = 14, fontweight = 'normal')
                return

        if event.key == 'enter' or event.key == ' ':
            state_tracker['move_index'] += 1

            # Last state
            if state_tracker['move_index'] >= len(state_tracker['all_moves']):
                write_outbound_file()
                visualize_state(state_tracker['curr_state'], "Updated Manifest - 'q' to quit, 'p' to log, 'r' to load new manifest", fig=state_tracker['fig'], ax=state_tracker['ax'], manifest_name=state_tracker['manifest_name'])
                ax.text(0.5, 1.02, "Reminder: Email file in output folder to captain", transform = ax.transAxes, ha = 'center', va = 'bottom', fontsize = 14, fontweight = 'normal')

                return
            
            start_pos, end_pos = state_tracker['all_moves'][state_tracker['move_index']]
            move_cost = state_tracker['all_cost'][state_tracker['move_index']]
            start_x, start_y = start_pos
            end_x, end_y = end_pos
            prev_pos = (start_x + 1, start_y + 1)
            updated_pos = (end_x + 1, end_y + 1)
            strPrev_pos = f"[0{prev_pos[0]},0{prev_pos[1]}]"
            strUpdated_pos = f"[0{updated_pos[0]},0{updated_pos[1]}]"

            current_move_num = state_tracker['move_index'] + 1
            total_moves = state_tracker['total_moves']
            duration_text = f" (Duration: {move_cost} min)"
            move_counter = f"{current_move_num} of {total_moves}: " 

            # INITIAL MOVE
            if start_x == 8 and start_y == 0:
                source_locations = []
                target_locations = [end_pos]
                #move_message = f"{current_move_num} of {total_moves}: PARK was moved to {strUpdated_pos}"
                logger.log_message(f"{move_counter}PARK was moved to {strUpdated_pos}{duration_text}")
                colored_parts = {
                    'counter': move_counter,
                    'source': "PARK",
                    'action': " was moved to ",
                    'target': strUpdated_pos,
                    'duration': duration_text
                }
            # FINAL MOVE
            elif end_x == 8 and end_y == 0:
                source_locations = [start_pos]
                target_locations = []
                #move_message = f"{current_move_num} of {total_moves}: {strPrev_pos} was moved to PARK"
                logger.log_message(f"{move_counter}{strPrev_pos} was moved to PARK{duration_text}")
                colored_parts = {
                    'counter': move_counter,
                    'source': strPrev_pos,
                    'action': " was moved to ",
                    'target': "PARK",
                    'duration': duration_text
                }
            # NORMAL MOVE
            else:
                #move_message = f"{current_move_num} of {total_moves}: {strPrev_pos} was moved to {strUpdated_pos}"
                logger.log_message(f"{move_counter}{strPrev_pos} was moved to {strUpdated_pos}{duration_text}")
                colored_parts = {
                    'counter': move_counter,
                    'source': strPrev_pos,
                    'action': " was moved to ",
                    'target': strUpdated_pos,
                    'duration': duration_text
                }
                container = state_tracker['curr_state'].grid[start_x][start_y]
                source_locations = [start_pos]
                target_locations = [end_pos]

                state_tracker['curr_state'].grid[end_x][end_y] = Cell(exists=True, weight=container.weight, description=container.description)
               
                # Clear prev position
                state_tracker['curr_state'].grid[start_x][start_y] = Cell(exists=True, weight=0, description="UNUSED")
            visualize_state(state_tracker['curr_state'], "Press ENTER to continue, 'p' to log, 'q' to quit", source_locations, target_locations, fig = state_tracker['fig'], ax=state_tracker['ax'], colored_message_parts=colored_parts, manifest_name=state_tracker['manifest_name'])
                

    fig = plt.gcf()
    ax = plt.gca()
    state_tracker['fig'] = fig
    state_tracker['ax'] = ax
    
    state_tracker['key_handler_id'] = fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    initial_message = "Manifest Already Balanced - ENTER to continue, 'p' to log, 'q' to quit" if is_balanced else "Initial Manifest - ENTER to continue, 'p' to log, 'q' to quit"
    visualize_state(curr_state, initial_message, fig = fig, ax = ax, logger_message=state_tracker['solution_message'], manifest_name=state_tracker['manifest_name'])
    fig.canvas.draw()
    
def run_interface():
    state_tracker = {
        'curr_state': None,
        'fig': None,
        'ax': None,
        'text_box': None,
        'text_box_ax': None,
        'input_mode': True,
        'load_button': None,
        'load_button_ax': None,
    }
    
    def on_manifest_submit(filename):
        if not filename.strip():
            print("No filename provided")
            return
        try:
            file_path = "data/" + filename.strip()
            manifest_io.MANIFEST_FILENAME = filename.strip()

            # Reset logger for new manifest
            logger.events = []
            logger.start_time = None
            logger.initialize_logger()
            
            puzzle = manifest_io.load_ship_manifest(file_path)

            # Run algorithm here
            finalCost, finalPuzzleState, allMoves, allCost = search_algorithm.uniformCostSearch(puzzle)
            duration = finalCost
            logger.log_balance_sol(len(allMoves), duration)

            hide_input_ui()
            visualize_steps(puzzle, allMoves, allCost,on_complete_callback=show_input_ui, num_moves=len(allMoves), duration=duration)

        except FileNotFoundError:
            show_input_ui(error_message="File not found or cannot be read")
        except Exception as e:
            show_input_ui(error_message="File not found or cannot be read")

    def show_input_ui(error_message=None):
        state_tracker['input_mode'] = True
        if state_tracker['fig'] is None:
            plt.ion()
            state_tracker['fig'], state_tracker['ax'] = plt.subplots(figsize = (16,10))
            state_tracker['fig'].canvas.mpl_connect('close_event', on_close)
        
        # Clean slate
        state_tracker['fig'].clear()
        state_tracker['ax'] = state_tracker['fig'].add_subplot(111)
        state_tracker['ax'].set_xlim(0,12)
        state_tracker['ax'].set_ylim(0,8)
        state_tracker['ax'].axis('off')

        # Menu title
        state_tracker['ax'].text(6,6, 'Load Balancing System', ha='center', va='center', fontsize=35, fontweight = 'bold')
        if error_message:
            state_tracker['ax'].text(6, 5, error_message, ha = 'center', va = 'center', fontsize = 20, color = 'red')
        else:
            state_tracker['ax'].text(6,5, 'Please enter manifest to load', ha='center', va='center', fontsize=20)

        # Menu input
        state_tracker['text_box_ax'] = state_tracker['fig'].add_axes([0.3, 0.45, 0.45, 0.05])
        state_tracker['text_box'] = TextBox(state_tracker['text_box_ax'], 'Manifest:', initial='')
        state_tracker['text_box'].on_submit(on_manifest_submit)

        # Menu buttons
        state_tracker['load_button_ax'] = state_tracker['fig'].add_axes([0.45, 0.35, 0.1, 0.05])
        state_tracker['load_button'] = Button(state_tracker['load_button_ax'], 'Load')
        state_tracker['load_button'].on_clicked(lambda event: on_manifest_submit(state_tracker['text_box'].text))
        
        state_tracker['fig'].canvas.draw()
    
    def hide_input_ui():
        if state_tracker['text_box_ax'] is not None:
            state_tracker['text_box_ax'].remove()
            state_tracker['text_box_ax'] = None
            state_tracker['text_box'] = None
        
        if state_tracker['load_button_ax'] is not None:
            state_tracker['load_button_ax'].remove()
            state_tracker['load_button_ax'] = None
            state_tracker['load_button'] = None
        state_tracker['input_mode'] = False
    
    def on_close(event):
        # Check actual loading of manifest
        if logger.events and len(logger.events) >1:
            logger.log_finish_operation()
            logger.log_kill()
            logger.write_logger_to_desktop()
        plt.close('all')
    
    show_input_ui()
    plt.show(block = True)
    plt.ioff()
            
