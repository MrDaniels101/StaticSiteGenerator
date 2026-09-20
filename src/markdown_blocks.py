from enum import Enum
from htmlnode import ParentNode, HTMLNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    cleaned_block = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped != "":
            cleaned_block.append(stripped)
    return cleaned_block

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "######")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    parent = ParentNode("div", children)
    return parent

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_lists_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_lists_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def heading_to_html_node(block):
    hash_number = 0
    for i in block:
        if i == "#":
            hash_number += 1
        else:
            break
    text = block[hash_number + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{hash_number}", children)

def paragraph_to_html_node(block):
    paragraph_text = block.replace("\n", " ")
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        stripped_line = line.lstrip(">").strip()
        new_lines.append(stripped_line)
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def unordered_lists_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line.lstrip("- ")
        children = text_to_children(text)
        list_item = ParentNode("li", children)
        list_items.append(list_item)
    return ParentNode("ul", list_items)

def ordered_lists_to_html_node(block):
    lines = block.split("\n")
    item_lists = []
    for i, line in enumerate(lines):
        number_length = len(str(i + 1))
        prefix_length = number_length + 2
        text = line[prefix_length:]
        children = text_to_children(text)
        list_item = ParentNode("li", children)
        item_lists.append(list_item)
    return ParentNode("?", item_lists) 

def code_to_html_node(block):
    text = block[3:-3].strip()
    text_node = TextNode(text, TextType.text)
    children = text_node_to_html_node(text_node)
    code_item = ParentNode("code", [children])
    return code_item

    
