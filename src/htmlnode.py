from textnode import TextNode, TextType
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        if not value and not children:
            raise ValueError("HTMLNode must have either a value or children")
        
    def to_html(self):
        raise NotImplementedError("Subclasses must implement to_html method")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if value is None:
            raise ValueError("LeafNode must have a value")
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        if not self.tag:
            return self.value
        
        if self.props:
            return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        if not children:
            raise ValueError("ParentNode must have children")
        
    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        
        if not self.children:
            raise ValueError("ParentNode must have children")
        
        children_html = "".join(child.to_html() for child in self.children)
        
        if self.props:
            return f'<{self.tag} {self.props_to_html()}>{children_html}</{self.tag}>'
        return f'<{self.tag}>{children_html}</{self.tag}>'
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("URL must be provided for link text type")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("URL must be provided for image text type")
            return LeafNode(tag="img", value=None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.type}")
        
