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