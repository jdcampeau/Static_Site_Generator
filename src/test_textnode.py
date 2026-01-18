import unittest

from textnode import TextType, TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a node", TextType.TEXT)
        node2 = TextNode("This is a different Node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("Test", TextType.TEXT)
        node2 = TextNode("Test", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_links(self):
        node1 = TextNode("Test", TextType.LINK, "https://www.boot.dev/")
        node2 = TextNode("Test", TextType.LINK, "https://www.boot.dev/")
        self.assertEqual(node1, node2)

    def test_not_eq_links(self):
        node = TextNode("Test", TextType.LINK, "https://www.boot.dev/")
        node2 = TextNode("Test", TextType.LINK, "https://www.facebook.com/")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def text_text_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/")
        htmo_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/"})


if __name__ == "__main__":
    unittest.main()
