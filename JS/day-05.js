const fs = require("fs");

/**
 * --- Shared Core Logic ---
 */

/**
 * Converts a text string like "10-20" into a range object.
 * Complexity: O(1)
 */
function createRangeFromText(text) {
  const tokens = text.split("-");

  const begin = parseInt(tokens.shift());
  const end = parseInt(tokens.shift());

  return { begin: begin, end: end };
}

/**
 * OPTIMIZED RANGE CONSOLIDATION (O(R log R))
 * This function sorts the ranges and then merges them in a single pass.
 * This is vastly more performant than the previous O(R^2) or O(R^3) approach.
 *
 * @param {Array<{begin: number, end: number}>} allRanges - The array of ranges to consolidate.
 * @returns {Array<{begin: number, end: number}>} A new array containing only the consolidated ranges.
 */
function consolidateRangesOptimized(allRanges) {
  if (allRanges.length < 2) {
    return allRanges;
  }

  // 1. Sort the ranges by their beginning point (O(R log R))
  // This is the key to single-pass merging.
  allRanges.sort((a, b) => a.begin - b.begin);

  const consolidated = [];
  let current = allRanges[0]; // Start with the first (smallest) range

  // 2. Iterate and Merge (O(R))
  for (let i = 1; i < allRanges.length; i++) {
    const next = allRanges[i];

    // Check for overlap or adjacency (touching: next.begin <= current.end + 1)
    if (next.begin <= current.end + 1) {
      // Merge: expand the current end to the maximum of the two ends
      current.end = Math.max(current.end, next.end);
    } else {
      // No overlap: The current consolidated range is complete.
      // Finalize it and start a new 'current' range.
      consolidated.push(current);
      current = next;
    }
  }

  // Push the final 'current' range after the loop finishes
  consolidated.push(current);

  return consolidated;
}

/**
 * --- Part 1 Logic (Checking individual numbers) ---
 * Uses Binary Search for a faster O(log R) lookup per number.
 */

/**
 * Performs a binary search-like check for a number in a sorted, consolidated range list.
 * @param {Array<{begin: number, end: number}>} ranges - The sorted array of consolidated ranges.
 * @param {number} number - The number to check.
 * @returns {boolean} True if the number is found within any range.
 */
function isNumberInRange(ranges, number) {
  let low = 0;
  let high = ranges.length - 1;

  while (low <= high) {
    const midIndex = Math.floor((low + high) / 2);
    const range = ranges[midIndex];

    if (number >= range.begin && number <= range.end) {
      // Found the range
      return true;
    } else if (number < range.begin) {
      // The number is to the left of the current range
      high = midIndex - 1;
    } else {
      // The number is to the right of the current range
      low = midIndex + 1;
    }
  }
  return false;
}

function part1(consolidatedRanges, availablePartLines) {
  let counter = 0;

  // Complexity: O(N * log R), where N is number of lines, R is number of ranges.
  for (const rawLine of availablePartLines) {
    const number = parseInt(rawLine);

    if (isNumberInRange(consolidatedRanges, number)) {
      counter += 1;
    }
  }

  console.log("Part 1 Answer:", counter);
}

/**
 * --- Part 2 Logic (Counting total covered integers) ---
 * Remains O(R) and is already optimal.
 */

function part2(consolidatedRanges) {
  let counter = 0;

  // Complexity: O(R), where R is the number of consolidated ranges.
  for (const range of consolidatedRanges) {
    // Count of integers in the range [begin, end] is (end - begin + 1)
    counter += range.end - range.begin + 1;
  }

  console.log("Part 2 Answer:", counter);
}

/**
 * --- Main Execution ---
 */
function run() {
  const input = fs
    .readFileSync("input-05-2025.txt", { encoding: "utf-8" })
    .trim();

  const rawParts = input.split("\n\n");
  const freshPart = rawParts.shift().trim(); // Initial ranges
  const availablePart = rawParts.shift().trim(); // List of numbers

  const freshPartLines = freshPart.split("\n");
  const availablePartLines = availablePart.split("\n");

  // 1. Initialize and populate the ranges
  let initialRanges = [];
  for (const rawLine of freshPartLines) {
    initialRanges.push(createRangeFromText(rawLine.trim()));
  }

  // 2. OPTIMIZED CONSOLIDATION
  // The result, `consolidatedRanges`, is now sorted, which is key for Part 1 optimization.
  const consolidatedRanges = consolidateRangesOptimized(initialRanges);

  // --- Run the parts ---

  // Part 1: uses the sorted consolidated ranges for fast lookup
  part1(consolidatedRanges, availablePartLines);

  // Part 2: uses the properties of the consolidated ranges
  part2(consolidatedRanges);
}

console.time("execution time");
run();
console.timeEnd("execution time");
