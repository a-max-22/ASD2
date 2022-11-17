
import unittest

from Heap import Heap


def validateSubHeap(heap:Heap, elemIndex):
    if elemIndex is None: return True
    leftChildIndex = heap.GetLeftChildIndex(elemIndex)
    rightChildIndex = heap.GetRightChildIndex(elemIndex)
    arr = heap.HeapArray
    
    if leftChildIndex is not None and arr[elemIndex] < arr[leftChildIndex]: return False
    if rightChildIndex is not None and arr[elemIndex] < arr[rightChildIndex]: return False
    return validateSubHeap(heap, leftChildIndex) and validateSubHeap(heap, rightChildIndex)

#heap properties to test:
#   1) each node has at least two children
#   2) parent key is always greater than child
#   3) how to correctly handle heap resize? - make tests
def validateHeap(heap):
    array = heap.HeapArray
    index = 0
    return validateSubHeap(heap, 0)

def makeHeapFromArrayNoValidate(arr):
    heap = Heap()
    heap.HeapArray = arr
    for i in range(0, len(arr)):
        if arr[i] is None:
            heap.size = i
            break
        if i == len(arr)-1:
            heap.size = len(arr)
    return heap


class TestAdd(unittest.TestCase):
    def testAddToEmptyHeap(self):
        heap = makeHeapFromArrayNoValidate([None]*3)
        newItem = 1
        expectedHeapArray = [newItem, None, None]
        addResult = heap.Add(newItem)
        self.assertTrue(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))

    def testAddToOneItemHeap(self):
        heap = makeHeapFromArrayNoValidate([1]+[None]*2)
        newItem = 2
        expectedHeapArray = [newItem, 1, None]
        addResult = heap.Add(newItem)
        self.assertTrue(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))
       

    def testNoNeedToRebuildHeap(self):
        heapArray = [16, 8, 4, 7, 3, 2, None]
        heap = makeHeapFromArrayNoValidate(heapArray)
        newItem = 1
        expectedHeapArray = [16, 8, 4, 7, 3, 2, newItem]
        addResult = heap.Add(newItem)
        self.assertTrue(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))
    
    def testNeedToRebuildHeap(self):
        heapArray = [16, 8, 4, 7, 3, 2, None]
        heap = makeHeapFromArrayNoValidate(heapArray)
        newItem = 9
        expectedHeapArray = [16, 8, newItem, 7, 3, 2, 4]
        addResult = heap.Add(newItem)
        self.assertTrue(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))

    def testNeedToUpHeapMultipleTimes(self):
        heapArray = [16, 10, 12, 8, 7, 9, 11, 2, 3, 4, 5, 6, 7, None, None]
        heap = makeHeapFromArrayNoValidate(heapArray)
        newItem = 13
        expectedHeapArray =[16, 10, newItem, 8, 7, 9, 12, 2, 3, 4, 5, 6, 7, 11, None]
        addResult = heap.Add(newItem)
        self.assertTrue(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))

    def testHeapIsFull(self):
        heapArray = [16, 8, 4, 7, 3, 2, 1]
        heap = makeHeapFromArrayNoValidate(heapArray)
        newItem = 15
        expectedHeapArray = [16, 8, 4, 7, 3, 2, 1]
        addResult = heap.Add(newItem)
        self.assertFalse(addResult)
        self.assertEqual(heap.HeapArray, expectedHeapArray)
        self.assertTrue(validateHeap(heap))


class TestMakeHeap(unittest.TestCase):
    def testMakeHeapFromSingleElemArray(self):
        array = [1]
        exceptedArray = [1, None, None]
        heap = Heap()
        heap.MakeHeap(array, depth = 1)
        self.assertEqual(exceptedArray, heap.HeapArray)
        self.assertEqual(heap.size, len(array))
        self.assertTrue(validateHeap(heap))

    def testMakeHeapFromTwoElemArray(self):
        array = [1,2]
        exceptedArray = [2, 1, None]
        heap = Heap()
        heap.MakeHeap(array, depth = 1)
        self.assertEqual(exceptedArray, heap.HeapArray)
        self.assertEqual(heap.size, len(array))
        self.assertTrue(validateHeap(heap))

    def testMakeHeapFromThreeElemArray(self):
        array = [1,2,3]
        exceptedArray = [3, 1, 2]
        heap = Heap()
        heap.MakeHeap(array, depth = 1)
        self.assertEqual(exceptedArray, heap.HeapArray)
        self.assertEqual(heap.size, len(array))
        self.assertTrue(validateHeap(heap))
    
    def testArrayLengthExceedsDepth(self):
        array = [1,2,3,4]
        exceptedArray = []
        heap = Heap()
        result = heap.MakeHeap(array, depth = 1)
        self.assertEqual(result, None)
        self.assertEqual(exceptedArray, heap.HeapArray)
        self.assertEqual(heap.size, 0)
        self.assertTrue(validateHeap(heap))
    
    def testMakeHeapFromMultipleElemArray(self):
        array = [1, 8, 3, 4, 7, 2, 16]
        exceptedArray = [16, 7, 8, 1, 4, 2, 3] 
        heap = Heap()
        heap.MakeHeap(array, depth = 2)
        self.assertEqual(exceptedArray, heap.HeapArray)
        self.assertEqual(heap.size, len(array))
        self.assertTrue(validateHeap(heap))

class TestGetMax(unittest.TestCase):
    def testGetMaxFromEmptyUninitialized(self):
        heap = Heap()
        max = heap.GetMax()
        self.assertEqual(max, -1)
        self.assertEqual(heap.size, 0)
        self.assertEqual(heap.HeapArray, [])
        self.assertTrue(validateHeap(heap))

    def testGetMaxFromEmptyWithInitializedStorage(self):
        arr  = [None, None, None]
        heap = makeHeapFromArrayNoValidate(arr)
        max = heap.GetMax()
        self.assertEqual(max, -1)
        self.assertEqual(heap.size, 0)
        self.assertEqual(heap.HeapArray, [None, None, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxFromSingleElemHeap(self):
        heap = Heap()
        val = 1
        arr = [val]
        heap.MakeHeap(arr, depth = 1)
        max = heap.GetMax()
        self.assertEqual(max, val)
        self.assertEqual(heap.size, 0)
        self.assertEqual(heap.HeapArray, [None, None, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxTwoElemHeap(self):
        heap = Heap()
        arr = [1, 2]
        heap.MakeHeap(arr, depth = 1)
        max = heap.GetMax()
        self.assertEqual(max, 2)
        self.assertEqual(heap.size, 1)
        self.assertEqual(heap.HeapArray, [1, None, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxThreeElemHeap(self):
        heap = Heap()
        arr = [1, 2, 3]
        heap.MakeHeap(arr, depth = 1)
        max = heap.GetMax()
        self.assertEqual(max, 3)
        self.assertEqual(heap.size, 2)
        self.assertEqual(heap.HeapArray, [2, 1, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxFourElemHeap(self):
        heap = Heap()
        arr = [1, 2, 3, 4]
        heap.MakeHeap(arr, depth = 2)
        max = heap.GetMax()
        self.assertEqual(max, 4)
        self.assertEqual(heap.size, 3)
        self.assertEqual(heap.HeapArray, [3, 1, 2, None, None, None, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxMultilpleElemHeap(self):
        heap = Heap()
        arr = [16, 8, 4, 7, 3, 2]
        heap.MakeHeap(arr, depth = 2)
        max = heap.GetMax()
        self.assertEqual(max, 16)
        self.assertEqual(heap.size, len(arr)-1)
        self.assertEqual(heap.HeapArray, [8, 7, 4, 2, 3, None, None])
        self.assertTrue(validateHeap(heap))

    def testGetMaxMultipleTimes(self):
        heap = Heap()
        arr = [16, 10, 13, 8, 7, 9, 12, 2, 3, 4, 5, 6, 7, 11]
        heap.MakeHeap(arr, depth = 4)
        arr.sort(reverse=True)
        iterCount = 0
        for expectedMax in arr:
            iterCount += 1
            max = heap.GetMax()
            self.assertEqual(max, expectedMax)
            self.assertEqual(heap.size, len(arr)-iterCount)
            self.assertTrue(validateHeap(heap))
        
        max = heap.GetMax()
        self.assertEqual(max, -1)
        self.assertEqual(heap.size, 0)