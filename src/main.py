import debug
import manifest_io
import logger

def main():
      # example receive
      logger.initialize_logger()
      puzzle = manifest_io.load_manifest_from_user()

      debug.debug_print_formatted_loaded_manifest(puzzle)
      # debug.debug_print_raw_loaded_manifest(puzzle_state)
      debug.debug_print_weight_grid(puzzle)
      #debug.debug_print_totalWeight_eachSide(puzzle)
      logger.log_finish_operation()
      logger.log_kill()
      logger.write_logger_to_desktop()


if __name__ == "__main__":
      main()