from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if text_type == TextType.LINK and url is None:
            raise ValueError("URL must be provided for link text type")
    
    def __eq__(self, value):
        return value.text == self.text and value.text_type == self.text_type and value.url == self.url
    
    def __repr__(self):
        match self.text_type:
            case TextType.NORMAL:
                return f"TextNode({self.text}, {self.text_type.value})"
            case TextType.BOLD:
                return f"TextNode(**{self.text}**, {self.text_type.value})"
            case TextType.ITALIC:
                return f"TextNode(*{self.text}*, {self.text_type.value})"
            case TextType.CODE:
                return f"TextNode(`{self.text}`, {self.text_type.value})"
            case TextType.LINK:
                if not self.url:
                    raise ValueError("URL must be provided for link text type")
                return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
            case TextType.IMAGE:
                if not self.url:
                    raise ValueError("URL must be provided for image text type")
                return f"TextNode![{self.text}]({self.url}, {self.text_type.value})"
        return f"TextNode({self.text}, {self.text_type.value})"