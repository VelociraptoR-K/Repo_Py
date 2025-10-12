import unittest
from GuessNumber import main, guess_number

class Guess(unittest.TestCase):
    # target попадает в диапазон
    def test_TargetEqual(self):
        self.assertEqual(guess_number(3,[1, 3, 5, 7, 11, 13, 17]),[3,2])

    # target не попадает в диапазон
    def test_TargetNotEqual(self):
        self.assertEqual(guess_number(9,[1, 3, 5, 7, 11, 13, 17]),[9,None])

    def test_EmptyList(self):
        self.assertEqual(guess_number(9,[]),'На вход подан пустой список')

    def test_OneList(self):
        self.assertEqual(guess_number(9,[9]),[9,1])

    def test_input_big_small(self):
        self.assertEqual(guess_number(32,[120,45,32,11]),[32,3])

    def test_FloatNotToInt(self):
        self.assertEqual(guess_number(32.65,[1,48,32,11,5,7]),'На вход подано нецелое число')

    def test_FloatToInt(self):
        self.assertEqual(guess_number(32.0,[120,45.8,32,11]),[32,3])

    def test_StringNotToInt(self):
        self.assertEqual(guess_number('five',[10,48,32.56,11,5,6,7]),'Данную строку нельзя преобразовать к int')

    def test_FromNegativeToPositive(self):
        self.assertEqual(guess_number(5,[-56,-123,-3,0,4,6,8,5,9]),[5,8])

    def test_BadRange(self):
        self.assertEqual(guess_number(5,'dhjshjd'),'На вход подан не список')

if __name__ == '__main__':
    unittest.main()