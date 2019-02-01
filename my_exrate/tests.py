from django.test import TestCase
import unittest
from my_exrate.views import test_fn1


# Create your tests here.
class Tests(unittest.TestCase):
    def test_1(self):
        result = test_fn1([4, 8, 12, 16], 2)
        print(result)
        self.assertTrue(result == [2.0, 4.0, 6.0, 8.0])

    def test_2(self):
        result = test_fn1([3, 9, 12, 15], 3)
        print(result)
        self.assertTrue(result == [1.0, 3.0, 4.0, 5.0])
