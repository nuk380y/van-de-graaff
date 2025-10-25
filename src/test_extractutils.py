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
