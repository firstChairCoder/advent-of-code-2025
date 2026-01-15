import sys

# Read all lines from standard input, strip whitespace, and turn each line into a list of characters
# This creates a 2D grid: grid[row][column]
grid = [list(line) for line in sys.stdin.read().strip().splitlines()]
ROWS, COLS = len(grid), len(grid[0])

# These represent the 8 neighbors (Up, Down, Left, Right, and 4 Diagonals)
# Format: (change_in_row, change_in_col)
NEIGHBORS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]


def count_active_neighbors(r, c):
    """Counts how many '@' symbols surround the cell at grid[r][c]."""
    count = 0
    for dr, dc in NEIGHBORS_8:
        nr, nc = r + dr, c + dc
        # Stay within the grid boundaries and check if neighbor is an '@'
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == "@":
            count += 1
    return count


# MAIN SIMULATION LOOP
first_pass_count = 0
total_removed = 0
is_first_iteration = True

while True:
    to_remove = []

    # Scan every cell in the grid
    for r in range(ROWS):
        for c in range(COLS):
            # We only care about active cells ('@')
            if grid[r][c] == "@":
                # If a cell has fewer than 4 neighbors, it's marked for removal
                if count_active_neighbors(r, c) < 4:
                    to_remove.append((r, c))

    # Part 1 logic: How many would be removed in the very first round?
    if is_first_iteration:
        print(f"Part 1 (Valids): {len(to_remove)}")
        is_first_iteration = False

    # If no cells were marked for removal, the simulation is finished
    if not to_remove:
        break

    # Perform the removals by changing '@' to '.'
    for r, c in to_remove:
        grid[r][c] = "."

    total_removed += len(to_remove)

print(f"Part 2 (Total Removed): {total_removed}")
