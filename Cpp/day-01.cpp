#include <iostream>
#include <fstream>
#include <string>
#include <cmath>  // For std::abs
#include <cctype> // For std::toupper

/**
 * --- Global Configuration ---
 * lockCurrentState: Represents the current "needle" position on the dial.
 * lockWrap: The modulus (100), defining the dial range from 0 to 99.
 */
int lockCurrentState = 50;
const int lockWrap = 100;

/**
 * --- Movement Functions (Part 1 Logic) ---
 * * leftTurn: Moves the dial counter-clockwise.
 * In C++, the % operator can return a negative remainder.
 * We use ((val % n) + n) % n to ensure the result stays in the [0, 99] range.
 */
int leftTurn(int n)
{
	return ((lockCurrentState - n) % lockWrap + lockWrap) % lockWrap;
}

/**
 * rightTurn: Moves the dial clockwise.
 * Since we are only adding positive integers here, a simple % is safe.
 */
int rightTurn(int n)
{
	return (lockCurrentState + n) % lockWrap;
}

/**
 * Calculates the 'floor' of a division (a / b), rounding toward negative infinity.
 * * In C++, the default behavior for negative numbers is truncation:
 * -5 / 2 = -2  (Truncation: drops the 0.5)
 * Python's floorDiv(-5, 2) = -3 (Floor: rounds down to the next integer)
 * * This function is essential for the Arithmetic Projection logic to work
 * correctly when the lock dial moves into "negative" territory.
 */
int floorDiv(int a, int b)
{
	// Perform standard C++ integer division (truncation)
	int q = a / b;

	// Calculate the remainder
	int r = a % b;

	/**
	 * Logic for rounding down:
	 * If there is a remainder (r != 0), we check if the signs of the remainder
	 * and the divisor (b) differ.
	 * * In our Lock problem, 'b' (lockWrap) is always 100 (positive).
	 * Therefore, if 'a' is negative and not a perfect multiple of 100,
	 * 'r' will be negative. Since 'r' (negative) != 'b' (positive),
	 * we must decrement 'q' to effectively "round down" to the more
	 * negative integer.
	 */
	if (r != 0 && ((r > 0) != (b > 0)))
	{
		q--;
	}

	return q;
}

/**
 * --- Wrap Counting Function (Part 2 Logic) ---
 * * This uses O(1) Arithmetic Projection. Instead of counting steps, we
 * calculate how many "full cycles" exist between the start and the
 * projected endpoint.
 */
int wraps(int value, int delta)
{
	// tmp is the 'theoretical' position if the dial didn't wrap around.
	int tmp = value + delta;
	int clicks = 0;

	if (delta > 0)
	{
		/**
		 * Clockwise (Right):
		 * Example: Start at 90, move 20. tmp = 110.
		 * 110/100 (1) - 90/100 (0) = 1 wrap.
		 */
		clicks = floorDiv(tmp, lockWrap) - floorDiv(value, lockWrap);
	}
	else
	{
		/**
		 * Counter-Clockwise (Left):
		 * We apply a -1 offset to 'value' and 'tmp' to handle the 0 boundary
		 * correctly, mimicking the floor division behavior seen in the Python version.
		 */
		clicks = floorDiv(value - 1, lockWrap) - floorDiv(tmp - 1, lockWrap);
	}

	// std::abs ensures the return is a positive count of boundary crossings.
	return std::abs(clicks);
}

int main()
{
	/**
	 * File I/O:
	 * std::ifstream is used for memory-efficient line-by-line streaming.
	 */
	std::ifstream infile("../inputs/input-2025.txt");
	if (!infile)
	{
		std::cerr << "Error: 'input-2025.txt' not found.\n";
		return 1;
	}

	int zeroCounter = 0; // Stores Part 1 result
	int wrapCounter = 0; // Stores Part 2 result
	std::string line;

	/**
	 * Main Processing Loop:
	 * We read each instruction (e.g., "R150") one by one.
	 */
	while (std::getline(infile, line))
	{
		// Skip empty lines or lines too short to contain a direction + number.
		if (line.length() < 2)
			continue;

		// Parse direction ('R' or 'L') and convert to uppercase for consistency.
		char direction = static_cast<char>(std::toupper(line[0]));
		int n;

		try
		{
			// stoi extracts the integer from the substring starting at index 1.
			n = std::stoi(line.substr(1));
		}
		catch (...)
		{
			std::cerr << "Skipping malformed line: " << line << "\n";
			continue;
		}

		/**
		 * --- Logic for Part 2 ---
		 * 'delta' is the signed distance (e.g., L50 becomes -50).
		 * We calculate wraps based on the CURRENT state before we move.
		 */
		int delta = (direction == 'R') ? n : -n;
		wrapCounter += wraps(lockCurrentState, delta);

		/**
		 * --- Logic for Part 1 ---
		 * Update the global state based on the direction.
		 */
		if (direction == 'R')
		{
			lockCurrentState = rightTurn(n);
		}
		else
		{
			lockCurrentState = leftTurn(n);
		}

		// If the needle lands exactly on 0, it's a "hit" for Part 1.
		if (lockCurrentState == 0)
		{
			zeroCounter++;
		}
	}

	// Output the final results to the console.
	std::cout << "Part 1 Answer: " << zeroCounter << "\n";
	std::cout << "Part 2 Answer: " << wrapCounter << "\n";

	return 0;
}
