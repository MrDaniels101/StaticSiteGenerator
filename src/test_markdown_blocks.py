import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
    This is block 1


    This is block 2    

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
             blocks,
             [
                  "This is block 1",
                  "This is block 2",
             ],
        )

    def test_markdown_to_blocks_whitespace(self):
        md = """   This is a block with leading and trailing space   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
             blocks,
             [
                  "This is a block with leading and trailing space",
             ],
        )

    def test_heading(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()