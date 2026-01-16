def solve_beams(lines):
    # 'current_row_light' tracks if light is present in each column.
    # We initialize it based on where the light starts (the 'S' or '^' in row 0).
    width = len(lines[0])
    light_map = [0] * width

    # Initialize the first row's light sources
    for i, char in enumerate(lines[0]):
        if char in "S^":
            light_map[i] = 1

    total_splits = 0

    # Process the grid from the second row downwards
    for row_text in lines[1:]:
        # We need a copy or a strategy to avoid 'double-moving' light
        # (i.e., light moving from col 2 to 3, then 3 to 4 in the same row).
        # We use a temporary list to store changes.
        next_light_map = list(light_map)

        for i, char in enumerate(row_text):
            # If we find a splitter...
            if char in "S^":
                # Light from this column "splits" left and right
                if i > 0:
                    next_light_map[i - 1] += light_map[i]
                if i < width - 1:
                    next_light_map[i + 1] += light_map[i]

                # If this splitter received any light, count it for Part 1
                if light_map[i] > 0:
                    total_splits += 1

                # The splitter blocks vertical light, so reset this column to 0
                next_light_map[i] = 0

        light_map = next_light_map

    # Part 1: How many splitters were activated?
    # Part 2: Total intensity of light reaching the bottom.
    return total_splits, sum(light_map)


if __name__ == "__main__":
    with open("inputs/input-07-2025.txt", "r") as file:
        input_data = file.read().strip().split("\n")

    p1, p2 = solve_beams(input_data)
    print(f"Part 1 (Activated Splitters): {p1}")
    print(f"Part 2 (Total Beams at Bottom): {p2}")
