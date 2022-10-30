
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


class TestFindMinMax(unittest.TestCase):
    def testFindMin(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 10
        actualMin = bst.FinMinMax(bst.Root, FindMax = False)
        self.assertEqual(expectedMin, actualMin)

    def testFindMax(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 22
        expectedMax = bst.FinMinMax(bst.Root, FindMax = True)
        self.assertEqual(expectedMax, expectedMax)

    def testFindMinSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 18
        subtreeNodeKey = 20
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMin = bst.FinMinMax(subtreeNode, FindMax = False)
        self.assertEqual(actualMin, expectedMin)

    def testFindMaxSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 14
        subtreeNodeKey = 12
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMax = bst.FinMinMax(subtreeNode, FindMax = True)
        self.assertEqual(actualMax, expectedMax)


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
        keyToDel = 16
        replacementKey = 18
        deletedNodeRightChildKey = 20
        deletedNodeLeftChildKey = 12
        nodes = getBstNodes(bst)

        deletedNodeParent = None
        replacementNode = getNodeByKey(nodes, replacementKey)
        deletedNodeRightChild = getNodeByKey(nodes, deletedNodeRightChildKey)
        deletedNodeLeftChild = getNodeByKey(nodes, deletedNodeLeftChildKey)

        delResult = bst.DeleteNodeByKey(keyToDel)

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

