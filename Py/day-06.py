import sys
from math import prod


def solver(task_input):
    """
    Solves both parts using optimized transpose and C-based math functions.
    """
    # Split into lines and remove the empty ones
    data = [line for line in task_input.splitlines() if line.strip()]
    if not data:
        return 0, 0

    # The operators (+ or *) are on the very last line
    operators = data[-1].split()
    # The grid of numbers is everything except that last line
    grid_lines = data[:-1]

    # zip(*grid_lines) turns columns into rows.
    # We then turn each column into a list of integers.
    columns = [
        [int(x) for x in col if x.strip()]
        for col in zip(*[row.split() for row in grid_lines])
    ]

    p1 = 0
    for i, nums in enumerate(columns):
        op = operators[i]
        # Use C-optimized sum() and prod()
        p1 += prod(nums) if op == "*" else sum(nums)

    # In Part 2, numbers are formed vertically.
    # Example:
    # Row 1: 1 . 4
    # Row 2: 2 . 5
    # Becomes numbers: 12 and 45
    p2 = 0
    temp_val = 0
    op_idx = 0
    current_op = operators[0]

    # We iterate through the columns using the zip(*) trick again
    for col_chars in zip(*grid_lines):
        # Join the characters vertically to form the number string
        # Example: ('1', '2') -> "12"
        combined_str = "".join(col_chars).strip()

        if combined_str:
            # If we found a number, convert and apply the current operator
            num = int(combined_str)
            if current_op == "*":
                # If temp_val is 0, we start with the first number
                temp_val = (temp_val * num) if temp_val != 0 else num
            else:
                temp_val += num
        else:
            # If we hit a space/gap, the current problem is over.
            # Add to total and move to the next operator.
            p2 += temp_val
            temp_val = 0
            op_idx += 1
            if op_idx < len(operators):
                current_op = operators[op_idx]

    # Don't forget the last accumulated value!
    p2 += temp_val

    return p1, p2


if __name__ == "__main__":
    # Standard boilerplate to run from terminal: python script.py < input.txt
    raw_data = sys.stdin.read()
    if raw_data:
        res1, res2 = solver(raw_data)
        print(f"Part 1: {res1}")
        print(f"Part 2: {res2}")
