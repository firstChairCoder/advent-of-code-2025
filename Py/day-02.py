import re
# The 're' module is imported for powerful, optimized regular expression processing.


# --- Regular Expression Setup ---

# Part 1 Pattern: Check for numbers made of EXACTLY two identical halves (e.g., 1212, 55).
# r'^(\d+)\1$' breakdown:
# ^          : Start of the string.
# (\d+)      : Capture Group 1: Match one or more digits.
# \1         : Match the exact content captured by Group 1.
# $          : End of the string.
# The re.compile() function pre-processes the pattern string into a pattern object,
# which makes repeated searching inside the loop faster.
pattern_a = re.compile(r"^(\d+)\1$")

# Part 2 Pattern: Check for numbers made of a repeating pattern (e.g., 1212, 111, 123123123).
# r'^(\d+)\1+$' breakdown:
# ^          : Start of the string.
# (\d+)      : Capture Group 1: Match one or more digits (the base repeating block).
# \1+        : Match the exact content of Group 1 *one or more* additional times.
# $          : End of the string.
pattern_b = re.compile(r"^(\d+)\1+$")


# --- Initialization ---

# 'a' sums the invalid numbers for the Part 1 rule (exactly two halves).
a = 0
# 'b' sums the invalid numbers for the Part 2 rule (any repeating pattern, which includes Part 1).
b = 0

# --- File Input and Parsing ---

# Read the entire file content into a single string.
file_content = open("input-02-2025.txt").read()

# Use re.findall to extract all range pairs (X-Y) from the input string.
# r'(\d+)-(\d+)' breakdown:
# (\d+)      : Capture Group 1: Matches and captures the starting number (lo).
# -          : Matches the literal dash separator.
# (\d+)      : Capture Group 2: Matches and captures the ending number (hi).
# The result is a list of tuples: [('1061119', '1154492'), ('3', '23'), ...]
# The loop iterates through these tuples.
for lo, hi in re.findall(r"(\d+)-(\d+)", file_content):
    # Convert the string boundaries to integers once per range.
    start = int(lo)
    end = int(hi)

    # --- Inner Loop: Processing Each Number ---

    # Iterate over every integer 'i' in the defined range (inclusive).
    for i in range(start, end + 1):
        # Convert the current integer 'i' to its string representation only once.
        s = str(i)

        # Check Part 1 rule using the pre-compiled pattern_a and re.search.
        # re.search is efficient because it stops immediately upon finding a match.
        if pattern_a.search(s):
            a += i

        # Check Part 2 rule using the pre-compiled pattern_b.
        # This check is independent of Part 1, summing numbers that match *any* repeating pattern.
        if pattern_b.search(s):
            b += i

# --- Output ---
# Print the final sums for both parts of the problem.
print(a, b)
