# --- Input Reading ---

# Read the data.
# 1. open('input-03-2025.txt'): Opens the specified file for reading.
# 2. .read(): Reads the entire content of the file as a single string.
# 3. .split(): Splits the string content into a list of substrings
#    based on whitespace (spaces, newlines, tabs).
#    Each element in 'data' is expected to be a string of digits.
data = open("input-03-2025.txt").read().split()

# --- Core Function: Greedy Subsequence Selection ---


# Define a function 'maxj' that implements a greedy algorithm.
# It finds the largest possible integer that can be formed by
# selecting 'k' digits from the input string 's' while preserving their original relative order.
def maxj(s, k):
    # 'r' will store the selected digits, which will form the maximized number.
    r = ""

    # The loop iterates 'k' times, once for each digit we need to select for the result 'r'.
    # 'skip' tracks how many characters *must* be left at the end of the original string 's'
    # to ensure that exactly 'k' characters can still be chosen.
    # The loop runs for skip = k-1, k-2, ..., 1, 0.
    # Example: If k=5, the loop starts with skip=4 (meaning 4 more digits must be chosen
    # from the rest of the string, so we must leave at least 4 chars unexamined).
    for skip in range(k - 1, -1, -1):
        # 1. Define the search range: s[:len(s)-skip]
        # This is the segment (a slice) of the current string 's' from which we can safely choose the next digit.
        # We must ensure that after choosing this digit, there are still at least 'skip'
        # characters remaining in 's' (i.e., s[j+1:]) to select the remaining 'skip' digits.
        search_range = s[: len(s) - skip]

        # 2. Greedy Choice: Find the largest available digit in the search range.
        max_char = max(search_range)

        # 3. Find the index 'j' of the *first* occurrence of this maximum digit
        #    within the safe search range (s).
        j = s.index(max_char)

        # 4. Update the result and the remaining string:
        # Append the chosen maximum digit (s[j]) to the result string 'r'.
        r = r + s[j]

        # Update the string 's' to start *after* the chosen digit.
        # s[j+1:] ensures that the relative order of the remaining digits is maintained.
        s = s[j + 1 :]

    # After the loop finishes (i.e., 'k' digits have been selected),
    # convert the resulting string 'r' into an integer and return it.
    return int(r)


# --- Calculation and Output ---

# Uses a generator expression to calculate maxj(s, 2) for every string 's' in the 'data' list,
# and then sums all the resulting integers.
# This finds the sum of the largest 2-digit numbers that can be formed from each input string.
print(sum(maxj(s, 2) for s in data))

# Performs the same operation but selects the largest 12-digit number from each string.
# This finds the sum of the largest 12-digit numbers that can be formed from each input string.
print(sum(maxj(s, 12) for s in data))
