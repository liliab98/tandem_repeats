import random
import string
from suffix_tree import SuffixTree
from find_tandem_repeats import naive, unmark_nodes, left_rotate
from find_tandem_repeats import basic, extended


# Unit tests with known results
def unit_test(text=None):
    texts = [
        "banana",
        "Mississippi",
        "ABAABAABBBA",
        "aaaaa",
        "TCAGTCTTAA",
        "GTTAGGCGGCTGGCACGGGG",
        "GTCCAAACATC",
        "TATCGTGACG",
    ]

    if text is not None:
        texts = [text]

    for text in texts:
        print("Text: ", text)
        tree = SuffixTree(text)
        print("Naive: ", naive(text))
        ta_basic = basic(tree)
        print("Basic: ", ta_basic)
        print("Basic all: ", left_rotate(tree, ta_basic))
        unmark_nodes(tree.root)
        ta_extended = extended(tree)
        print("Extended: ", ta_extended)
        print("Extended all: ", left_rotate(tree, ta_extended))
        print("")


def generate_random_string(length, alphabet=string.ascii_uppercase):
    return "".join(random.choice(alphabet) for _ in range(length))


# Randomized testing
def random_test():
    alphabet = "ACGT"
    lengths = [
        10,
        20,
        100,
        500,
    ]

    texts = []
    for i in range(10):
        for length in lengths:
            text = generate_random_string(length, alphabet)
            texts.append(text)

    basic_ev, extended_ev = True, True

    for text in texts:
        ta_naive = naive(text)
        tree = SuffixTree(text)
        ta_basic = basic(tree)
        ta_basic_all = left_rotate(tree, ta_basic)
        unmark_nodes(tree.root)
        ta_extended = extended(tree)
        ta_extended_all = left_rotate(tree, ta_extended)
        if ta_naive == [] or ta_basic == [] or ta_extended == []:
            print("Empty:", ta_naive, ta_basic, ta_extended, "at: ", text)
            break
        for elem in ta_basic:
            if elem not in ta_naive:
                basic_ev = False
                print("Basic failed for Wort:", text, "\nWith wrong ta:", elem)
        for elem in ta_extended:
            if elem not in ta_naive:
                extended_ev = False
                print("Extended failed for Wort:")
                print(text, "\nWith wrong ta:", elem)
        for elem in ta_naive:
            if elem not in ta_basic_all:
                basic_ev = False
                print("Basic all failed for Wort:", text)
                print("With wrong ta:", elem)
            if elem not in ta_extended_all:
                extended_ev = False
                print("Extended all failed for Wort:", text)
                print("With wrong ta:", elem)

    if basic_ev:
        print("Basic works for all test cases")
    if extended_ev:
        print("Extended works for all test cases")
