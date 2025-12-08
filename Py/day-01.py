# --- Global Configuration ---

# The current position of the lock. Starts at 50.
lock_current_state = 50
# The size of the circular lock (100 possible positions).
lock_wrap = 100


# --- Movement Functions (Calculating Final State) ---


def left_turn(n: int):
    """
    Calculates the new lock state after turning Left `n` clicks.
    """
    # The result is (Current Position - Distance) modulo Lock Size, i.e. 100.
    # Python's modulo operator (%) handles negative numbers correctly for circular arrays:
    # e.g., (50 - 60) % 100 = -10 % 100 = 90
    return (lock_current_state - n) % lock_wrap


def right_turn(n: int):
    """
    Calculates the new lock state after turning Right `n` clicks.
    """
    # The result is (Current Position + Distance) modulo Lock Size, i.e. 100.
    # e.g., (50 + 60) % 100 = 110 % 100 = 10
    return (lock_current_state + n) % lock_wrap


# --- Wrap Counting Function ---


def wraps(value, delta):
    """
    Calculates how many times the lock wraps around the `0` boundary
    given a starting `value` and a signed distance `delta`.
    This uses O(1) arithmetic instead of simulating every step.
    """
    # Calculate the theoretical position without any modulo wrap-around.
    tmp = value + delta

    if delta > 0:  # Right (R) turn
        # The number of wraps is determined by the difference in "full cycle counts".
        # Integer division (//) gives the number of times 100 fits into the number.
        # This count represents the number of full wraps passed.
        clicks = (tmp // lock_wrap) - (value // lock_wrap)
    else:  # Left (L) turn (delta is negative)
        # For negative deltas, using (value - 1) helps correct for boundary cases
        # near zero with Python's 'floor' division on negative numbers.
        clicks = ((value - 1) // lock_wrap) - ((tmp - 1) // lock_wrap)

    # Return the absolute count of wraps (always a positive number).
    return abs(clicks)


#

# --- Main Program Logic ---


def main():
    # Declare the global variable to be modified inside the function.
    global lock_current_state
    # Map direction characters from the input file to the corresponding function.
    function_array = {"R": right_turn, "L": left_turn}

    # Counter for Block 1's goal: how many times the state lands exactly on 0.
    zero_counter = 0

    # Counter for Block 2's goal: total number of times the lock wraps (crosses 0).
    wrap_counter = 0

    print(f"--- Starting state: {lock_current_state} (Wrap limit: {lock_wrap}) ---")

    try:
        # Open and process the input file.
        with open("input-2025.txt") as t:
            for line in t:
                line = line.strip()
                if not line:
                    continue

                direction = line[0].upper()
                try:
                    # Extract the numerical distance (n) from the rest of the string.
                    n = int(line[1:])
                except ValueError:
                    # skip lines where the distance is not an integer.
                    print(f"Skipping malformed line: {line} (non-integer rotation)")
                    continue

                # --- Logic for Block 2 ---

                # Determine the signed distance (delta) for the wraps function.
                delta = n if direction == "R" else -n
                # Calculate the number of wraps using the O(1) arithmetic function.
                lock_wrap_count = wraps(lock_current_state, delta)

                # --- Logic for Block 1 ---

                # Calculate the final position using the appropriate modulo function (right_turn or left_turn).
                new_state = function_array[direction](n)

                # Update the total wrap counter.
                wrap_counter += lock_wrap_count
                # Update the global state for the next instruction.
                lock_current_state = new_state

                # --- Final Checks ---

                # Check if the final position landed exactly on 0 (Part 1 Goal).
                if lock_current_state == 0:
                    zero_counter += 1

    except FileNotFoundError:
        # Inform the user if the required input file is missing.
        print(
            "\nError: 'input.txt' not found. Please create it with lines like 'L67' or 'R21'."
        )
        return  # Exit main function

    # --- Output Results ---
    print(f"Part 1 Answer: {zero_counter}")
    print(f"Part 2 Answer: {wrap_counter}")


# Standard Python entry point: ensures main() runs when the script is executed directly.
if __name__ == "__main__":
    main()
