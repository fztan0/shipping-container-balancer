from puzzle_state import PuzzleState

# "each move takes one minute"
# although this heuristic is in number of moves and in language it would pollute the cost function, but the number of moves essentially translates to one unit of time in minutes anyways, therefore it is still admissible.
def heuristic(state: PuzzleState) -> int:
      port_weights = []
      starboard_weights = []

      # scan and separate weights by side
      for row_index in state.grid:
            for column_index, cell in enumerate(row_index):
                  if cell.weight > 0:
                        if column_index <= 5: # columns 0–5 is port
                              port_weights.append((cell.weight, column_index))
                        else: # columns 6–11 is starboard
                              starboard_weights.append((cell.weight, column_index))

      # compute the weights for both sides
      left_mass = sum(w for w, _ in port_weights)
      right_mass = sum(w for w, _ in starboard_weights)


      # if nearly balanced then just set heuristic = 0
      if abs(left_mass - right_mass) <= 2:
            return 0

      # slide 40
      # calculate BalanceMass slide 40 (L_m + R_m) / 2
      total_mass = left_mass + right_mass
      balance_mass = total_mass / 2

      # slide 40
      # identify which side is the deficit and choose heavier side to slim down
      if left_mass < right_mass:
            deficit = balance_mass - left_mass
            heavy_side_containers = starboard_weights
            move_from = "starboard"
      else:
            deficit = balance_mass - right_mass
            heavy_side_containers = port_weights
            move_from = "port"


      # sort by weight (largest first)
      heavy_side_containers = sorted(heavy_side_containers, key=lambda x: x[0], reverse=True)







      # each unit of cost is a time in minutes
      cost = 0
      remaining_deficit = deficit

      for weight, column_index in heavy_side_containers:
            if remaining_deficit <= 0:
                  break

            # minimize deficit
            remaining_deficit -= weight

            # crossing distance of going to ther side (over midline)
            if move_from == "port":
                  # nearest starboard column = col 6
                  crossing_distance = 6 - column_index
            else:
                  # nearest port column = col 5
                  crossing_distance = column_index - 5 # ACCOUNT FOR ZERO INDEXING!

            # minimal cost per move = 1 minute
            # EVERY move must take AT LEAST 1 minute
            move_cost = 1 + crossing_distance

            cost += move_cost

      return cost