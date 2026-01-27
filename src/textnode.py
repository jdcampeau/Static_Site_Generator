from enum import Enum

from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (
                self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url
            )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def split_nodes_delimiter(input_nodes, delimiter, text_type):
    output = []
    for node in input_nodes:
        if node.text_type is not TextType.TEXT:
            output.append(node)
        else:
            sub_output = []
            string_list = node.text.split(delimiter)
            delimiter_count = 0
            for i in range(len(node.text)):
                if delimiter == "**":
                    if node.text[i] == "*" and node.text[i+1] == "*":
                        delimiter_count += 1
                else:
                    if node.text[i] == delimiter:
                        delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception("invalid Markdown syntax")
            plaintext = True
            if delimiter == "**":
                if node.text[0] == "*" and node.text[1] == "*":
                    plaintext = False
            else:
                if node.text[0] == delimiter:
                    plaintext = False
            for strng in string_list:
                if plaintext is False:
                    new_node = TextNode(strng, text_type)
                    sub_output.append(new_node)
                    plaintext = True
                else:
                    new_node = TextNode(strng, TextType.TEXT)
                    sub_output.append(new_node)
                    plaintext = False
            output.extend(sub_output)
    return output

def text_node_to_html_node(TextNode):
    if TextNode.text_type == TextType.TEXT:
        return LeafNode(None, TextNode.text)
    if TextNode.text_type == TextType.BOLD:
        return LeafNode("b", TextNode.text)
    if TextNode.text_type == TextType.ITALIC:
        return LeafNode("i", TextNode.text)
    if TextNode.text_type == TextType.CODE:
        return LeafNode("code", TextNode.text)
    if TextNode.text_type == TextType.LINK:
        return LeafNode("a", TextNode.text, {"href": TextNode.url})
    if TextNode.text_type == TextType.IMAGE:
        return LeafNode("img", "", {TextNode.url: TextNode.text})
    else:
        raise Exception("Unknown text type")


