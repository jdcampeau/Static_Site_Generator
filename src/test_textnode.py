import unittest

from textnode import TextType, TextNode, text_node_to_html_node, split_nodes_delimiter

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

    def test_split_delimiter(self):
        node1 = TextNode("boldtext", TextType.BOLD)
        node2 = TextNode("plain text with some **bold text** nested in it", TextType.TEXT)
        new_node_list = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected_result = [TextNode("boldtext", TextType.BOLD), TextNode("plain text with some ", TextType.TEXT), TextNode("bold text", TextType.BOLD), TextNode(" nested in it", TextType.TEXT)]
        self.assertEqual(new_node_list, expected_result)

    def test_split_delimiter_error(self):
        node1 = TextNode("invalid _Markdown syntax", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node1], "_", TextType.ITALIC)
    
    def test_split_del_italic_first(self):
        node = TextNode("_italics_ first", TextType.TEXT)
        new_node_list = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_result = [TextNode("italics", TextType.ITALIC), TextNode(" first", TextType.TEXT)]
        self.assertEqual(new_node_list, expected_result)

    def test_split_del_bold_first(self):
        node = TextNode("**bold** first", TextType.TEXT)
        new_node_list = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_result = [TextNode("bold", TextType.BOLD), TextNode(" first", TextType.TEXT)]
        self.assertEqual(new_node_list, expected_result)

if __name__ == "__main__":
    unittest.main()
