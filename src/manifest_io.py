import manifest_parser
import numpy

UNUSED = -1

def get_file_name() -> str:
      input_file_name = input("Enter name of manifest: ")

      if not input_file_name:
            raise ValueError("No file name provided")

      # input data files are placed in ./data within repo root
      input_file_name = "data/" + input_file_name

      return input_file_name


def load_ship_manifest(file_path: str) -> tuple[numpy.ndarray, dict[tuple[int, int], str]]:
      grid = numpy.full((8, 12), numpy.nan, dtype=float)
      description_lines = {} # store descriptions: desc[(r,c)] = "description_text"

      with open(file_path, "r") as file:
            for line in file:
                  line = line.strip()
                  if not line:
                        continue

                  # expected line format: [row,column], {WWWWW}, text_field
                  row, column, weight, text_field = manifest_parser.parse_manifest_line(line)

                  # convert to 0-based index
                  row_index = row - 1
                  column_index = column - 1

                  if text_field == "NAN":
                        grid[row_index, column_index] = numpy.nan
                  elif text_field == "UNUSED":
                        grid[row_index, column_index] = UNUSED
                  else:
                        grid[row_index, column_index] = weight
                        description_lines[(row, column)] = text_field

      return grid, description_lines


def load_manifest_from_user():
      return load_ship_manifest(get_file_name())