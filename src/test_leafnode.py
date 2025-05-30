import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_initialization_with_props(self):
        props = {'class': 'my-class', 'id': 'my-id'}
        node = LeafNode(tag='div', value="hi", props=props)
        props_html = node.props_to_html()
        self.assertEqual('class="my-class" id="my-id"', props_html)
        self.assertEqual(node.to_html(), '<div class="my-class" id="my-id">hi</div>')

    def test_to_html(self):
        node = LeafNode(tag='p', value='Hello, World!')
        expected_html = '<p>Hello, World!</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_value_none_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag='div', value=None)
    
    def test_to_html_without_tag(self):
        node = LeafNode(tag=None, value='Just text')
        expected_html = 'Just text'
        self.assertEqual(node.to_html(), expected_html)