from typing import Optional, Callable, List, Union, TypeVar, Generic

ValueType = TypeVar('ValueType', bound=Union[int, str, float, None])


class BinaryTreeNode(Generic[ValueType]):
    def __init__(self, value: ValueType,
                 left: Optional['BinaryTreeNode[ValueType]'] = None,
                 right: Optional['BinaryTreeNode[ValueType]'] = None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return str(to_set(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryTreeNode):
            return False
        return str(self) == str(other)

    def get_value(self):
        return self.value


def to_set(node: Optional[BinaryTreeNode[ValueType]]) -> set:
    if node is None:
        return set()
    return to_set(node.left).union({node.value}, to_set(node.right))


def mempty() -> Optional[BinaryTreeNode[ValueType]]:
    return None


def add(value: ValueType, root: Optional[BinaryTreeNode[ValueType]]) -> BinaryTreeNode[ValueType]:
    add_node = BinaryTreeNode(value)
    if root is None:
        return add_node
    new_root = copy(root)
    node_queue = [new_root]
    while node_queue:
        node = node_queue.pop(0)
        if node.left:
            node_queue.append(node.left)
        else:
            node.left = add_node
            return new_root
        if node.right:
            node_queue.append(node.right)
        else:
            node.right = add_node
            return new_root
    return new_root


# Auxiliary function for copying binary trees
def copy(root: Optional[BinaryTreeNode[ValueType]]) -> Optional[BinaryTreeNode[ValueType]]:
    if root is None:
        return None
    new_root = BinaryTreeNode(root.value)
    new_root.left = copy(root.left)
    new_root.right = copy(root.right)
    return new_root


def get_size(node):
    if node is None:
        return 0
    size = 1
    left_size = get_size(node.left)
    right_size = get_size(node.right)
    return size + left_size + right_size


def remove(root, value):
    if root is None:
        return None
    new_root = copy(root)
    parent = get_parent(root, value)
    new_parent = get_parent(new_root, value)
    if parent is not None:
        if parent.left and parent.left.value == value:
            delete_node = new_parent.left
        else:
            delete_node = new_parent.right
        if delete_node is not None:
            if delete_node.left is None:
                if parent.left.value == value:
                    new_parent.left = delete_node.right
                else:
                    new_parent.right = delete_node.right
            elif delete_node.right is None:
                if parent.left.value == value:
                    new_parent.left = delete_node.left
                else:
                    new_parent.right = delete_node.left
            else:
                # left and right all are not None
                leaf_node = find_leaf_node(delete_node)
                added_root = BinaryTreeNode(leaf_node.value)
                leaf_node_parent = get_parent(new_root, leaf_node.value)
                if leaf_node_parent.left.value == leaf_node.value:
                    leaf_node_parent.left = None
                else:
                    leaf_node_parent.left = None
                added_root.left = delete_node.left
                added_root.right = delete_node.right
                if parent.left.value == value:
                    new_parent.left = added_root
                else:
                    new_parent.right = added_root
            return new_root
        else:
            return root
    else:
        # root node is the delete node
        if root.value == value:
            delete_node = new_root
            leaf_node = find_leaf_node(delete_node)
            result_root = BinaryTreeNode(leaf_node.value)
            leaf_node_parent = get_parent(new_root, leaf_node.value)
            if leaf_node_parent.left.value == leaf_node.value:
                leaf_node_parent.left = None
            else:
                leaf_node_parent.right = None
            result_root.left = new_root.left
            result_root.right = new_root.right
            return result_root
        else:
            return root


def get_parent(root, value):
    if root is None or root.value == value:
        return None
    node_queue = [root]
    while node_queue:
        node = node_queue.pop(0)
        if node.left and node.left.value == value or node.right and node.right.value == value:
            return node
        if node.left:
            node_queue.append(node.left)
        if node.right:
            node_queue.append(node.right)
    return None


def find_leaf_node(root):
    if root is None:
        return None
    stack = [root]
    while stack:
        current_node = stack.pop()
        # If the current node is a leaf node and not the input node's child
        if current_node.left is None and current_node.right is None:
            return current_node
        # Push the right child first to ensure left child is visited first
        if current_node.right:
            stack.append(current_node.right)
        if current_node.left:
            stack.append(current_node.left)
    return None


def member(value, root):
    list = to_list(root)
    if value in list:
        return True
    else:
        return False


# Convert tree to list using preorder traversal
def to_list(root):
    if root is None:
        return []
    result_list = [root.value]
    left_list = to_list(root.left)
    right_list = to_list(root.right)
    return result_list + left_list + right_list


def intersection(root_A, root_B):
    if root_A is None or root_B is None:
        return None
    list_A = to_set(root_A)
    list_B = to_set(root_B)
    result_set = set()
    for value in list_A:
        if value in list_B:
            result_set.add(value)
    return result_set


def from_list(lst: List[ValueType]) -> Optional[BinaryTreeNode[ValueType]]:
    root = None
    for value in lst:
        root = add(value, root)
    return root


# Using level-order traversal in concat() can comply with the monoid group when implementing the function.
def concat(root_A: Optional[BinaryTreeNode[ValueType]], root_B: Optional[BinaryTreeNode[ValueType]]) -> Optional[BinaryTreeNode[ValueType]]:
    if root_A is None:
        return root_B
    if root_B is None:
        return root_A
    
    def level_order_traversal(root: Optional[BinaryTreeNode[ValueType]]) -> Optional[BinaryTreeNode[ValueType]]:
        level_order_list = []
        level_order_queue = [root]
        while level_order_queue:
            node = level_order_queue.pop(0)
            level_order_list.append(node.value)

            if node.left:
                level_order_queue.append(node.left)
            if node.right:
                level_order_queue.append(node.right)
        return level_order_list
    
    new_root = copy(root_A)
    new_node_list = level_order_traversal(root_B)
    for value in new_node_list:
        new_root = add(value, new_root)
    return new_root


def iterator(root: Optional[BinaryTreeNode[ValueType]]):
    if root is None:
        return
    node_queue = [root]
    while node_queue:
        current_node = node_queue.pop(0)
        yield current_node.value
        if current_node.left is not None:
            node_queue.append(current_node.left)
        if current_node.right is not None:
            node_queue.append(current_node.right)


def reduce(root, function, initial_state=0):
    state = initial_state
    result_list = to_list(root)
    for value in result_list:
        state = function(state, value)
    return state


def get_depth(node):
    if node is None:
        return 0
    depth = 1
    left_depth = get_depth(node.left)
    right_depth = get_depth(node.right)
    return depth + max(left_depth, right_depth)


def filter(root: Optional[BinaryTreeNode[ValueType]], f: Callable[[ValueType], bool]) -> set[ValueType]:
    result_set: set[ValueType] = set()
    if root is not None:
        result_set.update(filter(root.left, f))
        if f(root.value):
            result_set.add(root.value)
        result_set.update(filter(root.right, f))
    return result_set


def tmap(root,function):
    if root is None:
        return None

    def apply_map(root):
        if root is None:
            return None
        new_node = BinaryTreeNode(function(root.value))
        new_node.left = apply_map(root.left)
        new_node.right = apply_map(root.right)
        return new_node
    new_root = apply_map(root)
    return new_root
