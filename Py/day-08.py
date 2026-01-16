import sys


def solve():
    lines = sys.stdin.read().strip().splitlines()
    coords = [list(map(int, line.split(","))) for line in lines]
    n = len(coords)

    # We use distance squared to avoid the slow square root (math.sqrt)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d2 = sum((coords[i][k] - coords[j][k]) ** 2 for k in range(3))
            edges.append((d2, i, j))

    # Sort edges by distance (Kruskal's Algorithm)
    edges.sort()

    # UNION-FIND DATA STRUCTURE
    parent = list(range(n))
    size = [1] * n
    num_components = n

    def find(i):
        # Path Compression: makes the tree flat for near-constant lookup
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    def union(i, j):
        nonlocal num_components
        root_i, root_j = find(i), find(j)
        if root_i != root_j:
            # Union by Size: attach smaller tree to larger tree
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            num_components -= 1
            return True
        return False

    for idx, (_, i, j) in enumerate(edges):
        if idx == 1000:
            all_sizes = sorted(
                [size[k] for k in range(n) if parent[k] == k], reverse=True
            )
            print(f"Part 1: {all_sizes[0] * all_sizes[1] * all_sizes[2]}")

        # Perform the union
        if union(i, j):
            # Part 2: Last connection to make one single circuit
            if num_components == 1:
                print(f"Part 2: {coords[i][0] * coords[j][0]}")
                break


if __name__ == "__main__":
    solve()
