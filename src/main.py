import debug
import manifest_io

def main():
      # example receive
      puzzle_state = manifest_io.load_manifest_from_user()
      debug.debug_print_formatted_loaded_manifest(puzzle_state)

      # debug.debug_print_raw_loaded_manifest(puzzle_state)
      debug.debug_print_weight_grid(puzzle_state)



if __name__ == "__main__":
      main()