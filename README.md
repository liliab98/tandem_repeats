# Tandem repeats

## Project Overview

This project implements Stoye and Gusfield's algorithm to find tandem repeats in strings. It features two primary approaches:

- Naive Suffix Tree Implementation with Time Complexity O(n^2)
- Basic Algorithm with Time Complexity O(n^2 + z) 
- Extended Algorithm with Time Complexity O(n log n + z)

where 'n' is the length of the input string, and 'z' is the output size.

To verify the results and for runtime analysis, a naive approach to find tandem repeats with O(n^3) time complexity is also implemented.

## Repository Structure

- suffix_tree.py: Contains the implementation of - the suffix tree and its associated methods.
- testing.py: Includes unit tests with known results and randomized testing.
- main.py: The main script to run the unit tests and randomized testing.
- runtime_analysis.py: Performs runtime analysis and generates plots for the algorithms.
- find_tandem_repeats.py: Implements the algorithms to find tandem repeats.

## Getting Started

Prerequisites
- Python 3.x
- Required packages: matplotlib, numpy

