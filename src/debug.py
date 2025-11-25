import puzzle_state
import search_algorithm
import move_operators

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


