import numpy

UNUSED = -1.0

def debug_print_formatted_loaded_manifest(grid: numpy.ndarray, description: dict[tuple[int, int], str]):
      for r in range(1, 9): # rows 1–8
            for c in range(1, 13): # cols 1–12
                  value = grid[r - 1, c - 1]

                  if numpy.isnan(value):
                        weight = 0
                        token = "NAN"
                  elif value == UNUSED:
                        weight = 0
                        token = "UNUSED"
                  else:
                        weight = int(value)
                        token = description.get((r, c), "") # empty string in case it does happen

                  # format weight as 5 digits with 0-padding
                  weight_field = f"{weight:05d}"

                  # if a description exists, show it; otherwise show token (NAN/UNUSED)
                  text_field = token if token else "NO DESCRIPTION, EITHER INTENDED OR ERROR"

                  print(f"[{r:02d},{c:02d}], {{{weight_field}}}, {text_field}")

      return


def debug_print_raw_loaded_manifest(grid: numpy.ndarray, description: dict[tuple[int, int], str]):
      print(grid)
      print(description)
      return