import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np
from suffix_tree import SuffixTree
from find_tandem_repeats import naive, unmark_nodes, basic, extended


def generate_random_string(length, alphabet=string.ascii_uppercase):
    return "".join(random.choice(alphabet) for _ in range(length))


def plot():
    alphabet = "ACGT"
    lengths = list(range(50, 801, 50))

    naive_times = []
    build_times = []
    basic_times = []
    extended_times = []

    ta_naive = []
    ta_basic = []
    ta_extended = []

    for length in lengths:
        random_string = generate_random_string(length, alphabet)

        start_time_naive = time.time()
        ta_naive = naive(random_string)
        end_time_naive = time.time()
        tandem_repeat_naive_time = end_time_naive - start_time_naive
        naive_times.append(tandem_repeat_naive_time)

        start_time_build = time.time()
        tree = SuffixTree(random_string)
        end_time_build = time.time()
        build_time = end_time_build - start_time_build
        build_times.append(build_time)

        start_time_extended = time.time()
        ta_extended = extended(tree)
        end_time_extended = time.time()
        tandem_repeat_extended_time = end_time_extended - start_time_extended
        extended_times.append(tandem_repeat_extended_time)

        unmark_nodes(tree.root)

        start_time_basic = time.time()
        ta_basic = basic(tree)
        end_time_basic = time.time()
        tandem_repeat_basic_time = end_time_basic - start_time_basic
        basic_times.append(tandem_repeat_basic_time)

    # Calculating theoretical runtimes
    theoretical_cubic_times = [length**3 for length in lengths]
    theoretical_basic_times = [length**2 for length in lengths]
    theoretical_extended_times = [length * np.log2(length) for length in lengths]

    # Plotting the runtimes on a logarithmic scale
    plt.figure(figsize=(12, 8))

    plt.plot(lengths, naive_times, label="Naive Algorithm", marker="v")
    plt.plot(lengths, build_times, label="Build Time", marker="D")
    # plt.plot(lengths, basic_times, label='Basic Algorithm') #, marker='o')
    # plt.plot(lengths, extended_times, label='Extended Algorithm') #, marker='s')

    plt.plot(lengths, theoretical_cubic_times, label="Cubic Time (n^3)", linestyle="--")
    plt.plot(
        lengths, theoretical_basic_times, label="Quadratic Time (n^2)", linestyle="--"
    )
    # plt.plot(lengths, theoretical_extended_times,
    # label='Log-Linear Time (n log n)', linestyle='--')

    plt.yscale("log")  # Set the y-axis to a logarithmic scale

    plt.xlabel("Input Size")
    plt.ylabel("Time (log scale)")
    plt.title(
        "Runtimes of Basic and Extended Algorithms"
        + "on Log Scale compared to Theoretical Runtimes"
    )
    plt.legend()
    plt.grid(True, which="both", ls="--")

    plt.show()
