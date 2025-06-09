class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""

        attribs = list()

        for key in self.props:
            attribs.append(f' {key}="{self.props[key]}"')

        return "".join(attribs)

    def __repr__(self):
        return f"HTMLNode('{self.tag}', '{self.value}', {self.children}, {self.props})"


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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError
        elif self.children == None:
            raise ValueError("no children passed with parent")
        else:
            inner_tags = []
            for child in self.children:
                inner_tags.append(child.to_html())

            # Not really required, but it keeps each line under 80 characters.
            opener = f"<{self.tag}{self.props_to_html()}>"
            contents = f"{''.join(inner_tags)}"
            closer = f"</{self.tag}>"

            formatted = f"{opener}{contents}{closer}"
            return formatted
