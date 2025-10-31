import unittest
from BinaryTree import gen_bin_tree, gen_bin_tree_tuple

class Test(unittest.TestCase):
    def test_gen_bin_tree(self):
        self.assertEqual(gen_bin_tree(2,5), {5: [{7: [{9: []}, {21: []}]}, {15: [{17: []}, {45: []}]}]})

    def test_gen_bin_tree_tuple(self):
        self.assertEqual(gen_bin_tree_tuple(1,3), f'(3: [(5: []), (9: [])])')

    def test_Height(self):
        self.assertEqual(gen_bin_tree(-2,5),'Вершина дерева должна быть >= 0')

if __name__ == '__main__':
    unittest.main()

