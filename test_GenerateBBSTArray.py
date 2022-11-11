import unittest
from GenerateBBSTArray import GenerateBBSTArray

class TestGenerateBBSTArray(unittest.TestCase):
    def testEmptyArray(self):
        array = []
        expectedBbstArray = None        
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)    

    def testSingleElementArray(self):
        array = [1]
        expectedBbstArray = [1]        
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

    def testTwoElementArray(self):
        array = [1, 2]
        expectedBbstArray = None
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

    def testFourElementArray(self):
        array = [1, 2, 3, 4]
        expectedBbstArray = None
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

    def testThreeElementArray(self):
        array = [1, 2, 3]
        expectedBbstArray = [2, 1, 3]        
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

    def testDepthTwoArray(self):
        array = [10, 14, 12, 18, 22, 20, 16]
        expectedBbstArray = [16, 12, 20, 10, 14, 18, 22]        
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

    def testDepthThreeArray(self):
        array = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        expectedBbstArray = [16, 12, 20, 10, 14, 18, 22, 9, 11, 13, 15, 17, 19, 21, 23]
        generatedBbstArray = GenerateBBSTArray(array)
        self.assertEqual(expectedBbstArray, generatedBbstArray)

                