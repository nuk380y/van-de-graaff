class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Overridden by child classes")

    def props_to_html(self):
        attribs = list()

        for key in self.props:
            attribs.append(f' {key}="{self.props[key]}"')

        return "".join(attribs)

    def __repr__(self):
        tag_repr = "None"
        value_repr = "None"

        if self.tag != None:
            tag_repr = f'"{self.tag}"'

        if self.value != None:
            value_repr = f'"{self.value}"'

        return f"HTMLNode({tag_repr}, {value_repr}, {self.children}, {self.props})"
