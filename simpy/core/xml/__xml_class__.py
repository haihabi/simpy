class XMLTree(object):
    def __init__(self, tree):
        self.tree = tree

    def get_sub_trees(self, sub_tree_name):
        return [XMLTree(i) for i in self.tree if i.tag == sub_tree_name]

    def get_tree_attr(self):
        return self.tree.attrib

    def get_tree_attr_by_key(self, key_name):
        return self.get_tree_attr().get(key_name)
