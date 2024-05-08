class BinaryTreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_value(self):
        return self.value

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

def add(root, value):
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

def remove(root, value):
    if root is None:
        return None
    parent = get_parent(root, value)
    if parent is not None:
        if parent.left and parent.left.value == value:
            delete_node = parent.left
        else:
            delete_node = parent.right
        if delete_node is not None:
            new_root = BinaryTreeNode(root.value)
            new_root.left = root.left
            new_root.right = root.right
            if delete_node.left is None:
                if parent.left and parent.left.value == value:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.left = delete_node.right
                    if parent.right:
                        new_parent.right = parent.right
                    new_root.left = new_parent
                else:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.right = delete_node.right
                    new_root.right = new_parent
            elif delete_node.right is None:
                if parent.left and parent.left.value == value:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.left = delete_node.left
                    if parent.right:
                        new_parent.right = parent.right
                    new_root.left = new_parent
                else:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.right = delete_node.left
                    new_root.right = new_parent
            else:  # left and right all are not None
                tmp_pre = delete_node
                tmp_next = delete_node.right
                while tmp_next.left:
                    tmp_pre = tmp_next
                    tmp_next = tmp_next.left

                new_delete_node = BinaryTreeNode(delete_node.value)
                new_delete_node.left = delete_node.left
                new_delete_node.right = delete_node.right

                if tmp_pre == delete_node:
                    new_tmp_pre = new_delete_node
                else:
                    new_tmp_pre = BinaryTreeNode(tmp_pre.value)
                    new_tmp_pre.left = tmp_pre.left
                    new_tmp_pre.right = tmp_pre.right

                if parent.left and parent.left.value == value:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.left = tmp_next
                    new_parent.right = parent.right
                    new_root.left = new_parent
                else:
                    new_parent = BinaryTreeNode(parent.value)
                    new_parent.right = tmp_next
                    new_root.right = new_parent
                    
                if new_tmp_pre != new_delete_node:
                    new_tmp_pre.left = tmp_next.right
                    tmp_next.right = new_delete_node.right

            return new_root
        else:
            return False
    else:
        return False

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
        root = add(root, value)
    return root

def filter(root):
    filter_list = to_list(root)
    result_list = []
    for value in filter_list:
        if isinstance(value, int):
            result_list.append(value)
    return result_list

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

def empty():
    return None

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
    new_value = root_A.value + root_B.value
    new_left = concat(root_A.left, root_B.left)
    new_right = concat(root_A.right, root_B.right)
    return BinaryTreeNode(new_value, new_left, new_right)

def intersection(root_A, root_B):
    list_A = to_list(root_A)
    list_B = to_list(root_B)
    result_list = []
    for value in list_A:
        if value in list_B:
            result_list.append(value)
    return result_list

def member(root, value):
    list = to_list(root)
    if value in list:
        return True
    else:
        return False