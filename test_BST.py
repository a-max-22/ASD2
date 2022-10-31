
import unittest

from BST import BST, BSTFind, BSTNode

def makeChildNodes(parent: BSTNode, childrenLevelCount):
    if childrenLevelCount == 1: return 

    childKeyEvaluationDelta = 2 ** (childrenLevelCount-1)
    leftChildKey = parent.NodeKey - childKeyEvaluationDelta
    rightChildKey = parent.NodeKey + childKeyEvaluationDelta
    leftChild = BSTNode(key = leftChildKey, val = leftChildKey, parent = parent)
    rightChild = BSTNode(key = rightChildKey, val = rightChildKey, parent = parent)
    parent.LeftChild = leftChild
    parent.RightChild = rightChild
    makeChildNodes(leftChild, childrenLevelCount-1)
    makeChildNodes(rightChild, childrenLevelCount-1)

 
def makeFullBST(levelCount):
    basicValue = 2 ** (levelCount+1)
    rootNode = BSTNode(key = basicValue, val = basicValue, parent = None)
    makeChildNodes(rootNode, levelCount)
    return BST(rootNode)

def getBstNodes(bst:BST):
    nodesList = [bst.Root]
    currentNodeIndex = 0
    while currentNodeIndex < len(nodesList) :
        currentNode : BSTNode = nodesList[currentNodeIndex]
        if currentNode.LeftChild is not None: nodesList.append(currentNode.LeftChild)
        if currentNode.RightChild is not None: nodesList.append(currentNode.RightChild)
        currentNodeIndex += 1
    return nodesList

def getNodeByKey(nodesList, key):
    for node in nodesList:
        if node.NodeKey == key: return node

def printNodesListKeys(nodesList):
    print([x.NodeKey for x in nodesList ])


class TestFindNodeByKey(unittest.TestCase):
    def testFindInEmptyTree(self):
        bst = BST(node = None)
        soughtKey = 12
        result = bst.FindNodeByKey(soughtKey)
        self.assertEqual(result.Node, None)
        self.assertFalse(result.ToLeft)
        self.assertFalse(result.NodeHasKey)


    def testFindPresentNode(self):
        soughtKey = 12
        bst = makeFullBST(levelCount = 3)
        result = bst.FindNodeByKey(soughtKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, soughtKey)
        
        self.assertEqual(result.Node, expectedParentNode)
        self.assertFalse(result.ToLeft)
        self.assertTrue(result.NodeHasKey)

    def testFindAbsentNodePositionInLeftKeyLeafNode(self): 
        soughtKey = 9
        expectedParentKey = 10
        bst = makeFullBST(levelCount = 3)
        result = bst.FindNodeByKey(soughtKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, expectedParentKey)
        
        self.assertEqual(expectedParentKey, result.Node.NodeKey)
        self.assertEqual(result.Node, expectedParentNode)
        self.assertTrue(result.ToLeft)
        self.assertFalse(result.NodeHasKey)

    def testFindAbsentNodeInsertPositionInRightKey(self):
        soughtKey = 15
        expectedParentKey = 14
        bst = makeFullBST(levelCount = 3)
        result = bst.FindNodeByKey(soughtKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, expectedParentKey)

        self.assertEqual(expectedParentKey, result.Node.NodeKey)
        self.assertEqual(result.Node, expectedParentNode)
        self.assertFalse(result.ToLeft)
        self.assertFalse(result.NodeHasKey)


class TestAddKeyValue(unittest.TestCase):
    def testAddToEmptyTree(self):
        bst = BST(node = None)
        result =  bst.AddKeyValue(key = 16, val = 16)
        nodes = getBstNodes(bst)
        
        self.assertEqual(bst.Root, nodes[0])
        self.assertEqual(bst.Root.NodeKey, 16)
        self.assertEqual(bst.Root.NodeValue, 16)
        self.assertEqual(bst.Root.LeftChild, None)
        self.assertEqual(bst.Root.RightChild, None)
        self.assertTrue(result)

    def testAddPresentNode(self):
        soughtKey = 12
        bst = makeFullBST(levelCount = 3)
        result = bst.AddKeyValue(soughtKey, soughtKey)        
        self.assertFalse(result)

    def testAddNodeToLeft(self):
        addedKey = 9
        expectedParentKey = 10
        bst = makeFullBST(levelCount = 3)
        wasNAddedNodeAbsent = bst.AddKeyValue(key = addedKey, val = addedKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, expectedParentKey)
        expectedChildNode = getNodeByKey(nodes, addedKey)
        self.assertTrue(wasNAddedNodeAbsent)
        self.assertEqual(expectedChildNode.Parent, expectedParentNode)
        self.assertEqual(expectedParentNode.LeftChild, expectedChildNode)
        self.assertEqual(expectedParentNode.RightChild,  None)

    def testAddNodeToRight(self):
        addedKey = 15
        expectedParentKey = 14
        bst = makeFullBST(levelCount = 3)
        wasNAddedNodeAbsent = bst.AddKeyValue(key = addedKey, val = addedKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, expectedParentKey)
        expectedChildNode = getNodeByKey(nodes, addedKey)
        self.assertTrue(wasNAddedNodeAbsent)
        self.assertEqual(expectedChildNode.Parent, expectedParentNode)
        self.assertEqual(expectedParentNode.RightChild, expectedChildNode)
        self.assertEqual(expectedParentNode.LeftChild,  None)
    
    def testAddNodeToRootLeft(self):
        bst = makeFullBST(levelCount = 1)
        keyToAdd = bst.Root.NodeKey - 1
        addKeyResult = bst.AddKeyValue(key = keyToAdd, val = keyToAdd)
        nodes = getBstNodes(bst)
        addedNode = getNodeByKey(nodes, keyToAdd)
        self.assertEqual(bst.Root.LeftChild, addedNode)
        self.assertEqual(bst.Root.RightChild, None)
        self.assertTrue(addKeyResult)
    
    def testAddNodeToRootRight(self):
        bst = makeFullBST(levelCount = 1)
        keyToAdd = bst.Root.NodeKey + 1
        addKeyResult = bst.AddKeyValue(key = keyToAdd, val = keyToAdd)
        nodes = getBstNodes(bst)
        addedNode = getNodeByKey(nodes, keyToAdd)
        self.assertEqual(bst.Root.RightChild, addedNode)
        self.assertEqual(bst.Root.LeftChild, None)
        self.assertTrue(addKeyResult)
    

class TestFindMinMax(unittest.TestCase):
    def testFindMin(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 10
        actualMin = bst.FinMinMax(bst.Root, FindMax = False)
        self.assertEqual(expectedMin, actualMin.NodeValue)

    def testFindMax(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 22
        actualMax = bst.FinMinMax(bst.Root, FindMax = True)
        self.assertEqual(expectedMax, actualMax.NodeValue)

    def testFindMinSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 18
        subtreeNodeKey = 20
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMin = bst.FinMinMax(subtreeNode, FindMax = False)
        self.assertEqual(actualMin.NodeValue, expectedMin)

    def testFindMaxSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 14
        subtreeNodeKey = 12
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMax = bst.FinMinMax(subtreeNode, FindMax = True)
        self.assertEqual(actualMax.NodeValue, expectedMax)


class TestCount(unittest.TestCase):
    def testEmpty(self):
        bst = BST(None)
        count = bst.Count()
        self.assertEqual(count, 0)
    
    def testNonEmpty(self):
        levelCount = 3
        bst = makeFullBST(levelCount)
        count = bst.Count()
        self.assertEqual(count, 2**levelCount-1)


class TestDeleteNode(unittest.TestCase):
    def testDeleteLeftLeaf(self):
        bst = makeFullBST(levelCount = 3)
        keyToDel = 10
        parentKey = 12
        parentAnotherChildKey = 14
        nodes = getBstNodes(bst)
        deletedNode = getNodeByKey(nodes, keyToDel)
        deletedNodeParent = getNodeByKey(nodes, parentKey)
        parentAnotherChild = getNodeByKey(nodes, parentAnotherChildKey)
        delResult = bst.DeleteNodeByKey(keyToDel)
        self.assertTrue(deletedNodeParent.LeftChild is None)
        self.assertEqual(deletedNodeParent.RightChild, parentAnotherChild) 
        self.assertTrue(delResult)

    def testDeleteRightLeaf(self):
        bst = makeFullBST(levelCount = 3)
        keyToDel = 14
        parentKey = 12
        parentAnotherChildKey = 10
        nodes = getBstNodes(bst)
        deletedNode = getNodeByKey(nodes, keyToDel)
        deletedNodeParent = getNodeByKey(nodes, parentKey)
        parentAnotherChild = getNodeByKey(nodes, parentAnotherChildKey)
        delResult = bst.DeleteNodeByKey(keyToDel)
        self.assertEqual(deletedNodeParent.LeftChild, parentAnotherChild)
        self.assertTrue(deletedNodeParent.RightChild is None) 
        self.assertTrue(delResult)
    
    def testDeleteNonLeafNodeRightChild(self):
        bst = makeFullBST(levelCount = 4)
        keyToDel = 40
        parentKey = 32
        replacementKey = 42
        deletedNodeRightChildKey = 44
        deletedNodeLeftChildKey = 36
        nodes = getBstNodes(bst)
        deletedNodeParent = getNodeByKey(nodes, parentKey)
        replacementNode = getNodeByKey(nodes, replacementKey)
        deletedNodeRightChild = getNodeByKey(nodes, deletedNodeRightChildKey)
        deletedNodeLeftChild = getNodeByKey(nodes, deletedNodeLeftChildKey)

        delResult = bst.DeleteNodeByKey(keyToDel)

        self.assertEqual(deletedNodeParent.RightChild, replacementNode)
        self.assertEqual(replacementNode.RightChild, deletedNodeRightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertTrue(delResult)

    def testDeleteNonLeafNodeLeftChild(self):
        bst = makeFullBST(levelCount = 4)
        keyToDel = 24
        parentKey = 32
        replacementKey = 26
        deletedNodeRightChildKey = 28
        deletedNodeLeftChildKey = 20
        nodes = getBstNodes(bst)
        deletedNodeParent = getNodeByKey(nodes, parentKey)
        replacementNode = getNodeByKey(nodes, replacementKey)
        deletedNodeRightChild = getNodeByKey(nodes, deletedNodeRightChildKey)
        deletedNodeLeftChild = getNodeByKey(nodes, deletedNodeLeftChildKey)

        delResult = bst.DeleteNodeByKey(keyToDel)

        self.assertEqual(deletedNodeParent.LeftChild, replacementNode)
        self.assertEqual(replacementNode.RightChild, deletedNodeRightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertTrue(delResult)

    def testDeleteRootNode(self):
        bst = makeFullBST(levelCount = 3)
        replacementKey = 18
        deletedNodeRightChildKey = 20
        deletedNodeLeftChildKey = 12
        nodes = getBstNodes(bst)

        deletedNodeParent = None
        replacementNode = getNodeByKey(nodes, replacementKey)
        deletedNodeRightChild = getNodeByKey(nodes, deletedNodeRightChildKey)
        deletedNodeLeftChild = getNodeByKey(nodes, deletedNodeLeftChildKey)
        deletedNode = bst.Root

        delResult = bst.DeleteNodeByKey(bst.Root.NodeKey)
        self.assertEqual(replacementNode.Parent, deletedNodeParent)
        self.assertEqual(replacementNode.RightChild, deletedNodeRightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertTrue(delResult)
    
    def testDeleteLastNode(self):
        bst = makeFullBST(levelCount = 1)
        keyToDel = bst.Root.NodeKey
        delResult = bst.DeleteNodeByKey(keyToDel)
        self.assertEqual(bst.Root, None)
        self.assertTrue(delResult)
