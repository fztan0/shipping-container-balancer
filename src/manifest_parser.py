UNUSED = -1

def parse_manifest_line(line: str) -> tuple[int, int, int, str]:
    """Parse a manifest line into (row, column, weight, text) components"""
    # Parse the line: [RR,CC], {WWWWW}, description
    parts = line.split("], ", 1)
    coordinate_field = parts[0] + "]"  # "[RR,CC]"
    rest = parts[1]  # "{WWWWW}, description"
    weight_text = rest.split(", ", 1)
    weight_field = weight_text[0].strip()
    text_field = weight_text[1].strip().strip()  # Remove any trailing whitespace

    # Parse coordinates
    coord_stripped = coordinate_field.strip("[]")
    rr, cc = coord_stripped.split(",")
    row = int(rr)
    column = int(cc)

    # Parse weight inside { }
    weight = int(weight_field.strip("{}"))

    # Normalize text field
    text_upper = text_field.upper()

    return row, column, weight, text_upper