import re
from enum import Enum

from extractutils import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def text_to_textnodes(text):
    # Normalize the passed value.
    passed_node = TextNode("", TextType.PLAIN_TEXT)
    if type(text) == str:
        passed_node = TextNode(text, TextType.PLAIN_TEXT)
    elif type(text) == TextNode:
        passed_node = text

    new_nodes = []

    new_nodes = split_nodes_image([passed_node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC_TEXT)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE_TEXT)

    return new_nodes


def markdown_to_blocks(markdown):
    text_blocks = []

    blocks = markdown.split("\n\n")

    for block in blocks:
        block = block.strip()

        if block == "\n":
            continue
        elif block != "":
            text_blocks.append(block)

    return text_blocks


def block_to_block_type(md):
    identified_blocks = []

    # Define multiline patterns
    patt_code = re.compile(r"`{3}[a-z]*\n[\s\S]*?\n`{3}", re.MULTILINE)
    patt_quote = re.compile(r">{1}\s\w*", re.MULTILINE)
    patt_unordered = re.compile(r"^[\-\*]\s.+\n", re.MULTILINE)
    patt_ordered = re.compile(r"^[0-9]{1,3}\.\s.+\n", re.MULTILINE)

    for string in markdown_to_blocks(md):
        new_node = TextNode("", None)

        # Match for headings
        if re.match(r"^#{1,6}\s\w+", string):
            new_node = TextNode(string, BlockType.HEADING)
        # Match for code blocks
        elif patt_code.match(string):
            new_node = TextNode(string, BlockType.CODE)
        # Match for quotes
        elif patt_quote.match(string):
            new_node = TextNode(string, BlockType.QUOTE)
        # Match for unordered
        elif patt_unordered.match(string):
            new_node = TextNode(string, BlockType.UNORDERED_LIST)
        # Match for ordered
        elif patt_ordered.match(string):
            new_node = TextNode(string, BlockType.ORDERED_LIST)
        else:
            new_node = TextNode(string, BlockType.PARAGRAPH)

        identified_blocks.append(new_node)

    return identified_blocks
