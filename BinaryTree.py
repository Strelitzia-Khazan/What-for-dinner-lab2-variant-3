class BinaryTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        return self.value
    
    def __str__(self):
        return str(to_set(self))

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self is None or other is None:
            return False
        if self.value == other.value:
            left_equal = self.left.__eq__(other.left)
            right_equal = self.right.__eq__(other.right)
            return left_equal and right_equal
        else:
            return False

def copy(root):
    if root is None:
        return None
    new_root = BinaryTreeNode(root.value)
    new_root.left = copy(root.left)
    new_root.right = copy(root.right)
    return new_root

def add(value, root):
    # if root is None and value is None:
    #     return None
    # if root.value is None:
    #     return BinaryTreeNode()
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

def remove(root, value):
    if root is None:
        return None
    if value is None:
        return root
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
            else:  # left and right all are not None
                leaf_node = find_leaf_node(delete_node)
                alternative_node = leaf_node
                leaf_node_parent = get_parent(root, leaf_node.value)
                if leaf_node_parent.left.value == leaf_node.value:
                    leaf_node_parent.left = None
                else:
                    leaf_node_parent.left = None
                alternative_node.left = delete_node.left
                alternative_node.right = delete_node.right
                if parent.left.value == value:
                    parent.left = alternative_node
                else:
                    parent.right = alternative_node
            return new_root
        else:
            return root
    else:
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
        
def to_set(root):
    # if root is None or root.value is None:
    if root.value is None:
        return {None}
    result_set = {root.value}
    left_set = to_set(root.left)
    right_set = to_set(root.right)
    return result_set.union(left_set, right_set)
 
def to_list(root):
    if root is None or root.value is None:
        return []
    result_list = [root.value]
    left_list = to_list(root.left)
    right_list = to_list(root.right)
    return result_list + left_list + right_list

def get_depth(node):
    if node is None:
        return 0
    depth = 1
    left_depth = get_depth(node.left)
    right_depth = get_depth(node.right)
    return depth + max(left_depth, right_depth)

def get_size(node):
    if node is None:
        return 0
    size = 1
    left_size = get_size(node.left)
    right_size = get_size(node.right)
    return size + left_size + right_size

def from_list(lst):
    root = None
    for value in lst:
        root = add(value, root)
    return root

def find(root, function):
    find_list = to_list(root)
    result_list = function(find_list)
    return result_list

def filter(root, function):
    filter_list = to_list(root)
    result_list = function(filter_list)
    return result_list

"""    
    result_list = []
    for value in filter_list:
        if isinstance(value, int):
            result_list.append(value)
"""

def map(root,function):
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

def reduce(root, function, initial_state=0):
    state = initial_state
    result_list = to_list(root)
    for value in result_list:
        state = function(state, value)
    return state

def mempty():
    return BinaryTreeNode()

def iterator(root):
    if root is None:
        return None
    node_queue = [root]

    def generate_value():
        if node_queue is None:
            raise StopIteration
        current_node = node_queue.pop(0)
        if current_node.left is not None:
            node_queue.append(current_node.left)
        if current_node.right is not None:
            node_queue.append(current_node.right)
        return current_node.value
    return generate_value

def concat(root_A, root_B):
    if root_A is None:
        return root_B
    if root_B is None:
        return root_A
    list_A = to_list(root_A)
    list_B = to_list(root_B)
    new_list = list_A + list_B
    new_root = from_list(new_list)
    return new_root

def intersection(root_A, root_B):
    if root_A is None or root_B is None:
        return None
    list_A = to_list(root_A)
    list_B = to_list(root_B)
    result_list = []
    for value in list_A:
        if value in list_B:
            result_list.append(value)
    return result_list

def member(value, root):
    list = to_list(root)
    if value in list:
        return True
    else:
        return False