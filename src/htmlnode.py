class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        form_str = ""
        for key, value in self.props.items():
            form_str = f'{form_str} {key}="{value}"'
        return form_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props)
        if not all([tag, value]):
            raise ValueError("Tag and value must be provided")

    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes must have a value")
        if self.tag is None:
            return f"{self.value}"
        else:
            html_props = self.props_to_html()
            return f"<{self.tag}{html_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
