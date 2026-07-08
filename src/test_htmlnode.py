import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_none(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_empty_dict(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(props={"id": "main"})
        result = node.props_to_html()
        self.assertEqual(result, ' id="main"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_a(self):
        node = LeafNode("a", "some text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<a class="highlight">some text</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "just raw text")
        self.assertEqual(node.to_html(), "just raw text")

class TestParentNode(unittest.TestCase):
    def test_parentnode_init(self):
        child = LeafNode(None, "hello")
        node = ParentNode("div", [child], {"class": "main"})

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [child])
        self.assertEqual(node.props, {"class": "main"})

    def test_to_html_with_one_child(self):
        child = LeafNode("span", "child")
        node = ParentNode("div", [child])

        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " plain "),
                LeafNode("i", "italic"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b> plain <i>italic</i></p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        node = ParentNode("div", [child])

        self.assertEqual(
            node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode(None, "hello")],
            {"class": "main"},
        )

        self.assertEqual(
            node.to_html(),
            '<div class="main">hello</div>',
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode(None, "x")])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()