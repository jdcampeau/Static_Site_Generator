import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "You're a bold one.")
        self.assertEqual(node.to_html(), "<b>You're a bold one.</b>")

    def test_link_leaf_to_html(self):
        node = LeafNode("a", "Boot.dev!", {"href":"https://www.boot.dev/" })
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/">Boot.dev!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
