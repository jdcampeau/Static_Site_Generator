from enum import Enum

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
            if not line.startswith(">") or not line.startswith("> "):
                lines = False
        if lines == False:
            raise Exception("Invalid markdown syntax. Every line of a quote must start with '>' or '> '")
        else:
            return BlockType.QUOTE.value
    elif markdown_text.startswith("- "):
        lines = True
        for line in markdown_text.splitlines():
            if not line.startswith("- "):
                lines = False
        if lines == False:
            raise Exception("Invalid markdown syntax. Every line of an unordered list must start with '- '")
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
            raise Exception("Invalid markdown syntax. Every line of an ordered list must start with '{number}. '")
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
