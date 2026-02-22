import re

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
