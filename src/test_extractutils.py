import unittest

from extractutils import extract_markdown_images, extract_markdown_links


class TestUtils(unittest.TestCase):
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

    # markdown_to_html_node
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <<code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe**same** even with inline stuff\n</code></pre></div>",
        )
