from testing import unit_test, random_test
from runtime_analysis import plot


def main():
    # Unit tests with known results
    unit_test()
    # Randomized testing
    random_test()

    # Runtime analysis
    # plot()


if __name__ == "__main__":
    main()
