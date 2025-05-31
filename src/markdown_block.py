from enum import Enum
import re
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode
from markdown import markdown_to_blocks, text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """
    Convert a block of text to a BlockType.
    This function is used to determine the type of block based on its content.
    """
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d+\. ", line) for line in block.splitlines()):
        # Check if all lines start with a number followed by a dot and space
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    """
    Convert a markdown block to an HTMLNode.
    This function is used to convert a markdown block to an HTMLNode for rendering.
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
       
    return ParentNode(tag="div", children=children)

def block_to_html_node(block):
    """
    Convert a markdown block to an HTMLNode.
    This function is used to convert a markdown block to an HTMLNode for rendering.
    """
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
    raise ValueError(f"Unknown block type: {block_type}")


def text_to_children(text):
    """
    Convert a text string to a list of HTMLNode children.
    This function is used to convert the text content of a node into a list of HTMLNode children.
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    tag = f"h{level}"
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(tag=tag, children=children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Code block must start and end with ```")
    code_content = block[3:-3].lstrip()
    text_node = TextNode(code_content, TextType.TEXT)
    child = text_node_to_html_node(text_node)
    code = ParentNode(tag="code", children=[child])
    return ParentNode(tag="pre", children=[code])

def olist_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        text = item.split(". ", 1)[1] if ". " in item else item[2:]
        children.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ol", children=children)

def ulist_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        text = item[2:]  # Skip the "- " at the start
        children.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ul", children=children)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Quote block must start with '>'")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode(tag="blockquote", children=children)