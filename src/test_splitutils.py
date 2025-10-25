import unittest

from splitutils import split_nodes_delimiter, split_nodes_image, split_nodes_link
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

    def test_split_nodes_delimiter_leading_blank(self):
        node = TextNode(
            "**MarkDown** formatting at the front should be the first new node.",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertListEqual(
            [
                TextNode("MarkDown", TextType.BOLD_TEXT),
                TextNode(
                    " formatting at the front should be the first new node.",
                    TextType.PLAIN_TEXT,
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_trailing_blank(self):
        node = TextNode(
            "MarkDown formatting at the front should be the first new _node._",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC_TEXT)
        self.assertListEqual(
            [
                TextNode(
                    "MarkDown formatting at the front should be the first new ",
                    TextType.PLAIN_TEXT,
                ),
                TextNode("node.", TextType.ITALIC_TEXT),
            ],
            new_nodes,
        )

    # split_nodes_image
    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode(
                    "image", TextType.IMAGE_TEXT, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE_TEXT,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_images_with_no_target(self):
        node = TextNode(
            "There is no image formatted text in this string.",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "There is no image formatted text in this string.",
                    TextType.PLAIN_TEXT,
                )
            ],
            new_nodes,
        )

    def test_split_nodes_images_at_start(self):
        node = TextNode(
            "![fancy bullet](https://i.imgur.com/not_real.png) bullet point",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(
                    "fancy bullet",
                    TextType.IMAGE_TEXT,
                    "https://i.imgur.com/not_real.png",
                ),
                TextNode(" bullet point", TextType.PLAIN_TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_images_at_end(self):
        node = TextNode(
            "Ending ![image](https://i.imgur.com/not_real.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Ending ", TextType.PLAIN_TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE_TEXT,
                    "https://i.imgur.com/not_real.png",
                ),
            ],
            new_nodes,
        )

    # split_nodes_link
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://start.duckduckgo.com)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://www.google.com"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second link",
                    TextType.LINK_TEXT,
                    "https://start.duckduckgo.com",
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_links_with_no_target(self):
        node = TextNode(
            "There is no link formatted text in this string.",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "There is no link formatted text in this string.",
                    TextType.PLAIN_TEXT,
                )
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
