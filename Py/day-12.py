import sys


def solve():
    # PARSE INPUT
    raw_data = sys.stdin.read().split("\n\n")
    present_blocks = raw_data[:-1]
    region_lines = raw_data[-1].strip().split("\n")

    # Sttore shapes as sets of relative (x, y) coordinates
    shapes = []
    for block in present_blocks:
        lines = block.splitlines()
        # Assume first line is ID, shape starts at index 1
        shape_set = set()
        for y, line in enumerate(lines[1:]):
            for x, char in enumerate(line):
                if char == "#":
                    shape_set.add((x, y))
        shapes.append(shape_set)

    # PART 1: AREA HEEURISTIC
    # Fast count of '#' per shape
    shape_areas = [len(s) for s in shapes]

    possible_p1 = 0
    for line in region_lines:
        # Parse "2x20: 1 0 5"
        size_str, counts_str = line.split(": ")
        w, h = map(int, size_str.split("x"))
        counts = list(map(int, counts_str.split()))

        total_area_needed = sum(c * a for c, a in zip(counts, shape_areas))
        if total_area_needed <= w * h:
            possible_p1 += 1

    print(f"Part 1 (Heuristic): {possible_p1}")
    
	# PART 2: TRUE PACKING (Simplified)
    # Part 2 usually requires actually checking if they fit without overlaps.
    


if __name__ == "__main__":
    solve()
