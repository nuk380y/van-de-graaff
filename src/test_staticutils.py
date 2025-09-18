import unittest

# from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from staticutils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestUtils(unittest.TestCase):
    # split_nodes_delimiter
    def test_split_nodes_delimiter_with_code(self):
        node = TextNode("This is text with a `code block` in it", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)

    def test_split_nodes_delimiter_with_bold(self):
        node = TextNode("This text has **bold text** in it.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD_TEXT)

    def test_split_nodes_delimiter_multiple_types(self):
        node = TextNode(
            "This text has **bold** and _italic_ text.", TextType.PLAIN_TEXT
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes[0].text, "This text has **bold** and ")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN_TEXT)

    # Need to add more test that handle starting/ending with formatted sections.

    # extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_not_links(self):
        matches = extract_markdown_images(
            "A [link](https://start.duckduckgo.com) and an ![image](https://imgur.com/blah)"
        )
        self.assertListEqual([("image", "https://imgur.com/blah")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This ![string](https://imgur.com/spool_emoji) has ![two](https://imgur.com/number_two) images!"
        )
        self.assertListEqual(
            [
                ("string", "https://imgur.com/spool_emoji"),
                ("two", "https://imgur.com/number_two"),
            ],
            matches,
        )

    # extract_markdown_links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Trying again with an [obvious link](https://www.google.com)"
        )
        self.assertListEqual([("obvious link", "https://www.google.com")], matches)

    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_links(
            "A [link](https://start.duckduckgo.com) and an ![image](https://imgur.com/blah)"
        )
        self.assertListEqual([("link", "https://start.duckduckgo.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This [string](https://www.google.com) has [two](https://start.duckduckgo.com) links!"
        )
        self.assertListEqual(
            [
                ("string", "https://www.google.com"),
                ("two", "https://start.duckduckgo.com"),
            ],
            matches,
        )
