const fs = require("fs");

/**
 * Reads the input file and prepares two distinct data structures:
 * 1. grid_part1: A 2D array of strings ('.', '@') for Part 1.
 * 2. grid_part2: A 2D array of numbers (0 for '.', 1 for '@') for Part 2.
 */
const prepareInput = () => {
  const data = fs
    .readFileSync("input-04-2025.txt", { encoding: "utf-8" })
    .split("\n")
    .filter((row) => row.length > 0);

  const grid_part1 = data.map((row) => row.split(""));

  // For part 2, we convert '.' to 0 and any other character (like '@') to 1
  const grid_part2 = data.map((row) =>
    row.split("").map((cell) => (cell === "." ? 0 : 1))
  );

  return { grid_part1, grid_part2 };
};

// Global variables to hold the two input states
const { grid_part1, grid_part2 } = prepareInput();

/**
 * Shared logic to calculate the count of "active" neighbors for a cell (x, y).
 * @param {Array<Array<any>>} grid The grid to check against.
 * @param {number} y The row index.
 * @param {number} x The column index.
 * @param {string|number} activeMarker The value representing an active cell.
 * @param {number} [iteration=1] The current iteration (only used for part 2's logic).
 * @returns {number} The count of active neighbors.
 */
const getNeighborCount = (grid, y, x, activeMarker, iteration = 1) => {
  let neighbor = 0;
  const max_y = grid.length;
  const max_x = grid[0].length;

  for (let y_off = -1; y_off <= 1; y_off++) {
    for (let x_off = -1; x_off <= 1; x_off++) {
      // Skip the cell itself
      if (x_off === 0 && y_off === 0) {
        continue;
      }

      const next_x = x + x_off;
      const next_y = y + y_off;

      // Check bounds
      if (next_x < 0 || next_x >= max_x || next_y < 0 || next_y >= max_y) {
        continue;
      }

      // Check for active status (Code A uses direct comparison, Code B uses >= iteration)
      if (typeof activeMarker === "string") {
        // Logic for Part 1 (Code A)
        if (grid[next_y][next_x] === activeMarker) {
          neighbor++;
        }
      } else {
        // Logic for Part 2 (Code B)
        if (grid[next_y][next_x] >= iteration) {
          neighbor++;
        }
      }
    }
  }
  return neighbor;
};

/**
 * Implements the logic from Code A (Part 1).
 * Calculates the score based on the initial grid state.
 */
const part1 = () => {
  let score = 0;
  const grid = grid_part1;
  const activeMarker = "@";

  for (let y = 0; y < grid.length; y++) {
    const row = grid[y];
    for (let x = 0; x < row.length; x++) {
      if (row[x] !== activeMarker) {
        continue;
      }

      const neighborCount = getNeighborCount(grid, y, x, activeMarker);

      if (neighborCount < 4) {
        score++;
      }
    }
  }
  console.log(`Part 1 Result: ${score}`);
};

/**
 * Implements the logic from Code B (Part 2).
 * Simulates the iterative removal process.
 * @param {Array<Array<number>>} file_grid The numeric grid state (modified in place).
 * @returns {number} The total accumulated score.
 */
const part2 = (file_grid) => {
  // This function is the inner loop of Code B (renamed for clarity)
  const removeIteration = (iteration) => {
    let removed_count = 0;

    // Note: The original code used 'for...in' which iterates over keys (strings),
    // it is replaced here with standard numeric loops for performance and clarity.
    for (let y = 0; y < file_grid.length; y++) {
      const row = file_grid[y];
      for (let x = 0; x < row.length; x++) {
        // Skip cells that were already removed (value < current iteration)
        if (row[x] < iteration) {
          continue;
        }

        // Use a placeholder value for activeMarker (it's ignored for Part 2 logic)
        const neighborCount = getNeighborCount(file_grid, y, x, 1, iteration);

        if (neighborCount < 4) {
          // Marked for removal (removed_count increases)
          removed_count++;
          // The cell is marked as removed by being kept at its current value (iteration)
        } else {
          // The cell survives this round; it is marked for the *next* round
          // by incrementing its value (iteration + 1)
          file_grid[y][x] = iteration + 1;
        }
      }
    }
    return removed_count;
  };

  let total_score = 0;
  let iteration = 1;
  let removed_count = -1; // Initialize to enter the loop

  while (removed_count !== 0) {
    removed_count = removeIteration(iteration);
    total_score += removed_count;
    iteration++;
  }

  console.log(`Part 2 Result: ${total_score}`);
  return total_score;
};

// --- Execution ---
part1();
// Call part2, passing a deep copy of the grid_part2 data so part1's execution
// doesn't affect it, and part2 can safely modify it in place.
part2(grid_part2.map((row) => [...row]));
