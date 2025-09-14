class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""

        attribs = ""

        for key in self.props:
            attribs += f' {key}="{self.props[key]}"'

        return "".join(attribs)

    def __repr__(self):
        tag_repr = "None"
        value_repr = "None"

        if self.tag != None:
            tag_repr = f'"{self.tag}"'

        if self.value != None:
            value_repr = f'"{self.value}"'

        return f"HTMLNode({tag_repr}, {value_repr}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            formatted = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return formatted
