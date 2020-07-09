import pathlib

from dollo_tree import TreeNode
import _delete as dl
import numpy as np

def loads(s):
    """
    Load a list of trees from a Newick formatted string.

    :param s: Newick formatted string.
    :param strip_comments: Flag signaling whether to strip comments enclosed in square \
    brackets.
    :param kw: Keyword arguments are passed through to `Node.create`.
    :return: List of Node objects.
    """
    return [parse_node(ss.strip()) for ss in s.split(';') if ss.strip()]


def dumps(trees):
    """
    Serialize a list of trees in Newick format.
    :param trees: List of TreeNode objects or a single Node object.
    :return: Newick formatted string.
    """
    if isinstance(trees, TreeNode):
        trees = [trees]
    return ';\n'.join([tree.newick for tree in trees]) + ';'


def load(fp):
    """
    Load a list of trees from an open Newick formatted file.

    :param fp: open file handle.
    :return: List of Node objects.
    """
    return loads(fp.read())


def read(fname, encoding='utf8'):
    """
    Load a list of trees from a Newick formatted file.
    :param fname: file path.
    :return: List of Node objects.
    """
    with pathlib.Path(fname).open(encoding=encoding) as fp:
        return load(fp)


def _parse_name_and_length(s):
    length = None
    if ':' in s:
        s, length = s.split(':', 1)
    return s or None, length or None

def _parse_siblings(s):
    """
    http://stackoverflow.com/a/26809037
    """
    bracket_level = 0
    current = []

    # trick to remove special-case of trailing chars
    for c in (s + ","):
        if c == "," and bracket_level == 0:
            yield parse_node("".join(current))
            current = []
        else:
            if c == "(":
                bracket_level += 1
            elif c == ")":
                bracket_level -= 1
            current.append(c)


def parse_node(s):
    """
    Parse a Newick formatted string into a `TreeNode` object.
    :param s: Newick formatted string to parse.
    :param strip_comments: Flag signaling whether to strip comments enclosed in square \
    brackets.
    :return: `TreeNode` instance.
    """
    print(s)
    s = s.strip()
    parts = s.split(')')
    if len(parts) == 1:
        descendants, label = [], s
    else:
        if not parts[0].startswith('('):
            raise ValueError('unmatched braces %s' % parts[0][:100])
        descendants = list(_parse_siblings(')'.join(parts[:-1])[1:]))
        label = parts[-1]
    name, length = _parse_name_and_length(label)
    new_tree = TreeNode(name=name, label=length)
    new_tree.children = descendants
    #print("new_tree", new_tree.name)
    return new_tree


def main():
    fname = "OV2295-cn-tree.newick"
    tree_gw = "(a:1,(d:2,b:3,c:4))"
    #tree = read(fname)[0]
    tree1 = loads(tree_gw)[0]
    tree2 = loads(tree_gw)[0]
    print(tree1.print_attr_map("name"))
    print(tree1.is_leaf)
    #print(0 + np.inf)
    leaf_cns = {"a":[1,2], "b":[2,4], "c":[3,6], "d":[4,8]}
    leaf_cns1 = {"a": 2, "b":4, "c": 6, "d": 8}
    dl.calc_score_recursive(tree1, leaf_cns1, 1, 8)
    print(tree1.cn_score)
    dl.calc_score_recursive_vect(tree2, leaf_cns, 1, 8, 2)
    print(tree2.cn_score)

    '''
    for node in tree1.nodes:
        print(node.name)
        print(node.cn_score)
    '''


main()