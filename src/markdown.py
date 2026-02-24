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
        return BlockType.HEADING
    elif markdown_text.startswith("```\n") and markdown_text.startswith("```", -3):
        return BlockType.CODE
    elif markdown_text.startswith(">") or markdown_text.startwith("> "):
        lines = True
        for i in range(len(markdown_text)):
            if markdown_text[i] == "\n":
                if markdown_text[i+1] != ">" and markdown_text[i+1] != "> ":
                    lines = False
        if lines == False:
            continue
        else:
            return BlockType.QUOTE
    elif markdown_text.startswith("- "):
        lines = True
        for i in range(len(markdown_text)):
            if markdown_text[i] == "\n":
                if markdown_text[i+1] != "- ":
                    lines = False
        if lines == False:
            continue
        else:
            return BlockType.UNORDERED_LIST
    elif markdown_text.startswith("1. "):
        lines = True
        line = 2
        for i in range(len(markdown_text)):
            if markdown_text[i] == "\n":
                if markdown_text[i+1] != "{line}":
                    lines = False
                else:
                    line += 1
                    if markdown_text[i+2] != ".":
                        lines = False
                    else:
                        if markdown_text[i+3] != " ":
                            lines = False
        if line == False:
            continue
        else:
            return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

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
