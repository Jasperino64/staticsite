import unittest
from htmlnode import HTMLNode
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