"""
Classes for constructing binary tree from rhythm data.
"""

import json
import uuid


class Node:
    """
    Structure rhythm data as a single node for a single rhythm.
    """
    def __init__(self, rhythm, parent_id, short=None, long=None, frequency=1, probability=0, parent_frequency=0):
        self.short = short
        self.long = long
        self.rhythm = rhythm
        self.frequency = frequency
        self.probability = probability
        self.id = str(uuid.uuid4())
        self.parent_id = parent_id

    def __repr__(self):
        """
        Represent node as a string dictionary.
        :return: string representation of node
        """
        return str({"rhythm": self.rhythm, "frequency": self.frequency,
                    "probability": self.probability, "id": self.id,
                    "parent_id": self.parent_id})

    def __iter__(self):
        if self.short:
            yield from self.short
        yield self
        if self.long:
            yield from self.long

    def to_json(self):
        """
        Return JSON string of node.
        :return: JSON node
        """
        return json.dumps(self.__dict__, default=lambda o: o.__dict__)

class Tree:
    """
    Constuct binary tree from rhythm data.
    """
    def __init__(self):
        self.root = Node("x", frequency=0, parent_id=None)

    def __repr__(self):
        """
        Represent tree as string dictionary
        :return: string representation of node.
        """
        return self.root.__repr__()

    def to_json(self):
        """
        Return JSON string of tree.
        :return: JSON tree
        """
        return self.root.to_json()

    def add(self, rhythm):
        """
        Add rhythm to tree.
        :param rhythm: "x", "-", or "u"
        :ptype rhythm: str
        :return: void
        """
        self.root.frequency += 1
        rhythm = rhythm[::-1]
        for index_of_rhythm, char_in_rhythm in enumerate(rhythm):
            path = rhythm[:index_of_rhythm+1]
            curr_node = self.root
            for index, char in enumerate(path):
                if index == len(path) - 1:
                    if char == "-":
                        if curr_node.long is not None:
                            curr_node.long.frequency += 1
                        else:
                            curr_node.long = Node("-", parent_id=curr_node.id)
                    elif char == "u":
                        if curr_node.short is not None:
                            curr_node.short.frequency += 1
                        else:
                            curr_node.short = Node("u", parent_id=curr_node.id)
                else:
                    if char == "-":
                        curr_node = curr_node.long
                    if char == "u":
                        curr_node = curr_node.short

    def calculate_probability(self):
        nodes = [node.__dict__ for node in self.root]
        for node in self.root:
            node = node.__dict__
            parent_node = [n for n in nodes if n["id"] == node["parent_id"]]
            if len(parent_node) == 1:
                node["probability"] = round(node["frequency"] / parent_node[0]["frequency"], 5)


if __name__ == "__main__":
    test_rhythms1 = ["-u-x", "--ux", "uu-x"]
    tree = Tree()
    tree.add(test_rhythms1[0])
    tree.add(test_rhythms1[1])
    tree.add(test_rhythms1[2])
    tree.calculate_probability()
    print(tree.to_json())
