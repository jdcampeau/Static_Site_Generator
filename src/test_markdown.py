import unittest

from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type

class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_blank_line(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading1(self):
        md = "# This is a heading!!!"
        block_type = block_to_block_type(md)
        expected_output = "heading"
        self.assertEqual(block_type, expected_output)

    def test_block_to_block_type_heading6(self):
        md = "###### This is another heading!"
        block_type = block_to_block_type(md)
        expected_output = "heading"
        self.assertEqual(block_type, expected_output)

    def test_block_to_block_type_code(self):
        md = "```\n[here's some fake code]```"
        bt = block_to_block_type(md)
        expected_output = "code"
        self.assertEqual(bt, expected_output)

    def test_block_to_block_type_quote(self):
        md = ">Do,\n>or do not,\n>there is no 'try'."
        bt = block_to_block_type(md)
        exp_output = "quote"
        self.assertEqual(bt, exp_output)

    def test_block_to_block_type_unordered_list(self):
        md = "- This\n- is\n- an\n- unordered\n- list."
        bt = block_to_block_type(md)
        exp_output = "unordered list"
        self.assertEqual(bt, exp_output)

    def test_block_to_block_type_ordered_list(self):
        md = "1. This is an\n2. ordered\n3. list"
        bt = block_to_block_type(md)
        exp_output = "ordered list"
        self.assertEqual(bt, exp_output)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
