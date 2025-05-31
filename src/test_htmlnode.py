import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization_with_tag_and_value(self):
        node = HTMLNode(tag='p', value='Hello, World!')
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'Hello, World!')

    def test_initialization_with_children(self):
        child_node = HTMLNode(tag='span', value='Child Node')
        node = HTMLNode(tag='div', children=[child_node])
        self.assertEqual(node.tag, 'div')
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, 'span')

    def test_initialization_with_props(self):
        props = {'class': 'my-class', 'id': 'my-id'}
        node = HTMLNode(tag='div', value="hi", props=props)
        props_html = node.props_to_html()
        self.assertEqual('class="my-class" id="my-id"', props_html)

    def test_initialization_without_value_or_children(self):
        with self.assertRaises(ValueError):
            HTMLNode(tag='div')

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD)  # Simulating a bold text node
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'Bold Text')
        self.assertEqual(html_node.to_html(), '<b>Bold Text</b>')

    def test_img_node_to_html_node(self):
        text_node = TextNode("image", TextType.IMAGE, url="image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {'alt': 'image', 'src': 'image.png'})