from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
        else:
            if len(parts) % 2 == 0:
                # If the number of parts is even, it means the last part is normal text
                raise ValueError("invalid markdown, nmatched delimiter")
            for i in range(len(parts)):
                if parts[i] == "":
                    # Skip empty parts
                    continue
                if i % 2 == 0:
                    # Even index: normal text
                    new_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    # Odd index: styled text
                    new_nodes.append(TextNode(parts[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        current_text = node.text
        for match in matches:
            parts = current_text.split(f"![{match[0]}]({match[1]})", 1)
            if parts[0] != "":
                # If there's text before the image, add it as a text node
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            current_text = parts[1] if len(parts) > 1 else None
        
        if current_text:
            # If there's any text left after the last image, add it as a text node
            new_nodes.append(TextNode(current_text, TextType.TEXT))       
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        first = True
        current_text = node.text
        for match in matches:
            parts = current_text.split(f"[{match[0]}]({match[1]})", 1)
            if parts[0] != "":
                # If there's text before the link, add it as a text node
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            current_text = parts[1] if len(parts) > 1 else None
        
        if current_text:
            # If there's any text left after the last link, add it as a text node
            new_nodes.append(TextNode(current_text, TextType.TEXT))       
    return new_nodes

def text_to_textnodes(text):
    """
    Convert a text string to a list of TextNode objects.
    This function is used to convert the text content of a node into a list of TextNode objects.
    """
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def extract_title(markdown):
    """
    Extract the title from the markdown content.
    The title is assumed to be the first heading in the markdown.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()  # Remove the leading '# ' and any whitespace
        
    raise ValueError("No title found in markdown content")
    