import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_initialization_with_children(self):
        child1 = LeafNode(tag='p', value='Child 1')
        child2 = LeafNode(tag='p', value='Child 2')
        parent = ParentNode(tag='div', children=[child1, child2])
        self.assertEqual(parent.tag, 'div')
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, 'Child 1')
        self.assertEqual(parent.children[1].value, 'Child 2')

    def test_to_html_with_children(self):
        child = LeafNode(tag='span', value='Child Node')
        parent = ParentNode(tag='div', children=[child])
        expected_html = '<div><span>Child Node</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_without_children(self):
        with self.assertRaises(ValueError):
            parent = ParentNode(tag='div', children=[])