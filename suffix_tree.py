class Node:
    def __init__(self, sub=""):
        self.sub = sub
        self.children = []
        self.parent = None
        self.start = None  # depth of the leaf
        self.end = None
        self.leaf_list = []
        self.D = 0
        self.mark = False


class SuffixTree:
    def __init__(self, text):
        self.root = Node("root")
        if text[-1] != "$":
            text += "$"
        self.text = text
        self.tandem_repeats = []
        self.build_tree()
        self.fill_leaf_list(self.root)

    def build_tree(self):
        for i in range(len(self.text)):
            self.addSuffix(self.text[i:])

    def addSuffix(self, suf):
        new_leaf = Node(suf)
        new_leaf.start = len(self.text) - len(suf)
        new_leaf.end = len(self.text) - 1
        new_leaf.D = len(suf)
        # if the suffix is already (partly) in the tree
        for child in self.root.children:
            if child.sub[0] == suf[0]:
                self.internal_node(child, new_leaf, suf)
                return
        # if the suffix is not found in the tree
        new_leaf.parent = self.root
        self.root.children.append(new_leaf)
        return

    def internal_node(self, node, new_leaf, suf):
        # if the suffix is bigger the the current node
        if len(node.sub) < len(suf):
            for child in node.children:
                # When the suffix is partly in a child
                # traverse the tree further
                if child.sub[0] == suf[len(node.sub)]:
                    self.internal_node(child, new_leaf, suf[len(node.sub) :])
                    return
        # if the suffix starts in the middle of the current node
        # and a new internal node is needed
        for i in range(len(suf)):
            if len(node.sub) > i:
                if node.sub[i] != suf[i]:
                    # old parent
                    # grandparent = node.parent
                    # new parent node
                    internal = Node(node.sub[:i])
                    internal.parent = node.parent  # grandparent
                    internal.parent.children.remove(node)
                    internal.parent.children.append(internal)
                    internal.start = (
                        internal.parent.end if internal.parent.end is not None else 0
                    )
                    internal.end = (len(new_leaf.sub) - len(suf)) + i
                    internal.D = internal.parent.D + len(internal.sub)
                    # restructure old children node
                    node.parent = internal
                    node.sub = node.sub[i:]
                    # add new node as child
                    # new_leaf = Node(suf[i:])
                    new_leaf.parent = internal
                    new_leaf.sub = suf[i:]
                    # new_leaf.start = internal.end
                    # new_leaf.end = len(self.text) -1
                    internal.children.append(node)
                    internal.children.append(new_leaf)
                    return
        # When the suffix is a child of the current node
        node.children.append(new_leaf)
        new_leaf.parent = node
        new_leaf.sub = suf[len(node.sub) :]
        return

    def fill_leaf_list(self, node):
        if node.children == []:
            node.leaf_list = [node.start + 1]
        elif node == self.root:
            node.leaf_list = []
            for child in node.children:
                self.fill_leaf_list(child)
        else:
            for child in node.children:
                node.leaf_list += self.fill_leaf_list(child)
                node.leaf_list.sort()
        return node.leaf_list

    def print_tree(self):
        self.print_node(self.root)

    def print_node(self, node):
        if node.children == []:
            print(
                "Leave:",
                node.sub,
                "Depth: ",
                node.D,
                "Leaves:",
                node.leaf_list,
                "Start: ",
                node.start,
                "End: ",
                node.end,
            )
        else:
            print(
                "Internal:",
                node.sub,
                "Depth: ",
                node.D,
                "Leaves:",
                node.leaf_list,
                "Start: ",
                node.start,
                "End: ",
                node.end,
            )
        for child in node.children:
            self.print_node(child)

    # does not work
    def print_node_ascii(self, node, line=""):
        if node.children == []:
            print("--", node.sub)  # self.text[node.start:node.end])
        print("+-", node.sub)
        for child in node.children:
            print("+-")
            self.print_node_ascii(child, line)
        line += "+--" + node.sub
        for child in node.children:
            print(line, "+--")
            self.print_node_ascii(child, line + " | ")
        print(line, "+-")
        self.print_node_ascii(node, line + "  ")


def traverse_basic(string, node, tandem_repeats):
    # Select an unmarked internal node v
    if node.children != [] and not node.mark and node != tree.root:
        # mark v and execute steps 2a and 2b for node v
        node.mark = True
        # 2a. Collect the leaf-list LL(v) of node v
        for i in node.leaf_list:
            j = i + node.D
            # Test 1: if L(v)^2 is a tandem repeat
            if j in node.leaf_list:
                # Test 2: if its branching
                if string[i - 1] != string[(i + 2 * node.D) - 1]:
                    tandem_repeats.append((i, node.D))
    for child in node.children:
        traverse_basic(string, child, tandem_repeats)


def basic(tree):
    # tandem reapeats are denoted by (i, a, 2)
    tandem_repeats = []
    branching_tandem_repeats = []
    # get all branching tandem repeats
    traverse_basic(tree.text, tree.root, branching_tandem_repeats)
    # 1. Select an unmarked node v
    #    Mark v and execute steps 2a and 2b for node v

    # 2a. Collect the leaf-list LL(v) of node v
    # 2b. For each leaf i in LL(v) test wether
    #     - the leaf j = i + D(v) is in LL(v).
    #     - If yes, test wether S[i] /= S[i+2D(v)].
    #     If and only if both tests return true,
    #     there is a branching tandem repeat of length 2D(v)
    #     and depth D(v) starting at position i.

    # Left rotate branhcing tandem repeats to get all
    for ta in branching_tandem_repeats:
        begin, length = ta
        step = 1
        while (
            tree.text[begin - step : begin - step + length]
            == tree.text[begin - step + length : begin - step + 2 * length]
        ):
            tandem_repeats.append((begin - step + 1, length))
            step += 1
    return tandem_repeats


def traverse_extended(string, node, tandem_repeats):
    # 1. Select an unmarked internal node v
    if node.children != [] and not node.mark and node != tree.root:
        # mark v and execute steps 2a and 2b for node v
        node.mark = True
        # 2a. Collect the leaf-list LL'(v) of node v
        biggest_leaf_list = []
        for child in node.children:
            if len(child.leaf_list) > len(biggest_leaf_list):
                biggest_leaf_list = child.leaf_list
        new_leaf_list = [
            item for item in node.leaf_list if item not in biggest_leaf_list
        ]
        for i in new_leaf_list:
            # 2b. For each leaf i in LL'(v) test wether
            j = i + node.D
            # Test 1: if it's a tandem repeat
            if j in node.leaf_list:
                # Test 2: if its branching
                if string[i - 1] != string[(i + 2 * node.D) - 1]:
                    tandem_repeats.append((i, node.D))
            # 2c. For each leaf k in LL'(v) test wether
            k = i - node.D
            # Test 1: if it's a tandem repeat
            if k in node.leaf_list:
                # Test 2: if its branching
                if string[k - 1] != string[(k + 2 * node.D) - 1]:
                    tandem_repeats.append((k, node.D))
    for child in node.children:
        traverse_extended(string, child, tandem_repeats)


def extended(tree):
    # tandem reapeats are denoted by (i, a, 2)
    tandem_repeats = []
    branching_tandem_repeats = []
    # get all branching tandem repeats
    traverse_extended(tree.text, tree.root, branching_tandem_repeats)
    # 1. Select an unmarked internal node v.
    # Mark v and execute steps 2a and 2b and 2c for node v.

    # 2a. Collect the leaf-list LL'(v) for node v.
    # 2b. For each leaf i in LL'(v) test wether
    #     - the leaf j = i + D(v) is in LL'(v).
    #     - If yes, test wether S[i] /= S[i+2D(v)].
    #     If and only if both tests return true,
    #     there is a branching tandem repeat of length 2D(v)
    #     and depth D(v) starting at position i.

    # 2c. For each leaf j in LL'(v) test wether
    #     - the leaf i = j - D(v) is in LL'(v).
    #     - If yes, test wether S[i] /= S[i+2D(v)].
    #     If and only if both tests return true,
    #     there is a branching tandem repeat of length 2D(v)
    #     and depth D(v) ending at position j.

    # Left rotate branhcing tandem repeats to get all
    for ta in branching_tandem_repeats:
        begin, length = ta
        step = 1
        while (
            tree.text[begin - step : begin - step + length]
            == tree.text[begin - step + length : begin - step + 2 * length]
        ):
            tandem_repeats.append((begin - step + 1, length))
            step += 1
    return tandem_repeats


text = "Mississippi"  # "ABAABAABBBA" # "banana"
tree = SuffixTree(text)
tree.print_tree()
ta1 = basic(tree)
ta = extended(tree)
for elem in ta1:
    print(elem)
for elem in ta:
    print(elem)
