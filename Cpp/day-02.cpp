#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdint>
#include <chrono>
#include <sstream>

/**
 * --- PATTERN CHECKING (PART 2) ---
 * Mimics Python's /^(\d+)\1+$/
 * Logic: Checks if the string can be divided into 'n' identical blocks.
 */
bool is_repeated(const std::string &s)
{
	size_t total_len = s.length();
	if (total_len < 2)
		return false;

	// A pattern must have a length that is a divisor of the total string length
	for (size_t block_len = 1; block_len <= total_len / 2; ++block_len)
	{
		if (total_len % block_len == 0)
		{
			std::string block = s.substr(0, block_len);
			bool all_match = true;
			// Check every subsequent block of the same length
			for (size_t offset = block_len; offset < total_len; offset += block_len)
			{
				if (s.substr(offset, block_len) != block)
				{
					all_match = false;
					break;
				}
			}
			if (all_match)
				return true;
		}
	}
	return false;
}

/**
 * --- PATTERN CHECKING (PART 1) ---
 * Mimics Python's /^(\d+)\1$/
 * Logic: Compares the first half of the string directly with the second half.
 */
bool is_double(const std::string &s)
{
	size_t n = s.length();
	if (n == 0 || n % 2 != 0)
		return false;
	return s.substr(0, n / 2) == s.substr(n / 2);
}

int main()
{
	// 1. Start Benchmark Timer
	auto start_time = std::chrono::high_resolution_clock::now();

	// 2. Open File
	std::ifstream infile("inputs/input-02-2025.txt");
	if (!infile)
	{
		std::cerr << "Error: Could not open inputs/input-02-2025.txt\n";
		return 1;
	}

	uint64_t sum_part1 = 0;
	uint64_t sum_part2 = 0;

	// Read the entire file into a string to handle the comma-separated format
	std::stringstream buffer;
	buffer << infile.rdbuf();
	std::string content = buffer.str();

	// 3. COMMA PARSING
	// We use a stringstream to split the content by commas
	std::stringstream ss(content);
	std::string range_block;

	while (std::getline(ss, range_block, ','))
	{
		if (range_block.empty())
			continue;

		// 4. DASH PARSING
		// Now we split the "start-end" block
		size_t dash_pos = range_block.find('-');
		if (dash_pos == std::string::npos)
			continue;

		std::string left_raw = range_block.substr(0, dash_pos);
		std::string right_raw = range_block.substr(dash_pos + 1);

		// Convert to numbers for the loop
		long long start_val = std::stoll(left_raw);
		long long end_val = std::stoll(right_raw);

		/** * 5. LEADING ZERO HANDLING
		 * We must preserve the visual width of the 'left' side of the range.
		 * Example: "001-010" -> width is 3.
		 */
		size_t width = left_raw.length();

		// 6. RANGE LOOP
		for (long long i = start_val; i <= end_val; ++i)
		{
			// Convert number to string and pad with zeros to match width
			std::string s = std::to_string(i);
			if (s.length() < width)
			{
				s.insert(0, width - s.length(), '0');
			}

			if (is_double(s))
			{
				sum_part1 += i;
			}

			if (is_repeated(s))
			{
				sum_part2 += i;
			}
		}
	}

	// 7. Output Results
	std::cout << "Part 1: " << sum_part1 << "\n";
	std::cout << "Part 2: " << sum_part2 << "\n";

	// 8. Performance Log
	auto end_time = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end_time - start_time;
	std::cout << "--------------------------\n";
	std::cout << "Time taken: " << elapsed.count() << " seconds\n";

	return 0;
}
