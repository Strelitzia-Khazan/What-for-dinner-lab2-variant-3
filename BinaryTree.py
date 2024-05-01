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

def add(root, value):
    new_node = BinaryTreeNode(value)
    if root is None:
        root = new_node
    node_queue = [root]
    while node_queue:
        node = node_queue.pop(0)
        if node.left is None:
            node.left = new_node
            return True
        elif node.right is None:
            node.right = new_node
            return True
        else:
            node_queue.append(node.left)
            node_queue.append(node.right)

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
        return False
    parent = get_parent(root, value)
    if parent:
        if parent.left.value == value:
            delete_node = parent.left
        else:
            delete_node = parent.right
        
        if delete_node.left is None:
            if parent.left.value == value:
                parent.left = delete_node.right
            else:
                parent.right = delete_node.right
        elif delete_node.right is None:
            if parent.left.value == value:
                parent.left = delete_node.left
            else:
                parent.right = delete_node.left
        else:
            tmp_pre = delete_node
            tmp_next = delete_node.right
            if tmp_next.left is None:
                tmp_pre.right = tmp_next.right
                tmp_next.left = delete_node.left
                tmp_next.right = delete_node.right                
            else:
                while tmp_next.left:
                    tmp_pre = tmp_next
                    tmp_next = tmp_next.left
                tmp_pre.left = tmp_next.right
                tmp_next.left = delete_node.left
                tmp_next.right = delete_node.right
            if parent.left.value == value:
                parent.left = tmp_next
            else:
                parent.right = tmp_next   
        return True
    else:
        return False
    
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









