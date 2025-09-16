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
