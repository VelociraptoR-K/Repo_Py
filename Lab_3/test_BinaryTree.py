import unittest
from BinaryTree import gen_bin_tree, gen_bin_tree_tuple

class Test(unittest.TestCase):
    def test_gen_bin_tree(self):
        self.assertEqual(gen_bin_tree(2,5), {5: [{7: [{9: []}, {21: []}]}, {15: [{17: []}, {45: []}]}]})

    def test_gen_bin_tree_tuple(self):
        self.assertEqual(gen_bin_tree_tuple(4,3), (3, [(5, [(7, [(9, [(11, []), (27, [])]), (21, [(23, []), (63, [])])]), (15, [(17, [(19, []), (51, [])]), (45, [(47, []), (135, [])])])]), (9, [(11, [(13, [(15, []), (39, [])]), (33, [(35, []), (99, [])])]), (27, [(29, [(31, []), (87, [])]), (81, [(83, []), (243, [])])])])]))

    def test_Height(self):
        self.assertEqual(gen_bin_tree(-2,5),'Вершина дерева должна быть >= 0')

if __name__ == '__main__':
    unittest.main()
