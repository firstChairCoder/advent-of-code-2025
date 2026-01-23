package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// Global lock configuration
// lockCurrentState tracjs the dial's needle. Initialized to 50 as per requirements
// lockWrap defines the boundary of our circular dial (0-99)
var lockCurrentState = 50

const lockWrap = 100

/**
 * leftTurn calculates the new index when rotatinng counter-clockwise
 * In Go, the % operator can return a negative remainder (e.g: -10 % 100 = -10)
 * We use the formula ((a % n) + n) % n to ensure a positive circular index
 */
func leftTurn(n int) int {
	return ((lockCurrentState-n)%lockWrap + lockWrap) % lockWrap
}

/**
 * rightTurn calculats the new index when rotating clockwise
 * Since we are only adding positive integers, a standard modulo is sufficient
 */
func rightTurn(n int) int {
	return (lockCurrentState + n) % lockWrap
}

/**
 * wraps calculates how many times the movement crosses the '0' boundary
 * It uses O(1) Arithmetic Projection, treating the dial as an infinite number line
 * divided into "buckets" of 100.
 */
func wraps(value, delta int) int {
	// tmp represents the "projected destination" without wrapping yet
	tmp := value + delta
	var clicks int

	if delta > 0 {
		// Clockwise: We compare the 'bucket index' of the start and end points
		// Example: Start at 90, Move 20 -> tmp = 110
		// (110 / 100) - (90 / 100) => 1 - 0 = 1 wrap.
		clicks = tmp/lockWrap - value/lockWrap
	} else {
		// Counter-Clockwise: We use a -1 offset to correctly handle boundary cases
		// where the needle lands exactly on 0
		clicks = (value-1)/lockWrap - (tmp-1)/lockWrap
	}
	// Ensure the result is an absolute count of crossings.
	if clicks < 0 {
		clicks = -clicks
	}
	return clicks
}

// -- Main Execution Logic --
func main() {
	// Open the input file. 'os.Open' is more memory-efficient than reading the whole file at one.
	file, err := os.Open("input-2025.txt")
	if err != nil {
		fmt.Println("Error: 'input-2025.txt' not found.")
		return
	}
	// Ensuree the file is closed once the function finishes.
	defer file.Close()

	zeroCounter := 0 // Tracks Part 1 (Landing exactly on 0)
	wrapCounter := 0 // Tracks Part 2 (Total boundary crossings)

	// bufio.Scanner reads the file line-by-line to minimize memory footprint
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// Clean the line of any leading / trailing whitespace.
		line := strings.TrimSpace(scanner.Text())
		if len(line) < 2 {
			continue // Skip empty or malformed lines
		}

		// Extract direction (first character) and distance (rest of the string).
		direction := strings.ToUpper(string(line[0]))
		n, err := strconv.Atoi(line[1:])
		if err != nil {
			fmt.Printf("Skipping malformed line: %s (non-integer rotation)\n", line)
			continue
		}

		// Part 2 Logic: Calculate boundary crossings
		// We convert the direction into a signed integer 'delta'
		var delta int
		if direction == "R" {
			delta = n
		} else {
			delta = -n
		}
		// Calculate crossings using the current state before updating it.
		wrapCounter += wraps(lockCurrentState, delta)

		// Part 1 Logic: Update the dial position
		// We call the movement functions which apply the modular arithmetic.
		if direction == "R" {
			lockCurrentState = rightTurn(n)
		} else {
			lockCurrentState = leftTurn(n)
		}

		// If the needle lands perfectly on 0, increment Part 1 counter
		if lockCurrentState == 0 {
			zeroCounter++
		}
	}

	// Output the final computed answers for both parts of the problem.
	fmt.Printf("Part 1 Answer: %d\n", zeroCounter)
	fmt.Printf("Part 2 Answer: %d\n", wrapCounter)
}
