from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode

from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type

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
            if delimiter_count == 0:
                output.append(node)
                continue
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
                if strng == "":
                    continue
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

def split_nodes_image(old_nodes):
    output = []
    for node in old_nodes:
        if node.text == "":
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            output.append(node)
            continue
        sections = node.text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
        real_sections = sections
        if len(matches) > 1:
            for i in range(1, len(matches)):   
                next_section = real_sections.pop(len(real_sections)-1)
                new_sections = next_section.split(f"![{matches[i][0]}]({matches[i][1]})", 1)
                real_sections.extend(new_sections)
        matches_index = 0
        for i in range(len(real_sections)):
            if real_sections[i] == "":
                if matches_index == 0:
                    match_node = TextNode(matches[matches_index][0], TextType.IMAGE, matches[matches_index][1])
                    output.append(match_node)
                    matches_index += 1
                else:
                    continue
            else:
                new_node = TextNode(real_sections[i], TextType.TEXT)
                output.append(new_node)
                if matches_index <= len(matches)-1:
                    match_node = TextNode(matches[matches_index][0], TextType.IMAGE, matches[matches_index][1])
                    output.append(match_node)
                matches_index += 1
    return output

def split_nodes_link(old_nodes):  
    output = []
    for node in old_nodes:
        if node.text == "":
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            output.append(node)
            continue
        sections = node.text.split(f"[{matches[0][0]}]({matches[0][1]})")
        real_sections = sections
        if len(matches) > 1:
            for i in range(len(matches)):
                next_section = real_sections.pop(len(real_sections)-1)
                new_sections = next_section.split(f"[{matches[i][0]}]({matches[i][1]})", 1)
                real_sections.extend(new_sections)
        matches_index = 0
        for i in range(len(real_sections)):
            if real_sections[i] == "":
                if matches_index == 0:
                    match_node = TextNode(matches[matches_index][0], TextType.LINK, matches[matches_index][1])
                    output.append(match_node)
                    matches_index += 1
                else:
                    continue
            else:
                new_node = TextNode(real_sections[i], TextType.TEXT)
                output.append(new_node)
                if matches_index <= len(matches)-1:
                    match_node = TextNode(matches[matches_index][0], TextType.LINK, matches[matches_index][1])
                    output.append(match_node)
                matches_index += 1
        return output

def markdown_to_textnode(markdown_block):
    starting_node = [TextNode(markdown_block, TextType.TEXT)]
    bold_check = split_nodes_delimiter(starting_node, "**", TextType.BOLD)
    italic_check = split_nodes_delimiter(bold_check, "_", TextType.ITALIC)
    code_check = split_nodes_delimiter(italic_check, "`", TextType.CODE)
    image_check = split_nodes_image(code_check)
    link_check = split_nodes_link(image_check)
    return link_check

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

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    leaf_nodes = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        if block_type == "code":
            text_node = TextNode(block, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            leaf_nodes.append(html_node)
        else:
            htmlnodes = text_to_children(block)
            if len(htmlnodes) == 1:
                leaf_nodes.extend(htmlnodes)
            else:
                parent_node = ParentNode("div", htmlnodes)
                leaf_nodes.append(parent_node)
        #create HTMLNode(s) for remaining block types
        #add HTMLNode to above list
    grandparent_node = ParentNode("div", leaf_nodes)
    return grandparent_node

def text_to_children(text):
    textnodes = markdown_to_textnode(text)
    output = []
    for tnode in textnodes:
        htmlnode = text_node_to_html_node(tnode)
        output.append(htmlnode)
    return output


