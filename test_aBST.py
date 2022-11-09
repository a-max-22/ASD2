import unittest
from aBST import aBST

def make2DepthABST():
    result = aBST(depth = 2)
    result.Tree = [2, 1, 3]    
    return result    

def make3DepthABST():
    result = aBST(depth = 3)
    result.Tree = [8, 6, 5, 7, 10, 9, 11]    
    return result

def make4DepthABST():
    result = aBST(depth = 4)
    result.Tree = [16, 12, 20, 10, 14, 18, 22, 9, 11, 13, 15, 17, 19, 21, 23]
    return result

def make4DepthNoLeftSubtree():
    result = aBST(depth = 4)
    result.Tree = [16, None, 20, None, None, 18, 22, None, None, None, None, 17, 19, 21, 23]
    return result


def verifyTree(aBst:aBST):
    for index in range(0, len(aBst.Tree)):
        currentKey = aBst.Tree[index]
        if currentKey is None: 
            continue
        
        if 2 * index + 1 >= len(aBst.Tree): continue
        if 2 * index + 2 >= len(aBst.Tree): return False

        leftKey = aBst.Tree[2 * index + 1] if aBst.Tree[2 * index + 1] is not None else currentKey - 1
        rightKey = aBst.Tree[2 * index + 2] if aBst.Tree[2 * index + 2] is not None else currentKey + 1
        if leftKey < currentKey < rightKey:
            continue
        else:
            return False
    return True

class TestFindKeyIndex(unittest.TestCase):
    def testFindInEmptyTreeNoPlaceToInsert(self):
        abst = aBST(depth = 0)
        index = abst.FindKeyIndex(key = 0)
        self.assertEqual(index, None)
    
    def testFindInSingleElementEmptyTree(self):
        abst = aBST(depth = 1)
        index = abst.FindKeyIndex(key = 0)
        self.assertEqual(index, 0)

    def testFindInSingleElementFullTree(self):
        abst = aBST(depth = 1)
        keyToFind = 0
        abst.Tree = [keyToFind]
        index = abst.FindKeyIndex(key = keyToFind)
        self.assertEqual(index, 0)
    
    def testFindAbsentElementLeft(self):
        key = 0
        abst  = make4DepthABST()
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, None)

    def testFindAbsentElementRight(self):
        key = 50
        abst  = make4DepthABST()
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, None)

    def testFindPresentElementNonLeaf(self):
        key = 18
        abst  = make4DepthABST()
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, 5)

    
    def testFindPresentElementLeaf(self):
        key = 21
        abst  = make4DepthABST()
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, 13)
    
    def testFindAbsentElementNonLeaf(self):
        key = 18
        abst  = make4DepthABST()
        keyIndex = abst.Tree.index(key) 
        abst.Tree[keyIndex] = None
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, -keyIndex)

    def testFindAbsentElementLeaf(self):
        key = 23
        abst  = make4DepthABST()
        keyIndex = abst.Tree.index(key) 
        abst.Tree[keyIndex] = None
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, -keyIndex)

    def testFindAbsentElementLeafSubTree(self):
        key = 12
        abst  = make4DepthABST()
        keyIndex = abst.Tree.index(key) 
        abst.Tree[keyIndex] = None
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, keyIndex)

    def testFindAbsentElementLeafSubTree(self):
        key = 12
        abst  = make4DepthABST()
        keyIndex = abst.Tree.index(key) 
        abst.Tree[keyIndex] = None
        index = abst.FindKeyIndex(key)
        self.assertEqual(index, -keyIndex)

    def testFindAbsentElementNoSuitablePlaceToInsert(self):
        keyToDel = 17
        keyToFind = 50
        abst  = make4DepthABST()
        keyToDelIndex = abst.Tree.index(keyToDel) 
        abst.Tree[keyToDelIndex] = None
        index = abst.FindKeyIndex(keyToFind)
        self.assertEqual(index, None)
        self.assertTrue(verifyTree(abst))


class TestAddKey(unittest.TestCase):
    def testInsertIntoEmptyTreeNoPlace(self):
        abst = aBST(depth = 0)
        index = abst.AddKey(key = 0)
        self.assertEqual(index, -1)
        self.assertEqual([], abst.Tree)
        self.assertTrue(verifyTree(abst))

    def testInsertRoot(self):
        abst = aBST(depth = 1)
        newKey = 0
        index = abst.AddKey(key = newKey)
        self.assertEqual(index, 0)
        self.assertEqual([newKey], abst.Tree)
        self.assertTrue(verifyTree(abst))


    def testInsertRootMultipleNodes(self):
        abst = aBST(depth = 3)
        newKey = 0
        index = abst.AddKey(key = newKey)
        self.assertEqual(index, 0)
        self.assertEqual([newKey] + [None] * (len(abst.Tree) - 1), abst.Tree)
        self.assertTrue(verifyTree(abst))
    
    def testInsertRootPresentNode(self):
        abst = make2DepthABST()
        keyToInsert = abst.Tree[0]
        oldNodesList  = abst.Tree.copy()
        index = abst.AddKey(key = keyToInsert)
        self.assertEqual(index, 0)
        self.assertEqual(oldNodesList, abst.Tree)
        self.assertTrue(verifyTree(abst))
    
    def testInsertPresentNodeNonLeaf(self):
        key = 18
        abst  = make4DepthABST()
        index = abst.AddKey(key)
        oldNodesList  = abst.Tree.copy()
        self.assertEqual(index, 5)
        self.assertEqual(oldNodesList, abst.Tree)
        self.assertTrue(verifyTree(abst))

    def testInsertPresentNodeLeaf(self):
        key = 23
        abst  = make4DepthABST()
        index = abst.AddKey(key)
        oldNodesList  = abst.Tree.copy()
        self.assertEqual(index, 14)
        self.assertEqual(oldNodesList, abst.Tree)
        self.assertTrue(verifyTree(abst))
    
    def testInsertAbsentLeftSubtree(self):
        key = 12
        abst  = make4DepthNoLeftSubtree()        
        index = abst.AddKey(key)
        self.assertEqual(index, 1)
        self.assertTrue(verifyTree(abst))
        self.assertEqual( [16, key, 20, None, None, 18, 22, None, None, None, None, 17, 19, 21, 23], abst.Tree)

    def testInsertAbsentNodeLeadf(self):
        keyToDel = 23
        abst  = make4DepthABST()
        keyIndex = abst.Tree.index(keyToDel) 
        abst.Tree[keyIndex] = None
        
        keyToInsert  = 50
        index = abst.AddKey(keyToInsert)
        
        self.assertEqual(index, 14)
        self.assertTrue(verifyTree(abst))
        self.assertEqual([16, 12, 20, 10, 14, 18, 22, 9, 11, 13, 15, 17, 19, 21, keyToInsert], abst.Tree)

    def testInsertIntoFullTree(self):
        abst = make4DepthABST()
        treeBeforeInsertion = abst.Tree.copy()
        keyToInsert = abst.Tree[-1] + 1
        index = abst.AddKey(keyToInsert)
        self.assertEqual(index, -1)
        self.assertTrue(verifyTree(abst))
        self.assertEqual(treeBeforeInsertion, abst.Tree)