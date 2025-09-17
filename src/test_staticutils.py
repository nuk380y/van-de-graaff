import unittest

# from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from staticutils import split_nodes_delimiter
from textnode import TextNode, TextType


class TestUtils(unittest.TestCase):
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
