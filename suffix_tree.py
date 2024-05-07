class Node:
    def __init__(self, sub=""):
        self.sub = sub
        self.children = []
        self.parent = None
        self.start = None  # depth of the leaf
        self.end = None
        self.leaf_list = []


class SuffixTree:
    def __init__(self, text):
        self.root = Node("root")
        if text[-1] != "$":
            text += "$"
        self.text = text
        self.build_tree()
        self.fill_leaf_list(self.root)

    def build_tree(self):
        for i in range(len(self.text)):
            self.addSuffix(self.text[i:])

    def addSuffix(self, suf):
        # if the suffix is already (partly) in the tree
        for child in self.root.children:
            if child.sub[0] == suf[0]:
                self.internal_node(child, suf)
                return
        # if the suffix is not found in the tree
        new_leaf = Node(suf)
        new_leaf.parent = self.root
        new_leaf.start = len(self.text) - len(suf)
        new_leaf.end = len(self.text)
        self.root.children.append(new_leaf)
        return

    def internal_node(self, node, suf):
        if node.end - node.start < len(suf):
            for child in node.children:
                if child.sub[0] == suf[0]:
                    self.internal_node(child, suf)
                    return
        for i in range(len(suf)):
            if node.sub[i] != suf[i]:
                # old parent
                grandparent = node.parent
                # new parent node
                internal = Node(suf[:i])
                internal.parent = grandparent
                internal.parent.children.remove(node)
                internal.parent.children.append(internal)
                internal.start = node.start
                internal.end = node.start + i
                # restructure old children node
                node.parent = internal
                node.sub = node.sub[i:]
                # add new node as child
                new_leaf = Node(suf[i:])
                new_leaf.parent = internal
                new_leaf.start = len(self.text) - len(suf)
                new_leaf.end = len(self.text)
                internal.children.append(node)
                internal.children.append(new_leaf)
                return

    def fill_leaf_list(self, node):
        if node.children == []:
            return [node.start + 1]
        for child in node.children:
            node.leaf_list += self.fill_leaf_list(child)
            node.leaf_list.sort()
        return node.leaf_list

    def print_tree(self, ascii=False):
        if ascii:
            self.print_node_ascii(self.root)
        else:
            self.print_node(self.root)

    def print_node(self, node):
        if node.children == []:
            print("Leave:", self.text[node.start : node.end], "Leaves:", node.leaf_list)
        else:
            print("Internal:", node.sub, "Leaves:", node.leaf_list)
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


text = "ABAABAABBBA$"  # "banana$"
tree = SuffixTree(text)
# tree.build_tree()
tree.print_tree()
