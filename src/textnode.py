from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            (self.text == other.text)
            and (self.text_type == other.text_type)
            and (self.url == other.url)
        )

    def __repr__(self):
        repr_str = f'TextNode("{self.text}", {self.text_type.value}, {self.url})'
        if self.url != None:
            repr_str = f'TextNode("{self.text}", {self.text_type.value}, "{self.url}")'

        return repr_str
