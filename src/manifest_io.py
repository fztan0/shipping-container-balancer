import manifest_parser
import puzzle_state

def get_file_name() -> str:
      input_file_name = input("Enter name of manifest: ")

      if not input_file_name:
            raise ValueError("No file name provided")

      # input data files are placed in ./data within repo root
      input_file_name = "data/" + input_file_name

      return input_file_name


def load_ship_manifest(file_path: str) -> 'PuzzleState':
      manifest_data = []

      with open(file_path, "r") as file:
            for line in file:
                  line = line.strip()
                  if not line:
                        continue

                  # parse line
                  row, column, weight, text_field = manifest_parser.parse_manifest_line(line)

                  # convert to 0-based indexes
                  row_index = row - 1
                  column_index = column - 1

                  # for PuzzleState, store all data including NAN/UNUSED flags
                  manifest_data.append((row_index, column_index, weight, text_field))

      return puzzle_state.PuzzleState.from_manifest_data(manifest_data)

def load_manifest_from_user() -> 'PuzzleState':
      return load_ship_manifest(get_file_name())