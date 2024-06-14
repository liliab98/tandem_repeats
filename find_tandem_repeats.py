from suffix_tree import Node, LeafList


def naive(s: str) -> list:
    tandem_repeats = []
    n = len(s)

    for i in range(n):
        for l in range(1, n - i + 1):
            if (i + 2 * l) > n:
                break
            if s[i : i + l] == s[i + l : i + 2 * l]:
                tandem_repeats.append((i + 1, l))

    return tandem_repeats


def unmark_nodes(node):
    """
    This function unmarks all the nodes in the suffix tree.
    """
    if node.children == []:
        node.mark = False
    else:
        for child in node.children:
            child.mark = False
            unmark_nodes(child)


def left_rotate(tree, branching_tandem_repeats: list) -> list:
    """
    This function left rotates the tandem repeats in the list.
    """
    tandem_repeats = []
    for ta in branching_tandem_repeats:
        begin, length = ta
        step = 2
        while (
            begin - step >= 0
            and tree.text[begin - step] == tree.text[begin + length - step]
        ):
            tandem_repeats.append((begin - step + 1, length))
            step += 1
    return branching_tandem_repeats + tandem_repeats


def traverse_basic(DFS, string, node, tandem_repeats):
    # Select an unmarked internal node v
    if node.children != [] and not node.mark and node.sub != "root":
        # 2a. Collect the leaf-list LL(v) of node v
        leaf_list = LeafList(node)
        for i in leaf_list:
            j = i + node.D
            # Test 1: if L(v)^2 is a tandem repeat
            (a, b) = node.DFS
            # To determine if a leaf j = i + D(v) is in LL(v)
            # just check if DFS[j] is between the two dfs numbers recorded at v.
            if DFS[j - 1] >= a and DFS[j - 1] <= b:
                # if j in leaf_list:
                # Test 2: if its branching
                if string[i - 1] != string[(i + 2 * node.D) - 1]:
                    tandem_repeats.append((i, node.D))
    # mark v and execute steps 2a and 2b for node v
    node.mark = True
    for child in node.children:
        traverse_basic(DFS, string, child, tandem_repeats)


def basic(tree):
    """
    This function finds all branching tandem repeats in a suffix tree.

    1. Select an unmarked node v. Mark v and execute steps 2a and 2b for node v.
    2a. Collect the leaf-list LL(v) of node v.
    2b. For each leaf i in LL(v) test whether
        - the leaf j = i + D(v) is in LL(v).
        - If yes, test whether S[i] /= S[i+2D(v)].
        If and only if both tests return true,
        there is a branching tandem repeat of length 2D(v)
        and depth D(v) starting at position i.

    Input:
    - tree: a suffix tree

    Output:
    - branching_tandem_repeats: a list of branching tandem repeats,
    where each tandem repeat is denoted by a tuple (i, a) where i is the
    starting position and a is the length of the tandem repeat.
    """
    branching_tandem_repeats = []
    traverse_basic(tree.DFS, tree.text, tree.root, branching_tandem_repeats)

    return branching_tandem_repeats


def traverse_extended(DFS, string, node, tandem_repeats):
    # 1. Select an unmarked internal node v
    if node.children != [] and not node.mark and node.sub != "root":
        # 2a. Collect the leaf-list LL'(v) of node v
        node_with_largest_LL = Node()
        for child in node.children:
            if (
                child.DFS[1] - child.DFS[0]
                > node_with_largest_LL.DFS[1] - node_with_largest_LL.DFS[0]
            ):
                node_with_largest_LL = child
        node_leaf_list = LeafList(node, node_with_largest_LL)
        (a, b) = node.DFS
        (c, d) = node_with_largest_LL.DFS
        for i in node_leaf_list:
            # 2b. For each leaf i in LL'(v) test wether
            j = i + node.D
            # Test 1: if it's a tandem repeat
            # To determine if a leaf j = i + D(v) is in LL(v)
            # just check if DFS[j] is between the two dfs numbers recorded at v.
            if DFS[j - 1] >= a and DFS[j - 1] <= b:
                # if j in node_leaf_list:
                # Test 2: if its branching
                if string[i - 1] != string[(i + 2 * node.D) - 1]:
                    tandem_repeats.append((i, node.D))
            # 2c. For each leaf k in LL'(v) test wether
            k = i - node.D
            # Test 1: if it's a tandem repeat
            if DFS[k - 1] >= c and DFS[k - 1] <= d:
                # if k in biggest_leaf_list: #node_leaf_list
                # Test 2: if its branching
                if string[k - 1] != string[(k + 2 * node.D) - 1]:
                    tandem_repeats.append((k, node.D))
    # mark v and execute steps 2a and 2b for node v
    node.mark = True
    for child in node.children:
        traverse_extended(DFS, string, child, tandem_repeats)


def extended(tree):
    """
    This function finds all branching tandem repeats in a suffix tree.

    1. Select an unmarked internal node v.
       Mark v and execute steps 2a and 2b and 2c for node v.
    2a. Collect the leaf-list LL'(v) for node v.
    2b. For each leaf i in LL'(v) test wether
        - the leaf j = i + D(v) is in LL'(v).
        - If yes, test wether S[i] /= S[i+2D(v)].
        If and only if both tests return true,
        there is a branching tandem repeat of length 2D(v)
        and depth D(v) starting at position i.
    2c. For each leaf j in LL'(v) test wether
        - the leaf i = j - D(v) is in LL'(v).
        - If yes, test wether S[i] /= S[i+2D(v)].
        If and only if both tests return true,
        there is a branching tandem repeat of length 2D(v)
        and depth D(v) ending at position j.

    Input:
    - tree: a suffix tree

    Output:
    - branching_tandem_repeats: a list of branching tandem repeats,
    where each tandem repeat is denoted by a tuple (i, a) where i is the
    """
    branching_tandem_repeats = []
    traverse_extended(tree.DFS, tree.text, tree.root, branching_tandem_repeats)

    return branching_tandem_repeats
