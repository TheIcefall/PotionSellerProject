""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, it rebalances the sub-tree, rotating whenever needed.
            Returns the new root of the subtree.

            Complexity: Worst case O(log(n)), best case O(1)

        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.right_nodes += 1
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        return self.rebalance(current)

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion, it rebalances the subtree.
            Rotating when needed.

            Complexity: Worst case O(log(n)), best case O(1)
        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        child = current.right
        center = child.left

        child.left = current
        current.right = center

        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        current.right_nodes -= 1

        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """

        child = current.left
        center = child.right

        child.right = current
        current.left = center

        current.height = 1 + max(self.get_height(current.right), self.get_height(current.left))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        child.right_nodes += 1
        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def kth_largest_aux(self, k: int, root: AVLTreeNode) -> AVLTreeNode:
        """
        Auxillary function to kth largest.

        This function returns the node of the k'th largest key in the subtree.
        :param k: The key we are looking for is the k'th largest
        :param current: The root node of the subtree
        :return: Returns the kth largest node in subtree of initial input

        Complexity: Worst O(log(n)), best O(1) where n is the amount of nodes on AVLTree
        """
        if k == root.right_nodes:
            return root
        if k < root.right_nodes:
            if root.right:
                return self.kth_largest_aux(k, root.right)
            elif root.left:
                return self.kth_largest_aux(k, root.left)
            else:
                return root
        else:
            if root.left:
                return self.kth_largest_aux(k - root.right_nodes, root.left)
            else:
                return root

    def kth_largest(self, k):
        """
        Function which calls auxillary function, which returns the node of the k'th largest key in tree.
        :param k: The key we are looking for is the k'th largest
        :return: The node of the k'th largest key.

        Complexity: Worst O(log(n)), best O(1) where n is the amount of nodes on AVLTree
        """
        current = self.root
        return self.kth_largest_aux(k, current)


