"use strict"; 
/**
 * Enabling strict mode:
 * - Prevents accidental globals
 * - Throws errors for unsafe behavior
 * - Allows JavaScript engines to optimize better
 * 
 * Think of this as "no silent mistakes allowed".
 */
const { readFileSync } = require("fs");


/* -------------------------------------------------------------------------- */
/*                            GLOBAL CONFIGURATION                             */
/* -------------------------------------------------------------------------- */

// The lock has positions from 0 to 99 (100 total positions).
// We start at position 50.
let lockCurrentState = 50;

// The size of the circular lock.
// When we move past 99, we wrap back to 0.
const LOCK_WRAP = 100;


/* -------------------------------------------------------------------------- */
/*                          MOVEMENT / TURN FUNCTIONS                          */
/* -------------------------------------------------------------------------- */

/**
 * Turn the lock LEFT by `n` clicks.
 *
 * This function does NOT mutate state.
 * It simply calculates and returns the new position.
 *
 * Why the weird math?
 * - JavaScript's `%` operator can return negative numbers.
 * - We normalize it so the result is ALWAYS between 0 and 99.
 */
function leftTurn(state, n) {
  // Example:
  // state = 10, n = 20
  // 10 - 20 = -10
  // (-10 % 100) = -10  ❌
  // (-10 + 100) = 90   ✅
  // 90 % 100 = 90
  return ((state - n) % LOCK_WRAP + LOCK_WRAP) % LOCK_WRAP;
}

/**
 * Turn the lock RIGHT by `n` clicks.
 *
 * This is simpler because positive modulo works as expected.
 */
function rightTurn(state, n) {
  // Example:
  // state = 90, n = 15
  // 90 + 15 = 105
  // 105 % 100 = 5
  return (state + n) % LOCK_WRAP;
}


/* -------------------------------------------------------------------------- */
/*                          WRAP (BOUNDARY CROSSING) LOGIC                     */
/* -------------------------------------------------------------------------- */

/**
 * Counts how many times we CROSS position 0
 * during a movement.
 *
 * Important:
 * - This does NOT simulate step-by-step movement.
 * - It uses math to compute wraps in O(1) time.
 *
 * @param {number} value - starting position (0–99)
 * @param {number} delta - signed movement (+ for right, - for left)
 * @returns {number} number of times we wrapped around 0
 */
function wraps(value, delta) {
  // Temporary unbounded position (no modulo applied yet)
  const tmp = value + delta;
  let clicks;

  if (delta > 0) {
    /**
     * RIGHT TURN LOGIC
     *
     * We compare how many full 100s fit before and after moving.
     * If the quotient increases, we crossed 0.
     */
    clicks =
      Math.floor(tmp / LOCK_WRAP) -
      Math.floor(value / LOCK_WRAP);
  } else {
    /**
     * LEFT TURN LOGIC
     *
     * Negative division is tricky.
     * Subtracting 1 shifts the boundary so we don't
     * falsely count when landing exactly on 0.
     */
    clicks =
      Math.floor((value - 1) / LOCK_WRAP) -
      Math.floor((tmp - 1) / LOCK_WRAP);
  }

  // Wrap count must always be positive
  return Math.abs(clicks);
}


/* -------------------------------------------------------------------------- */
/*                                  MAIN LOGIC                                 */
/* -------------------------------------------------------------------------- */

function main() {

  // Part 1:
  // How many times we LAND exactly on position 0
  let zeroCounter = 0;

  // Part 2:
  // How many times we CROSS position 0
  let wrapCounter = 0;

  /**
   * We copy the global state into a local variable.
   *
   * Why?
   * - Local variables are faster
   * - Avoids accidental mutation during the loop
   */
  let currentState = lockCurrentState;

  let buffer;
  try {
    /**
     * Read the file as ONE string.
     *
     * We intentionally avoid splitting immediately:
     * - Splitting creates many small strings
     * - This puts pressure on the Garbage Collector
     */
    buffer = readFileSync("../inputs/input-2025.txt", "utf8");
  } catch (err) {
    console.error("\nError: 'input-2025.txt' not found.");
    return;
  }

  /**
   * Split the input into lines.
   * Using a simple array and index-based loop
   * is faster than for...of on large inputs.
   */
  const lines = buffer.split("\n");
  const totalLines = lines.length;

  for (let i = 0; i < totalLines; i++) {
    const rawLine = lines[i];

    // Lines shorter than 2 characters can't be valid commands
    // Example valid line: "R15"
    if (rawLine.length < 2) continue;

    /**
     * We avoid .trim() and .toUpperCase():
     * - Index access is faster
     * - Input format is trusted
     */
    const direction = rawLine[0];
    const n = parseInt(rawLine.slice(1), 10);

    // Skip malformed lines
    if (isNaN(n)) continue;

    /* --------------------------- PART 2: WRAPS --------------------------- */

    // Convert direction to signed movement
    const delta =
      direction === "R" || direction === "r" ? n : -n;

    // Count how many times we crossed position 0
    wrapCounter += wraps(currentState, delta);

    /* -------------------------- PART 1: MOVEMENT -------------------------- */

    // Use direct branching instead of function maps (faster)
    if (delta > 0) {
      currentState = rightTurn(currentState, n);
    } else {
      currentState = leftTurn(currentState, n);
    }

    /* ---------------------------- FINAL CHECK ----------------------------- */

    // Count exact landings on 0
    if (currentState === 0) {
      zeroCounter += 1;
    }
  }

  // Persist the final state back to the global variable
  lockCurrentState = currentState;

  console.log(`Part 1 Answer: ${zeroCounter}`);
  console.log(`Part 2 Answer: ${wrapCounter}`);
}

/* -------------------------------------------------------------------------- */
/*                                   EXECUTION                                 */
/* -------------------------------------------------------------------------- */

console.time("Performance");
main();
console.timeEnd("Performance");
