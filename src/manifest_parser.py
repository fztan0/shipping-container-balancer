
# parse line: [RR,CC], {WWWWW}, description
def parse_manifest_line(line: str) -> tuple[int, int, int, str]:

      # parse[0]: "[RR,CC"    missing ] is intentional
      # parse[1]: "{WWWWW}, description"
      parts = line.split("], ", 1)

      coordinate_stripped = parts[0].strip("[")

      rest_of_line = parts[1].split(", ", 1)

      # parse coordinates
      rr, cc = coordinate_stripped.split(",")
      row = int(rr)
      column = int(cc)

      # parse weight inside { }
      weight = int(rest_of_line[0].strip("{}"))

      # parse text field
      text_field = rest_of_line[1].strip()

      return row, column, weight, text_field