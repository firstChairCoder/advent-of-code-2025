import sys
import functools as ft


def solve():
    # THE INPUT HACK:
    # This builds the entire graph dictionary in one go.
    # We split each line by the colon, thenn split the right side by whitespace.
    # 'iter(sys.stdin.readline, "")' is a fast way to consume the streamm.
    try:
        G = {
            parts[0].strip(): parts[1].split()
            for line in iter(sys.stdin.readline, "")
            if (parts := line.split(":", 1))
        }
    except EOFError:
        return

    @ft.cache
    def paths(src, dest):
        # BASE CASE: We've arrived
        if src == dest:
            return 1

        # RECURSIVE STEP:
        # Sum up paths from all neighbors.
        # G.get(src, []) handles 'sink' nodes like "out" that have no neighbors.
        return sum(paths(neighbor, dest) for neighbor in G.get(src, []))

    # PART 1: Straight line
    p1 = paths("you", "out")

    # PART 2: The "Acyclic Multiplication" logic
    # In a DAG, only one of these two routes can physically exist.
    # The other will automatically result in 0.
    p2 = paths("svr", "dac") * paths("dac", "fft") * paths("fft", "out") + paths(
        "svr", "fft"
    ) * paths("fft", "dac") * paths("dac", "out")

    print(f"Part 1 Answer: {p1}")
    print(f"Part 2 Answer: {p2}")


if __name__ == "__main__":
    # Standard practice for deep graph recursionn
    sys.setrecursionlimit(10000)
    solve()
