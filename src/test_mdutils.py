import unittest

# from mdutils import markdown_to_blocks, markdown_to_html_node, text_to_textnodes
from mdutils import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestUtils(unittest.TestCase):
    # text_to_textnodes
    def test_text_to_textnodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word, a `code block`, an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), and a [link](https://boot.dev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN_TEXT),
                TextNode("text", TextType.BOLD_TEXT),
                TextNode(" with an ", TextType.PLAIN_TEXT),
                TextNode("italic", TextType.ITALIC_TEXT),
                TextNode(" word, a ", TextType.PLAIN_TEXT),
                TextNode("code block", TextType.CODE_TEXT),
                TextNode(", an ", TextType.PLAIN_TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE_TEXT,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(", and a ", TextType.PLAIN_TEXT),
                TextNode("link", TextType.LINK_TEXT, "https://boot.dev"),
            ],
            new_nodes,
        )

    # markdown_to_blocks
    def test_markdown_to_blocks(self):
        md = """
This is a **bolded** paragraph.

This is another paragraph with _italic_ text and `code` here.
This is the same paragraph on a new line.

- This is a list
- with items.
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph.",
                "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line.",
                "- This is a list\n- with items.",
            ],
        )

    def test_markdown_to_blocks_with_even_newlines(self):
        md = """
This is a paragraph.


This is another paragraph after two blank lines.
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph after two blank lines.",
            ],
        )

    def test_markdown_to_blocks_with_odd_newlines(self):
        md = """
This is a paragraph.





This is another paragraph after five blank lines.
        """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph after five blank lines.",
            ],
        )

    # block_to_block_type
    def test_block_to_block_type_basic_presentations(self):
        md = """
# First heading

Paragraph leading to code:

```py
def code_block():
    pass
```

> Robert Morris had a cool quote about something.
        """

        id_blocks = block_to_block_type(md)
        self.assertEqual(
            id_blocks,
            [
                TextNode("# First heading", BlockType.HEADING),
                TextNode("Paragraph leading to code:", BlockType.PARAGRAPH),
                TextNode("```py\ndef code_block():\n    pass\n```", BlockType.CODE),
                TextNode(
                    "> Robert Morris had a cool quote about something.", BlockType.QUOTE
                ),
            ],
        )

    def test_block_to_block_type_lists(self):
        md = """
# First heading

1. First bullet
2. Second bullet
3. Third...

- bullet point
- bullet point

* bullet point
* bullet point
        """

        id_blocks = block_to_block_type(md)
        self.assertEqual(
            id_blocks,
            [
                TextNode("# First heading", BlockType.HEADING),
                TextNode(
                    "1. First bullet\n2. Second bullet\n3. Third...",
                    BlockType.ORDERED_LIST,
                ),
                TextNode("- bullet point\n- bullet point", BlockType.UNORDERED_LIST),
                TextNode("* bullet point\n* bullet point", BlockType.UNORDERED_LIST),
            ],
        )


#     # markdown_to_html_node
#     def test_markdown_to_html_node_paragraph(self):
#         md = """
# This is **bolded** paragraph
# text in a p
# tag here
#
# This is another paragraph with _italic_ text and `code` here
#
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <<code>code</code> here</p></div>",
#         )
#
#     def test_markdown_to_html_node_codeblock(self):
#         md = """
# ```
# This is text that _should_ remain
# the **same** even with inline stuff
# ```
# """
#
#         node = markdown_to_html_node(md)
#         html = node.to_html()
#         self.assertEqual(
#             html,
#             "<div><pre><code>This is text that _should_ remain\nthe**same** even with inline stuff\n</code></pre></div>",
#         )
#
