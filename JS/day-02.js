"use strict"; // Enables strict mode to catch common coding errors (like undeclared variables)

/**
 * Node.js 'fs' module for File System access.
 * We use this to read the puzzle input from the local directory.
 */
const fs = require("fs");

/**
 * --- REGEX PATTERNS ---
 * Both patterns use "Backreferences" (\1) to detect repetition.
 * * patternA: Matches strings composed of exactly two identical parts.
 * Example: "1212" -> Group 1 is "12", \1 matches "12". Result: Match.
 * * patternB: Matches strings where the first part repeats one OR MORE times.
 * Example: "121212" -> Group 1 is "12", \1+ matches "1212". Result: Match.
 */
const patternA = /^(\d+)\1$/;
const patternB = /^(\d+)\1+$/;

// Accumulators for our two-part solution
let a = 0; // Total sum for Part 1
let b = 0; // Total sum for Part 2

/**
 * File Reading:
 * We read the entire file into memory as a UTF-8 string.
 */
const fileContent = fs.readFileSync("inputs/input-02-2025.txt", "utf8");

/**
 * rangeRegex:
 * Looks for the pattern "Number-Number" (e.g., "100-120").
 * The 'g' flag (global) allows us to find all occurrences in the file.
 */
const rangeRegex = /(\d+)-(\d+)/g;
let match;

/**
 * --- MAIN LOOP ---
 * .exec() returns a match object containing capturing groups:
 * match[0]: The full string (e.g., "100-120")
 * match[1]: The first capture group (the start number)
 * match[2]: The second capture group (the end number)
 */
while ((match = rangeRegex.exec(fileContent)) !== null) {
  // Convert the string matches into base-10 integers
  const start = parseInt(match[1], 10);
  const end = parseInt(match[2], 10);

  /**
   * --- RANGE ITERATION ---
   * We iterate through every integer in the inclusive range.
   */
  for (let i = start; i <= end; i++) {
    // Regex .test() requires a string. We cast the number to a string here.
    const s = String(i);

    // Part 1: Check if the number repeats exactly twice
    if (patternA.test(s)) {
      a += i;
    }

    // Part 2: Check if the number repeats two or more times
    if (patternB.test(s)) {
      b += i;
    }
  }
}

// Output the final sums to the terminal
console.log(a, b);
