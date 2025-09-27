import unittest
from SumOfTwo import sum_two
class Tests(unittest.TestCase):

    def test_EmptyList(self):
        self.assertEqual(sum_two([],9),'Подан пустой список')

    def test_TypeList_1(self):
        self.assertEqual(sum_two([2,5,3.785,7], 7), 'В списке есть нецелочисленное значение')

    def test_TypeList_2(self):
        self.assertEqual(sum_two('qwsx', 5),'На вход подан не список')

    def test_type_target_float(self):
        self.assertEqual(sum_two([1,2], 9.76), 'Переменная target дробная, а должна быть целочисленной')

    def test_type_target_string(self):
        self.assertEqual(sum_two([1,2], '9.76'), 'Переменная target строковая, а должна быть целочисленной')

    def test_NegativeValue(self):
        self.assertEqual(sum_two([2,5,1,-3], 2),[1,3])

    def test_SameValues(self):
        self.assertEqual(sum_two([4,4,4,4], 8),[0,1])

    def test_Equal(self):
        self.assertEqual(sum_two([2,7,11,15], 9),[0,1])

    def test_Is_In(self):
        self.assertEqual(sum_two([2,7,11,15], 99),'В списке не нашлось нужной комбинации')

if __name__ == '__main__':

    unittest.main()
