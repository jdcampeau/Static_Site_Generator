import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test__repr__(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node1 = HTMLNode("a", "boot.dev link", [child1, child2], {"href": "https://www.boot.dev/"})
        print(node1.__repr__())

    def test_props_to_html(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node1 = HTMLNode("a", "boot.dev link", [child1, child2], {"href": "https://www.boot.dev/"})
        print(node1.props_to_html())
