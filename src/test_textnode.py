import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_not_eq_string(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("Yet another text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        link = TextNode("This is a link text node", TextType.LINK,
                        "http://pypi.org")
        link2 = TextNode("This is a link text node", TextType.LINK,
                         "http://pypi.org")
        self.assertEqual(link, link2)

    # Does this test actually do anything?
    def test_unneeded_url(self):
        node = TextNode("This is a text node", TextType.NORMAL,
                        None)
        self.assertTrue(node)

    def test_url_text_not_eq(self):
        link = TextNode("This is a link text node", TextType.LINK,
                        "http://pypi.org")
        link2 = TextNode("Yet another text node", TextType.LINK,
                         "http://pypi.org")
        self.assertNotEqual(link, link2)

    def test_url_link_not_eq(self):
        link = TextNode("This is a link text node", TextType.LINK,
                        "http://pypi.org")
        link2 = TextNode("This is a link text node", TextType.LINK,
                         "https://pypi.org")
        self.assertNotEqual(link, link2)


if __name__ == "__main__":
    unittest.main()
