import debug
import manifest_io
import visualization
import logger

def main():
      # example receive
      logger.initialize_logger()
      manifest_io.load_manifest_from_user()

      # debug.debug_print_formatted_loaded_manifest(puzzle)
      # # debug.debug_print_raw_loaded_manifest(puzzle_state)
      # debug.debug_print_weight_grid(puzzle)
      #debug.debug_print_totalWeight_eachSide(puzzle)
      list_moves = [("01", "04"), ("03", "03"), ("01", "03"), ("03", "04"), ("04", "01"), ("10", "02")]
      logger.log_move_operation(list_moves)
      logger.log_finish_operation()
      logger.log_kill()
      logger.write_logger_to_desktop()
      # visualization.visualize_state(puzzle)



if __name__ == "__main__":
      main()