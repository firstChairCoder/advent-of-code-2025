import sys
from itertools import combinations, pairwise


def solve():
    # We turn each line like "1,2" or "(1,2)" into a (1, 2) tuple
    points = []
    for line in sys.stdin:
        if line.strip():
            # Standard way to parse "x,y"
            points.append(
                tuple(map(int, line.replace("(", "").replace(")", "").split(",")))
            )

    if not points:
        return

    # Helper function to calculate area (inclusive)
    def get_area(x1, y1, x2, y2):
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    # We create a list of all perimeter lines of the shape
    # pairwise([A, B, C]) -> (A, B), (B, C)
    edges = []
    for (a, b), (c, d) in pairwise(points + [points[0]]):
        # We store edges as (min_x, min_y, max_x, max_y) for easy comparison
        edges.append((min(a, c), min(b, d), max(a, c), max(b, d)))

    # Every pair of points in the input defines a candidate rectangle
    candidates = []
    for p1, p2 in combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2
        candidates.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    # Sort candidates by area, largest first
    candidates.sort(key=lambda p: get_area(*p), reverse=True)

    # Part 1: The largest possible area between any two points
    # (The first item in our sorted list)
    print(f"Part 1: {get_area(*candidates[0])}")

    # Part 2: The largest "Solid" area
    for cx1, cy1, cx2, cy2 in candidates:
        # Check if any edge of the shape passes THROUGH this rectangle
        is_invalid = False
        for ex1, ey1, ex2, ey2 in edges:
            # Intersection logic: if the edge is inside the rectangle bounds
            if ex1 < cx2 and ey1 < cy2 and ex2 > cx1 and ey2 > cy1:
                is_invalid = True
                break

        # If no edges intersected, this is our winner!
        if not is_invalid:
            print(f"Part 2: {get_area(cx1, cy1, cx2, cy2)}")
            break


if __name__ == "__main__":
    solve()
