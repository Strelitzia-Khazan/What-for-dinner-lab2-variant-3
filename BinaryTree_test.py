import itertools
import unittest
from hypothesis import given
from BinaryTree import BinaryTreeNode, from_list, remove, member, to_list, \
    mempty, add, to_set, get_size, intersection, concat, iterator, reduce, \
    tmap, get_parent, get_depth, copy, filter

from hypothesis import strategies as st


class TestBinaryTreeSet(unittest.TestCase):
    def test_api(self):
        empty = mempty()
        self.assertEqual(str(add(None, empty)), "{None}")
        l1 = add(None, add(1, empty))
        l2 = add(1, add(None, empty))
        self.assertEqual(str(to_set(empty)), "set()")
        self.assertTrue(str(l1) == "{None, 1}" or str(l1) == "{1, None}")
        self.assertNotEqual(empty, l1)
        self.assertNotEqual(empty, l2)
        self.assertEqual(l1, l2)
        self.assertEqual(l1, add(None, add(1, l1)))
        self.assertEqual(get_size(empty), 0)
        self.assertEqual(get_size(l1), 2)
        self.assertEqual(get_size(l2), 2)
        self.assertEqual(str(remove(l1, None)), "{1}")
        self.assertEqual(str(remove(l1, 1)), "{None}")
        self.assertFalse(member(None, empty))
        self.assertTrue(member(None, l1))
        self.assertTrue(member(1, l1))
        self.assertFalse(member(2, l1))
        self.assertEqual(intersection(l1, l2), to_set(l1))
        self.assertEqual(intersection(l1, l2), to_set(l2))
        self.assertEqual(intersection(l1, empty), empty)
        self.assertEqual(intersection(l1, add(None, empty)),
                         to_set(add(None, empty)))
        self.assertTrue(to_list(l1) == [None, 1] or to_list(l1) == [1, None])
        self.assertEqual(l1, from_list([None, 1]))
        self.assertEqual(l1, from_list([1, None, 1]))
        self.assertEqual(concat(l1, l2), from_list([None, 1, 1, None]))
        buf = []
        for e in iterator(l1):
            buf.append(e)
        self.assertIn(buf, map(list, itertools.permutations([1, None])))
        lst = to_list(l1) + to_list(l2)
        for e in iterator(l1):
            lst.remove(e)
        for e in iterator(l2):
            lst.remove(e)
        self.assertEqual(lst, [])

    def test_map(self):
        tree = from_list([1, 2, 3])
        mapped_tree = tmap(tree, lambda x: x * 2)
        self.assertEqual(to_list(mapped_tree), [2, 4, 6])

    def test_reduce(self):
        tree = from_list([1, 2, 3])
        reduced_value = reduce(tree, lambda x, y: x + y)
        self.assertEqual(reduced_value, 6)

    def setUp(self):
        # 创建一棵简单的二叉树进行测试
        self.root = BinaryTreeNode(1)
        self.root.left = BinaryTreeNode(2)
        self.root.right = BinaryTreeNode(3)
        self.root.left.left = BinaryTreeNode(4)
        self.root.left.right = BinaryTreeNode(5)

    def test_copy(self):
        copied_root = copy(self.root)
        self.assertIsNot(copied_root, self.root)
        self.assertEqual(copied_root, self.root)

    def test_add(self):
        new_root = add(6, self.root)
        self.assertTrue(new_root.right.left.value == 6)

    def test_get_parent(self):
        parent = get_parent(self.root, 5)
        self.assertEqual(parent.value, 2)

    def test_remove_root(self):
        # 创建一棵树：1 -> 2 -> 3
        root = from_list([1, 2, 3])
        new_root = remove(root, 1)
        # 断言根节点是否被正确删除
        self.assertNotIn(1, to_list(new_root))

    def test_remove_leaf(self):
        # 创建一棵树：1 -> 2 -> 3
        root = from_list([1, 2, 3])
        new_root = remove(root, 3)
        # 断言叶子节点是否被正确删除
        self.assertIsNone(new_root.right)

    def test_remove_single_child_node(self):
        root = from_list([1, 2, 3, 4])
        new_root = remove(root, 2)
        # 断言具有单个子节点的节点是否被正确删除
        self.assertFalse(member(2, new_root))

    def test_remove_node_with_two_children(self):
        root = from_list([1, 2, 3, 4, 5])
        new_root = remove(root, 2)
        print("tree:", to_list(new_root))
        # 断言具有两个子节点的节点是否被正确删除
        self.assertFalse(member(2, new_root))

    def test_get_depth(self):
        tree1 = from_list([1, 2, 3, 4, 5])
        depth1 = get_depth(tree1)
        self.assertEqual(depth1, 3)
        tree2 = mempty()
        depth2 = get_depth(tree2)
        self.assertEqual(depth2, 0)

    def test_get_size(self):
        size = get_size(self.root)
        self.assertEqual(size, 5)
        tree2 = mempty()
        size2 = get_size(tree2)
        self.assertEqual(size2, 0)

    def test_from_list_and_to_list(self):
        lst = [1, 2, 3, 4, 5]
        tree1 = from_list(lst)
        self.assertEqual(to_list(tree1), [1, 2, 4, 5, 3])
        lst2 = []
        tree2 = from_list(lst2)
        self.assertEqual(to_list(tree2), [])

    def test_intersection(self):
        tree_A = from_list([1, 2, 3, 4, 5])
        tree_B = from_list([4, 5, 6, 7, 8])
        tree_C = from_list([9])
        intersected_values_ab = intersection(tree_A, tree_B)
        self.assertEqual(intersected_values_ab, set([4, 5]))
        intersected_values_ad = intersection(tree_A, tree_C)
        self.assertEqual(intersected_values_ad, set())

    @given(st.lists(st.integers()), st.lists(st.integers()),
           st.lists(st.integers()))
    def test_concat_associativity(self, list_a, list_b, list_c):
        tree_a = from_list(list_a)
        tree_b = from_list(list_b)
        tree_c = from_list(list_c)
        tree_ab = concat(tree_a, tree_b)
        tree_ab_c = concat(tree_ab, tree_c)
        tree_bc = concat(tree_b, tree_c)
        tree_a_bc = concat(tree_a, tree_bc)
        self.assertEqual(to_list(tree_a_bc), to_list(tree_ab_c))

    @given(st.lists(st.integers()))
    def test_concat_identity(self, list_a):
        tree_a = from_list(list_a)
        tree_empty = mempty()
        tree_ea = concat(tree_empty, tree_a)
        tree_ae = concat(tree_a, tree_empty)
        list_ae = to_list(tree_ae)
        list_ea = to_list(tree_ea)
        self.assertEqual(list_ae, list_ea)

    @given(st.lists(st.integers()), st.integers())
    def test_member(self, values, target):
        tree = from_list(values)
        if target in values:
            self.assertTrue(member(target, tree))
        else:
            self.assertFalse(member(target, tree))

    def test_filter(self):
        tree = from_list([1, "a", 2, 3.5, None])
        self.assertEqual(
            filter(tree, lambda value: isinstance(value, int)),
            set([1, 2])
        )
        self.assertEqual(
            filter(tree, lambda value: isinstance(value, float)),
            set([3.5])
        )
        self.assertEqual(
            filter(tree, lambda value: isinstance(value, str)),
            set(["a"])
        )
