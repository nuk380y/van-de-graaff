import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            fragments = node.text.split(delimiter)

            if len(fragments) % 2 == 0:
                raise SyntaxError("unmatched delimiter")

            for index, value in enumerate(fragments):
                if index % 2 != 0:
                    new_nodes.append(TextNode(value, text_type))
                else:
                    new_nodes.append(TextNode(value, node.text_type))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
