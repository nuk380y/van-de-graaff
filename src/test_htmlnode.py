import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is only a test", None, {"color": "ffffff"})
        expected_repr = (
            f"HTMLNode(\"p\", \"This is only a test\", None, {{'color': 'ffffff'}})"
        )
        self.assertEqual(f"{node}", f"{expected_repr}")

    def test_to_html(self):
        node = HTMLNode("p", "This is only a test", None)
        expected_repr = f'HTMLNode("p", "This is only a test", None, None)'
        self.assertEqual(f"{node}", f"{expected_repr}")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        attribs = {"href": "https://pypi.org", "rel": "noopener nofollower"}
        node = HTMLNode("a", "Example link", None, attribs)
        expected_props = f' href="https://pypi.org" rel="noopener nofollower"'
        self.assertEqual(f"{node.props_to_html()}", f"{expected_props}")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>",
        )

    def test_leaf_to_html_a(self):
        attribs = {"href": "https://pypi.org"}
        node = LeafNode("a", "Python Package Index", attribs)
        self.assertEqual(
            node.to_html(),
            '<a href="https://pypi.org">Python Package Index</a>',
        )

    def test_leaf_to_html_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
