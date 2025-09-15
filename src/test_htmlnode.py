import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParantNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
