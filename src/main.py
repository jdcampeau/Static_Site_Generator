from textnode import TextType, TextNode

def main():
    dummy_node = TextNode("anchortext", TextType.LINK, "https://www.boot.dev")
    print(dummy_node.__repr__())

main()

