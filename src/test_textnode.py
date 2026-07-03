import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_text(self):
        node1 = TextNode("hello", TextType.BOLD)
        node2 = TextNode("goodbye", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_text_type(self):
        node1 = TextNode("hello", TextType.BOLD)
        node2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_equal_url(self):
        node1 = TextNode("click here", TextType.LINK, "https://a.com")
        node2 = TextNode("click here", TextType.LINK, "https://b.com")
        self.assertNotEqual(node1, node2)

    def test_equal_url_none(self):
        node1 = TextNode("plain text", TextType.TEXT, None)
        node2 = TextNode("plain text", TextType.TEXT, None)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()