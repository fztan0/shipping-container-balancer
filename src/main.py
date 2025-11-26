import debug
import manifest_io
import visualization

def main():
      # example receive
      puzzle = manifest_io.load_manifest_from_user()

      debug.debug_print_formatted_loaded_manifest(puzzle)
      # debug.debug_print_raw_loaded_manifest(puzzle_state)
      debug.debug_print_weight_grid(puzzle)
      #debug.debug_print_totalWeight_eachSide(puzze)
      #debug.debug_getContainers(puzzle)
      #debug.debug_validContainers(puzzle)
      #debug.debug_getNextPosition(puzzle)
      # debug.debug_testCraneCost(puzzle)
      # debug.debug_updateState(puzzle)
      # debug.debug_hashMap(puzzle)
      debug.debug_ucsAlg(puzzle)
      visualization.visualize_state(puzzle)




if __name__ == "__main__":
      main()