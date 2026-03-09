from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode

from textnode import text_node_to_html_node

import re

class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list" 
    ORDERED_LIST = "ordered list"

def block_to_block_type(markdown_text): #input must be a single block, not a list of blocks or multiple blocks in a single string
    if markdown_text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING.value
    elif markdown_text.startswith("```\n") and markdown_text.startswith("```", -3):
        return BlockType.CODE.value
    elif markdown_text.startswith(">") or markdown_text.startswith("> "):
        lines = True
        for line in markdown_text.splitlines():
            if not line.startswith(">") and not line.startswith("> "):
                lines = False
        if lines == False:
            return BlockType.PARAGRAPH.value
        else:
            return BlockType.QUOTE.value
    elif markdown_text.startswith("- "):
        lines = True
        for line in markdown_text.splitlines():
            if not line.startswith("- "):
                lines = False
        if lines == False:
            return BlockType.PARAGRAPH.value
        else:
            return BlockType.UNORDERED_LIST.value
    elif markdown_text.startswith("1. "):
        lines = True
        num = 1
        for line in markdown_text.splitlines():
            if line.startswith(f"{num}. "):
                num += 1
            else:
                break
        if num > len(markdown_text.splitlines()):
            return BlockType.ORDERED_LIST.value
        else:
            return BlockType.PARAGRAPH.value
    else:
        return BlockType.PARAGRAPH.value

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def markdown_to_blocks(raw_markdown):
    blocks = []
    initial_blocks = raw_markdown.split("\n\n")
    for block in initial_blocks:
        strip = block.strip()
        if strip == "":
            continue
        blocks.append(strip)
    return blocks

def markdown_to_html(markdown):
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
