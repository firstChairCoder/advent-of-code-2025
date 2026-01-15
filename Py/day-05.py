import sys

def run_optimized(task_input):
    """
    Solves the puzzle by checking which ingredients fall into ranges (Part 1)
    and calculating the total unique numbers covered by all ranges (Part 2).
    """

    # We split the input into two chunks: the range definitions and the ingredient list.
    raw_ranges, raw_ingredients = task_input.strip().split("\n\n")

    # We convert the strings into Python 'range' objects.
    # Why? Because 'x in range(start, end)' is mathematically optimized and extremely fast.
    ranges = []
    for line in raw_ranges.splitlines():
        # Example: "10-20" becomes start=10, end=20
        start, end = map(int, line.split("-"))
        # Python ranges are exclusive at the end, so we add 1 to include the 'end' number.
        ranges.append(range(start, end + 1))

    # Convert the ingredients chunk into a list of integers.
    ingredients = [int(i) for i in raw_ingredients.splitlines()]

    # For every ingredient, check if it exists in ANY of our range objects.
    # 'any()' stops checking as soon as it finds the first match (short-circuiting).
    p1 = sum(1 for i in ingredients if any(i in r for r in ranges))
    print(f"Part 1: {p1}")

    # To find the total numbers covered without double-counting overlaps, we sort them first.
    # Sorting by the 'start' value allows us to process the grid from left to right.
    sorted_ranges = sorted(ranges, key=lambda r: r.start)

    if not sorted_ranges:
        print("Part 2: 0")
        return

    # Initialize our tracker with the first range in the sorted list.
    current_range = sorted_ranges[0]
    total_count = len(current_range)

    # Loop through the rest of the ranges and compare them to our "current_range"
    for next_r in sorted_ranges[1:]:
        # CASE A: The next range overlaps or touches the current one.
        # [Current Range]
        #       [Next Range]
        if next_r.start <= current_range.stop:
            # Only if the next range pushes the boundary further do we add to the count.
            if next_r.stop > current_range.stop:
                # We only add the 'new' territory covered.
                total_count += next_r.stop - current_range.stop
                # Update our current reach to the new furthest point.
                current_range = range(current_range.start, next_r.stop)

        # CASE B: There is a gap between the ranges.
        # [Current Range]   ...gap...   [Next Range]
        else:
            # Since there is no overlap, we add the entire length of the new range.
            total_count += len(next_r)
            # This new range now becomes the one to beat!
            current_range = next_r

    print(f"Part 2: {total_count}")


# This block only runs if you call this file directly (e.g., python your_file.py)
if __name__ == "__main__":
    # We read from 'sys.stdin' so you can pipe your input file into the script:
    # Example: python solve.py < input.txt
    try:
        user_data = sys.stdin.read()
        if user_data:
            run_optimized(user_data)
        else:
            print("Error: No input data detected. Try: python filename.py < input.txt")
    except EOFError:
        pass
