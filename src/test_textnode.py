import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()
