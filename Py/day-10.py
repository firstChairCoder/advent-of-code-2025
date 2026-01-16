import sys
from functools import cache


def solve_machine():
    total_indicator_presses = 0
    total_joltage_presses = 0

    for line in sys.stdin:
        if not line.strip():
            continue

        # PARSING
        # Format: [Indicator] [Button1] [Button2] ... [Joltage]
        parts = line.split()
        
        # Indicator: [.#..#] -> bitmask
        indicator_str = parts[0][1:-1]
        target_indicator_mask = 0
        for i, char in enumerate(indicator_str):
            if char == "#":
                target_indicator_mask |= 1 << i

        # Joltage: (38,27,...) -> tuple of ints
        target_joltage = tuple(map(int, parts[-1][1:-1].split(",")))

        # Buttons: (0,1,4) -> list of bitmasks
        buttons = []
        for b_str in parts[1:-1]:
            mask = 0
            for pos in b_str[1:-1].split(","):
                mask |= 1 << int(pos)
            buttons.append(mask)

        # PRE-COMPUTE PARITY COMBINATIONS
        # We need to know every way to combine buttons to hit a parity mask
        # Map: bitmask -> list of (press_count, button_usage_mask)
        # For Part 2, we need to know WHICH buttons were used to subtract them correctly
        combos = {0: 0}  # {bitmask: num_presses}
        for b_mask in buttons:
            new_combos = combos.copy()
            for mask, count in combos.items():
                new_mask = mask ^ b_mask
                if new_mask not in new_combos or count + 1 < new_combos[new_mask]:
                    new_combos[new_mask] = count + 1
            combos = new_combos

        # --- PART 1: INDICATOR LIGHTS ---
        # The fewest presses to hit the exact parity mask
        if target_indicator_mask in combos:
            total_indicator_presses += combos[target_indicator_mask]

        # --- PART 2: JOLTAGE LEVELS ---
        # RECURSIVE SOLVER (The "Binary Lifting" logic)
        @cache
        def get_min_joltage_presses(current_goal):
            # Base Case: All joltages are zero
            if all(v == 0 for v in current_goal):
                return 0

            # Determine the parity bitmask of the current goal
            # current_parity_mask = sum((v % 2) << i for i, v in enumerate(current_goal))
            current_parity = 0
            for i, v in enumerate(current_goal):
                if v % 2 != 0:
                    current_parity |= 1 << i

            # If the parity mask isn't reachable by any button combo,
            # this path is impossible
            if current_parity not in combos:
                return float("inf")

            best = float("inf")

            # We must press a combination that satisties the current parity
            # But there might be multiple combinations  that result in the same mask!
            # However, for this puzzle, the "cheapest" parity match is usually best
            for mask, presses in combos.items():
                if mask == current_parity:
                    # Subtract the effect of these buttons and divide by 2
                    next_goal = []
                    possible = True
                    for i, val in enumerate(current_goal):
                        # If bit i is set in the mask, it means an odd button combo hit it
                        effect = (mask >> i) & 1
                        remaining = val - effect
                        if remaining < 0:
                            possible = False
                            break
                        next_goal.append(remaining // 2)
                    if possible:
                        res = get_min_joltage_presses(tuple(next_goal))
                        if res != float("inf"):
                            best = min(best, presses + 2 * res)

            return best

        joltage_res = get_min_joltage_presses(target_joltage)
        if joltage_res != float("inf"):
            total_joltage_presses += joltage_res

    print(f"Fewest Button Presses: {total_indicator_presses}")
    print(f"Actual Button presses for counters: {total_joltage_presses}")


if __name__ == "__main__":
    # Increase recursion depth for deep binary lifting
    sys.setrecursionlimit(5000)
    solve_machine()
