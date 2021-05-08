"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import log
from random import choice
from time import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, source_collection=None):
        """Sets the initial state of self, which includes the
        contents of source_collection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, source_collection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            node_parent = top
            current_node_child = top.left
            while current_node_child.right is not None:
                node_parent = current_node_child
                current_node_child = current_node_child.right
            top.data = current_node_child.data
            if node_parent == top:
                top.left = current_node_child.left
            else:
                node_parent.right = current_node_child.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximum node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the node_parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise.
        """
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if not top:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        height = self.height()
        size = self._size

        return height < 2 * log(size + 1, 2) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where
        low <= item <= high.
        """
        item_list = []

        def recurse(node):
            """Helper function for the range_find method."""
            if node is not None:
                if low <= node.data <= high:
                    item_list.append(node.data)
                recurse(node.left)
                recurse(node.right)

        recurse(self._root)
        return sorted(item_list)

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        item_list = []
        for item in self.inorder():
            item_list.append(item)
            self.remove(item)

        self._recurse_add(item_list)

    def _recurse_add(self, item_list: list) -> None:
        """Helper method for the rebalance method."""
        if not item_list:
            return None

        if len(item_list) % 2 == 0:
            mid_index = int((len(item_list) / 2) - 1)
        else:
            mid_index = int(len(item_list) // 2)

        self.add(item_list[mid_index])
        self._recurse_add(item_list[:mid_index])
        self._recurse_add(item_list[mid_index + 1:])

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        node = self._find_node(item)

        if node is None:
            node = self._root
            while node.left is not None:
                node = node.left
            return node.data

        node = node.right
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node.data

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        node = self._find_node(item)

        if node is None:
            return None

        node = node.left
        if node is None:
            return None
        while node.right:
            node = node.right
        return node.data

    def _find_node(self, item):
        """Return a node which has the given item."""

        def recurse(node):
            """Helper function for the _find_node method."""
            if node is None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    @staticmethod
    def demo_bst(path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_list = []
        words_sorted_tree = LinkedBST()
        words_unsorted_tree = LinkedBST()
        random_words = []

        file = open(file=path, mode="r", encoding="utf-8")
        for line in file:
            words_list.append(line.strip())
            if len(words_list) < 900:
                words_sorted_tree.add(line.strip())
        file.close()

        word_list_copy = words_list.copy()
        while word_list_copy:
            word = choice(word_list_copy)
            if len(random_words) < 900:
                words_unsorted_tree.add(word)
                random_words.append(word)
            elif len(random_words) < 10000:
                random_words.append(word)
            else:
                break
            word_list_copy.remove(word)

        words_list = words_list[:900]

        print(
            "Searching for 10000 random words in:\n"
            "1) A list in alphabetical order\n"
            "2) An unbalanced binary search tree in alphabetical order\n"
            "3) An unbalanced binary search tree in random order\n"
            "4) A balanced binary search tree\n"
        )

        start = time()
        for word in random_words:
            if word in words_list:
                continue
        print("Search time in a list, alphabetical:", f"{(time() - start):.4f}")

        start = time()
        for word in random_words:
            if word in words_sorted_tree:
                continue
        print("Search time in a tree, alphabetical:", f"{(time() - start):.4f}")

        start = time()
        for word in random_words:
            if word in words_unsorted_tree:
                continue
        print("Search time in a tree, random:", f"{(time() - start):.4f}")

        words_sorted_tree.rebalance()
        start = time()
        for word in random_words:
            if word in words_sorted_tree:
                continue
        print("Search time in a balanced tree:", f"{(time() - start):.4f}")
