from extractutils import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue
        else:
            fragments = node.text.split(delimiter)

            if len(fragments) % 2 == 0:
                raise SyntaxError("unmatched delimiter")

            for index, value in enumerate(fragments):
                if value == "":
                    continue

                if index % 2 != 0:
                    new_nodes.append(TextNode(value, text_type))
                else:
                    new_nodes.append(TextNode(value, node.text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        for alt, url in images:
            pre, post = text.split(f"![{alt}]({url})", 1)

            if pre:
                new_nodes.append(TextNode(pre, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE_TEXT, url))

            text = post

        if text != "":
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        for alt, url in links:
            pre, post = text.split(f"[{alt}]({url})", 1)

            if pre:
                new_nodes.append(TextNode(pre, TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK_TEXT, url))

            text = post

        if text != "":
            new_nodes.append(TextNode(text, TextType.PLAIN_TEXT))

    return new_nodes
