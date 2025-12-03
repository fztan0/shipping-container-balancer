import puzzle_state
import search_algorithm
import move_operators
import search_nodes
import hashing
import visualization
import time
import logger
import manifest_io
import math
import output_formatter
import os

def debug_print_formatted_loaded_manifest(state: puzzle_state):
      for r in range(1, 9): # rows 1–8
            for c in range(1, 13): # cols 1–12
                  cell = state.grid[r - 1][c - 1]

                  if not cell.exists:
                        weight = 0
                        token = "NAN"
                  elif cell.description == "UNUSED":
                        weight = 0
                        token = "UNUSED"
                  else:
                        weight = cell.weight
                        token = cell.description

                  # format weight as 5 digits with 0-padding
                  weight_field = f"{weight:05d}"

                  print(f"[{r:02d},{c:02d}], {{{weight_field}}}, {token}")

      return


def debug_print_raw_loaded_manifest(state: puzzle_state):
      print("Grid:")
      for row in state.grid:
            print([f"CELL(exists={cell.exists}, weight={cell.weight}, desc='{cell.description}')" for cell in row])

      return

def debug_print_weight_grid(state: puzzle_state):
      print("Weight Grid:")
      #reflect example from cs179 lecture slides
      for row in reversed(state.grid):
            print([cell.weight if cell.exists else 'NAN' for cell in row])
      return

def debug_print_totalWeight_eachSide(state: puzzle_state):
      #reflect example from cs179 lecture slides
      ph,sh = search_algorithm.getCurrentWeight(state)
      print(f"Weight of PH: {ph}")
      print(f"Weight of SH: {sh}")
      p0,s0 = search_algorithm.getCurrentWeight(state)
      isGoal = search_algorithm.isGoalState(state, p0, s0)
      print(f"Is goal? : {isGoal}")
      return

def debug_goalstate_initialmanifest(state: puzzle_state):
      #reflect example from cs179 lecture slides
      isGoal = search_algorithm.valid_edgecase_initialContainers(state)
      print(f"Is goal? : {isGoal}")
      return

def debug_getNextPosition(state: puzzle_state):
      #reflect example from cs179 lecture slides
      containers = move_operators.getNextMoves(state)
      if len(containers) == 0:
            print("No containers")
      else:
            for (x,y), _ in containers:
                  print((x+1,y+1))
      return

def debug_getContainers(state: puzzle_state):
      #reflect example from cs179 lecture slides
      containers = move_operators.getAllContainers(state)
      if len(containers) == 0:
            print("No containers")
      else:
            for (x,y), _ in containers:
                  print((x,y))
      return

def debug_validContainers(state: puzzle_state):
      containers = move_operators.getAllContainers(state)
      if len(containers) == 0:
            print("No containers")
            return
      else:
            print(f"Original Containers: {len(containers)}")
            for (x,y), _ in containers:
                  
                  print(f"({x+1},{y+1})")

      validContainers = move_operators.validContainers(state, containers)
      print(f"Valid Containers: {len(validContainers)}")
      for (x,y), _ in validContainers:
                  print(f"({x+1},{y+1})")
      return


def debug_bfs(state: puzzle_state):
      containers = move_operators.getAllContainers(state)
      if len(containers) == 0:
            print("No containers")
            return
      validContainers = move_operators.validContainers(state, containers)
      nextContainers = move_operators.getNextMoves(state)
      for container in validContainers:
            containerStart = container
            (startX, startY) , _ = containerStart
            print(f"Starting Position: ({startX+1},{startY+1})")
            for nextC in nextContainers:
                  containerEnd = nextC
                  (endX, endY), _ = containerEnd
                  if(((startX + 1), startY) != (endX, endY)): #a final position can't move up 1. (gravity)
                        print(f"Final Position: ({endX+1},{endY+1})")
                        cost = search_nodes.bfs(state, containerStart, containerEnd)
                        print(f"Cost: {cost}")

def debug_testCraneCost(state: puzzle_state):
      cranePosition = [(8,0), puzzle_state.Cell(exists=True, weight=0, description="UNUSED")]
      (craneX, craneY) , _ = cranePosition
      startingPosition = [(0,5), puzzle_state.Cell(exists=True, weight=99, description="B")]
      (startX, startY) , _ = startingPosition
      cost = search_nodes.bfs(state, startingPosition, cranePosition)
      print(f"Starting Position: ({craneX+1},{craneY+1})")
      print(f"Final Position: ({startX+1},{startY+1})")
      print(f"Cost: {cost}")

def debug_updateState(state: puzzle_state):
      emptyPosition = [(1, 7), puzzle_state.Cell(exists=True, weight=0, description="UNUSED")]
      container = [(0,1), puzzle_state.Cell(exists=True, weight=101, description="Z")]
      newState = search_nodes.updatedState(state, emptyPosition, container)
      for row in reversed(newState.grid):
            print([cell.weight if cell.exists else 'NAN' for cell in row])
      return

def debug_hashMap(state: puzzle_state):
      test_hashMap = {}
      key = hashing.createKey(state)
      test_hashMap[key] = True
      if key not in test_hashMap:
            print("Unique")
      else:
            print("duplicate")
      return
      
def debug_ucsAlg(state: puzzle_state):
      start = time.time()
      finalCost, finalPuzzleState, allMoves, allCost = search_algorithm.uniformCostSearch(state)
      duration = time.time() - start
      ceiling_duration = math.ceil(duration)
      print(f"Final Cost: {finalCost}")
      print(f"All Cost: {allCost}")
      print(f"{(allMoves)}")
      logger.log_balance_sol(len(allMoves), ceiling_duration)
      visualization.visualize_steps(state, allMoves)
      return

def debug_logger_example():
      logger.initialize_logger()
      file_path = manifest_io.get_file_name()
      puzzle_state = manifest_io.load_ship_manifest(file_path)

      debug_ucsAlg(puzzle_state)
      
      # logger.log_move_operation(allMoves)
      logger.log_finish_operation()
      logger.log_kill()
      logger.write_logger_to_desktop()

def debug_output(state: puzzle_state):
      new_output = os.path.splitext(manifest_io.MANIFEST_FILENAME)[0]
      filename = new_output + "OUTBOUND" + ".txt"
      finalCost, finalPuzzleState, allMoves, allCost = search_algorithm.uniformCostSearch(state)
      output_formatter.outputPuzzle(finalPuzzleState, filename)
      return