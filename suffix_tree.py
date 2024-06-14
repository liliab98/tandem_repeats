class Node:
    def __init__(self, sub=""):
        self.sub = sub
        self.children = []
        self.parent = None
        self.start = None  # depth of the leaf
        self.end = None
        self.D = 0
        self.mark = False
        self.DFS = (float("+inf"), float("-inf"))


class SuffixTree:
    def __init__(self, text):
        self.root = Node("root")
        if len(text) <= 1:
            raise ValueError("Text must be longer than 1 character")
        if text[-1] != "$":
            text += "$"
        self.text = text
        self.DFS = [0] * len(text)
        self.build_tree()
        self.traverse()

    def internal_node(self, node, new_leaf, suf):
        # if the suffix is bigger the the current node
        if len(node.sub) < len(suf) and node.sub == suf[: len(node.sub)]:
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
                    # new parent node
                    internal = Node(node.sub[:i])
                    internal.parent = node.parent  # grandparent
                    internal.parent.children.remove(node)
                    internal.parent.children.append(internal)
                    internal.start = (
                        internal.parent.end if internal.parent.end is not None else 0
                    )
                    internal.end = (len(new_leaf.sub) - len(suf)) + i
                    internal.D = internal.parent.D + internal.end - internal.start
                    # restructure old children node
                    node.parent = internal
                    node.sub = node.sub[i:]
                    # add new node as child
                    new_leaf.parent = internal
                    new_leaf.sub = suf[i:]
                    internal.children.append(node)
                    internal.children.append(new_leaf)
                    return
        # When the suffix is a child of the current node
        node.children.append(new_leaf)
        new_leaf.parent = node
        new_leaf.sub = suf[len(node.sub) :]
        return

    def addSuffix(self, suf):
        new_leaf = Node(suf)
        new_leaf.start = len(self.text) - len(suf)
        new_leaf.end = len(self.text) - 1
        new_leaf.D = len(suf)
        # if the suffix is already (partly) in the tree
        for child in self.root.children:
            if child.sub[0] == suf[0]:
                # print("Node not to root:", suf)
                self.internal_node(child, new_leaf, suf)
                return
        # if the suffix is not found in the tree
        new_leaf.parent = self.root
        self.root.children.append(new_leaf)
        return

    def build_tree(self):
        for i in range(len(self.text)):
            self.addSuffix(self.text[i:])

    def post_order(self, node):
        for child in node.children:
            self.post_order(child)
        if node.children == []:
            dfs = max(self.DFS) + 1
            self.DFS[node.start] = dfs
            node.DFS = (dfs, dfs)
        if node.parent is not None:
            (a, b) = node.parent.DFS
            (c, d) = node.DFS
            if c < a:
                node.parent.DFS = (c, b)
            (a, b) = node.parent.DFS
            (c, d) = node.DFS
            if d > b:
                node.parent.DFS = (a, d)

    def traverse(self):
        self.post_order(self.root)

    def print_tree(self):
        self.print_node(self.root)

    def print_node(self, node):
        if node.children == []:
            print(
                "Leave:",
                node.sub,
                "DFS:",
                node.DFS,
                "Depth: ",
                node.D,
                "Start: ",
                node.start,
                "End: ",
                node.end,
            )
        else:
            print(
                "Internal:",
                node.sub,
                "DFS:",
                node.DFS,
                "Depth: ",
                node.D,
                "Start: ",
                node.start,
                "End: ",
                node.end,
            )
        for child in node.children:
            self.print_node(child)


def get_leaf_list(node, leaf_list, excluded=None):
    if excluded is None or node != excluded:
        if node.children == []:
            leaf_list.append(node.start + 1)
        else:
            for child in node.children:
                get_leaf_list(child, leaf_list, excluded)


def LeafList(node, excluded=None):
    leaf_list = []
    get_leaf_list(node, leaf_list, excluded)
    return leaf_list
