import itertools
import unittest
from hypothesis import given
from BinaryTree import *
from hypothesis import strategies as st


class TestBinaryTreeSet(unittest.TestCase):
    # def test_api(self):
    #     empty = BinaryTreeSet()
    #     self.assertEqual(str(add(None, empty)), "{None}")
    #     l1 = add(None, add(1, empty))
    #     l2 = add(1, add(None, empty))
    #     self.assertEqual(str(empty), "{}")
    #     self.assertTrue(str(l1) == "{None, 1}" or str(l1) == "{1, None}\
    #     ")
    #     self.assertNotEqual(empty, l1)
    #     self.assertNotEqual(empty, l2)
    #     self.assertEqual(l1, l2)
    #     self.assertEqual(l1, add(None, add(1, l1)))
    #     self.assertEqual(get_size(empty), 0)
    #     self.assertEqual(get_size(l1), 2)
    #     self.assertEqual(get_size(l2), 2)
    #
    #     self.assertEqual(str(remove(l1, None)), "{1}")
    #     self.assertEqual(str(remove(l1, 1)), "{None}")
    #     # self.assertFalse(member(None, empty))
    #     # self.assertTrue(member(None, l1))
    #     # self.assertTrue(member(1, l1))
    #     # self.assertFalse(member(2, l1))
    #     self.assertEqual(intersection(l1, l2), l1)
    #     self.assertEqual(intersection(l1, l2), l2)
    #     self.assertEqual(intersection(l1, empty), empty)
    #     self.assertEqual(intersection(l1, add(None, empty)), add(None, empty))
    #     self.assertTrue(to_list(l1) == [None, 1] or to_list(l1) == [1,\
    #     None])
    #     self.assertEqual(l1, from_list( [None, 1]))
    #     self.assertEqual(l1, from_list([1, None, 1]))
    #     self.assertEqual(concat(l1, l2), from_list([None, 1, 1, None]))
    #     buf = []
    #     for e in l1:
    #         buf.append(e)
    #     self.assertIn(buf, map(list, itertools.permutations([1, None])))
    #     lst = to_list(l1) + to_list(l2)
    #     for e in l1:
    #         lst.remove(e)
    #     for e in l2:
    #         lst.remove(e)
    #     self.assertEqual(lst, [])

    def test_filter(self):
        # tree = from_list([1, None, 'a', 2, 'b', 3])
        tree = from_list([1, 'a', 2, 'b', 3])
        filtered_tree_list = filter(tree)
        self.assertEqual(filtered_tree_list, [1, 3, 2])

    def test_map(self):
        tree = from_list([1, 2, 3])
        mapped_tree = map(tree, lambda x: x * 2)
        self.assertEqual(to_list(mapped_tree), [2, 4, 6])

    def test_reduce(self):
        tree = from_list([1, 2, 3])
        reduced_value = reduce(tree, lambda x, y: x + y)
        self.assertEqual(reduced_value, 6)

    def test_empty(self):
        empty_tree = empty()
        self.assertIsNone(empty_tree)

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
        new_root = add(self.root, 6)
        self.assertTrue(new_root.right.left.value == 6)

    def test_get_parent(self):
        parent = get_parent(self.root, 5)
        self.assertEqual(parent.value, 2)

    def test_remove_root(self):
        # 创建一棵树：1 -> 2 -> 3
        root = from_list([1, 2, 3])
        new_root = remove(root, 1)
        # 断言根节点是否被正确删除
        self.assertEqual(new_root.get_value(), 2)

    def test_remove_leaf(self):
        # 创建一棵树：1 -> 2 -> 3
        root = from_list([1, 2, 3])
        new_root = remove(root, 3)
        # 断言叶子节点是否被正确删除
        self.assertIsNone(new_root.right)

    def test_remove_single_child_node(self):
        # 创建一棵树：1 -> 2 -> 3
        root = from_list([1, 2, 3])
        new_root = remove(root, 2)
        # 断言具有单个子节点的节点是否被正确删除
        self.assertEqual(new_root.get_value(), 1)
        self.assertEqual(new_root.right.get_value(), 3)
        self.assertIsNone(new_root.left)

    def test_remove_node_with_two_children(self):
        # 创建一棵树：2 -> 1 -> 3
        root = from_list([2, 1, 3])
        new_root = remove(root, 2)
        # 断言具有两个子节点的节点是否被正确删除
        self.assertEqual(new_root.get_value(), 3)
        self.assertEqual(new_root.left.get_value(), 1)

    def test_get_depth(self):
        depth = get_depth(self.root)
        self.assertEqual(depth, 3)

    def test_get_size(self):
        size = get_size(self.root)
        self.assertEqual(size, 5)

    def test_from_list_and_to_list(self):
        lst = [1, 2, 3, 4, 5]
        new_root = from_list(lst)
        self.assertEqual(to_list(new_root), [1, 2, 4, 5, 3])

    def test_reduce(self):
        def sum_values(state, value):
            return state + value

        total_sum = reduce(self.root, sum_values)
        self.assertEqual(total_sum, 15)

    def test_iterator(self):
        iterator_func = iterator(self.root)
        values = [iterator_func() for _ in range(get_size(self.root))]
        self.assertEqual(values, [1, 2, 3, 4, 5])

    def test_intersection(self):
        root_A = from_list([1, 2, 3, 4, 5])
        root_B = from_list([4, 5, 6, 7, 8])
        intersected_values = intersection(root_A, root_B)
        self.assertEqual(intersected_values, [4, 5])

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
            tree_empty = empty()
            tree_ea = concat(tree_empty, tree_a)
            tree_ae = concat(tree_a, tree_empty)
            list_ae = to_list(tree_ae)
            list_ea = to_list(tree_ea)
            self.assertEqual(list_ae, list_ea)


