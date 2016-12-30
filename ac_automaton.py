#!/usr/bin/env python
# encoding: utf-8
from collections import deque


class Node:
    def __init__(self, value=None):
        self.ch = value
        self.transitions = []
        self.fail = None
        self.output = []


class Ac_automaton:
    def __init__(self, dictionary):
        self.root = self.buildAc(dictionary)

    def buildAc(self, dictionary):
        root = Node()
        # create a ordinary Trie
        for keyword in dictionary:
            current_node = root
            for char in keyword:
                new_node = None
                for child_node in current_node.transitions:
                    if child_node.ch == char:
                        new_node = child_node
                        break
                if new_node is None:
                    new_node = Node(value=char)
                    current_node.transitions.append(new_node)
                current_node = new_node
            current_node.output.append(keyword)

        # construct the fail transitions in a BFS way
        queue = deque([root])
        while queue:
            current_node = queue.popleft()
            for child_node in current_node.transitions:
                queue.append(child_node)
                fail_state_node = current_node.fail
                while fail_state_node and not any(x for x in fail_state_node.transitions if child_node.ch == x.ch and x is not child_node):
                    fail_state_node = fail_state_node.fail
                if fail_state_node:
                    child_node.fail = next((x for x in fail_state_node.transitions if child_node.ch == x.ch and x is not child_node), root)
                else:
                    child_node.fail = root
                if len(child_node.fail.output) > 0:
                    child_node.output = child_node.output + child_node.fail.output
        return root

    def search(self, text):
        current_node = self.root
        for index, charactor in enumerate(text):
            while not next((x for x in current_node.transitions if x.ch == charactor), None) and current_node.fail:
                current_node = current_node.fail
            current_node = next((x for x in current_node.transitions if x.ch == charactor), self.root)
            if len(current_node.output) > 0:
                for result in current_node.output:
                    yield index, result
