import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("Test text please ignore", TextType.PLAIN_TEXT)
        exp_repr = "TextNode(Test text please ignore, , None)"
        self.assertEqual(repr(node), exp_repr)


if __name__ == "__main__":
    unittest.main()
