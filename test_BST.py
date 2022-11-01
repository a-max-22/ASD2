
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
    if bst.Root is None: return []
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

def printNode(node):
    print(node.NodeKey, node.NodeValue, node.LeftChild.NodeKey if node.LeftChild is not None else None , node.RightChild.NodeKey if node.RightChild is not None else None)


def visitBstNode(node):
    if node is None: return []
    return visitBstNode(node.LeftChild) + [node] + visitBstNode(node.RightChild) 

def getBstNodesAscending(bst):
    nodesLitsAscending = visitBstNode(bst.Root)
    return nodesLitsAscending

def verifyBST(bst): 
    nodes = getBstNodesAscending(bst)
    if nodes == [] and bst.Root is None: return True

    nodesKeys = [x.NodeKey for x in nodes]
    if not sorted(nodesKeys): return False
    rootAlreadyWasInNodesList = False
    for node in nodes:
        if node.LeftChild is not None and not( node.LeftChild.NodeKey < node.NodeKey):
            print("l")
            return False
        if node.RightChild is not None and not( node.RightChild.NodeKey > node.NodeKey): 
            print("r")
            return False

        if node.Parent is None and rootAlreadyWasInNodesList: 
            print("Two roots")
            return False
            
        if node.Parent is None: rootAlreadyWasInNodesList = True
        parent = node.Parent
        if parent is not None:
            if parent.LeftChild != node and parent.RightChild != node: 
                print("Error, node parent has wrong children: parent, node")
                printNode(parent)
                printNode(node)
                return False
    return True

class TestFindNodeByKey(unittest.TestCase):
    def testFindInEmptyTree(self):
        bst = BST(node = None)
        soughtKey = 12
        result = bst.FindNodeByKey(soughtKey)
        self.assertEqual(result.Node, None)
        self.assertFalse(result.ToLeft)
        self.assertFalse(result.NodeHasKey)
        self.assertTrue(verifyBST(bst))

    def testFindPresentNodeInSingleElementTree(self):
        bst = BST(node = BSTNode(key = 11, val = 11, parent = None))
        soughtKey = 11
        result = bst.FindNodeByKey(soughtKey)
        self.assertEqual(result.Node, bst.Root)
        self.assertFalse(result.ToLeft)
        self.assertTrue(result.NodeHasKey)
        self.assertTrue(verifyBST(bst))

    def testFindPresentNode(self):
        soughtKey = 12
        bst = makeFullBST(levelCount = 3)
        result = bst.FindNodeByKey(soughtKey)
        nodes = getBstNodes(bst)
        expectedParentNode = getNodeByKey(nodes, soughtKey)
        
        self.assertEqual(result.Node, expectedParentNode)
        self.assertFalse(result.ToLeft)
        self.assertTrue(result.NodeHasKey)
        self.assertTrue(verifyBST(bst))

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
        self.assertTrue(verifyBST(bst))

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
        self.assertTrue(verifyBST(bst))


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
        self.assertTrue(verifyBST(bst))

    def testAddPresentNode(self):
        soughtKey = 12
        bst = makeFullBST(levelCount = 3)
        result = bst.AddKeyValue(soughtKey, soughtKey)        
        self.assertFalse(result)
        self.assertTrue(verifyBST(bst))

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
        self.assertTrue(verifyBST(bst))

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
        self.assertTrue(verifyBST(bst))
    
    def testAddNodeToRootLeft(self):
        bst = makeFullBST(levelCount = 1)
        keyToAdd = bst.Root.NodeKey - 1
        addKeyResult = bst.AddKeyValue(key = keyToAdd, val = keyToAdd)
        nodes = getBstNodes(bst)
        addedNode = getNodeByKey(nodes, keyToAdd)
        self.assertEqual(bst.Root.LeftChild, addedNode)
        self.assertEqual(bst.Root.RightChild, None)
        self.assertTrue(addKeyResult)
        self.assertTrue(verifyBST(bst))
    
    def testAddNodeToRootRight(self):
        bst = makeFullBST(levelCount = 1)
        keyToAdd = bst.Root.NodeKey + 1
        addKeyResult = bst.AddKeyValue(key = keyToAdd, val = keyToAdd)
        nodes = getBstNodes(bst)
        addedNode = getNodeByKey(nodes, keyToAdd)
        self.assertEqual(bst.Root.RightChild, addedNode)
        self.assertEqual(bst.Root.LeftChild, None)
        self.assertTrue(addKeyResult)
        self.assertTrue(verifyBST(bst))
    

class TestFindMinMax(unittest.TestCase):
    def testFindMin(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 10
        actualMin = bst.FinMinMax(bst.Root, FindMax = False)
        self.assertEqual(expectedMin, actualMin.NodeKey)
        self.assertTrue(verifyBST(bst))

    def testFindMax(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 22
        actualMax = bst.FinMinMax(bst.Root, FindMax = True)
        self.assertEqual(expectedMax, actualMax.NodeKey)
        self.assertTrue(verifyBST(bst))

    def testFindMinSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMin = 18
        subtreeNodeKey = 20
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMin = bst.FinMinMax(subtreeNode, FindMax = False)
        self.assertEqual(actualMin.NodeKey, expectedMin)
        self.assertTrue(verifyBST(bst))

    def testFindMaxSubTree(self):
        bst = makeFullBST(levelCount = 3)
        expectedMax = 14
        subtreeNodeKey = 12
        nodes = getBstNodes(bst)
        subtreeNode = getNodeByKey(nodes, subtreeNodeKey)
        actualMax = bst.FinMinMax(subtreeNode, FindMax = True)
        self.assertEqual(actualMax.NodeKey, expectedMax)
        self.assertTrue(verifyBST(bst))
    
    def testFindMaxInSingleElementTree(self):
        bst = makeFullBST(levelCount = 1)
        expectedMax = bst.Root.NodeValue
        actualMax = bst.FinMinMax(bst.Root, FindMax = True)
        self.assertEqual(actualMax.NodeValue, expectedMax)
        self.assertTrue(verifyBST(bst))

    def testFindMaxInEmptyTree(self):
        bst = BST(None)
        actualMax = bst.FinMinMax(bst.Root, FindMax = True)
        self.assertEqual(actualMax, None)
        self.assertTrue(verifyBST(bst))


class TestCount(unittest.TestCase):
    def testEmpty(self):
        bst = BST(None)
        count = bst.Count()
        self.assertEqual(count, 0)
        self.assertTrue(verifyBST(bst))
    
    def testNonEmpty(self):
        levelCount = 3
        bst = makeFullBST(levelCount)
        count = bst.Count()
        self.assertEqual(count, 2**levelCount-1)
        self.assertTrue(verifyBST(bst))


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
        nodes = getBstNodes(bst)
        self.assertTrue(deletedNodeParent.LeftChild is None)
        self.assertEqual(deletedNodeParent.RightChild, parentAnotherChild)
        self.assertEqual(deletedNodeParent, parentAnotherChild.Parent)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

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
        nodes = getBstNodes(bst)
        self.assertEqual(deletedNodeParent.LeftChild, parentAnotherChild)
        self.assertTrue(deletedNodeParent.RightChild is None) 
        self.assertEqual(deletedNodeParent.LeftChild.Parent, deletedNodeParent)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))
    
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
        replacementNodePrevParent = replacementNode.Parent
        replacementNodePrevParentRightChild = replacementNode.Parent.RightChild
        deletedNodeRightChild = getNodeByKey(nodes, deletedNodeRightChildKey)
        deletedNodeLeftChild = getNodeByKey(nodes, deletedNodeLeftChildKey)

        delResult = bst.DeleteNodeByKey(keyToDel)
        nodes = getBstNodes(bst)
        self.assertEqual(deletedNodeParent.RightChild, replacementNode)
        self.assertEqual(replacementNode.Parent, deletedNodeParent)
        self.assertEqual(replacementNode.RightChild, deletedNodeRightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertEqual(replacementNode.LeftChild.Parent, replacementNode)
        self.assertEqual(replacementNode.RightChild.Parent, replacementNode)
        self.assertEqual(replacementNodePrevParent.LeftChild, None)
        self.assertEqual(replacementNodePrevParentRightChild, replacementNodePrevParent.RightChild)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

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
        replacementNodePrevParent = replacementNode.Parent
        replacementNodePrevParentRightChild = replacementNode.Parent.RightChild

        delResult = bst.DeleteNodeByKey(keyToDel)
        nodes = getBstNodes(bst)
        self.assertEqual(deletedNodeParent.LeftChild, replacementNode)
        self.assertEqual(replacementNode.Parent, deletedNodeParent)
        self.assertEqual(replacementNode.RightChild, deletedNodeRightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertEqual(replacementNode.LeftChild.Parent, replacementNode)
        self.assertEqual(replacementNode.RightChild.Parent, replacementNode)
        self.assertEqual(replacementNodePrevParent.LeftChild, None)
        self.assertEqual(replacementNodePrevParentRightChild, replacementNodePrevParent.RightChild)
        self.assertTrue(delResult)

    def testDeleteRootNode(self):
        replacementKey = 18
        bst = makeFullBST(levelCount = 3)
        nodes = getBstNodes(bst)
        replacementNode = getNodeByKey(nodes, replacementKey)
        deletedNode = bst.Root
        replacementNodePrevParent = replacementNode.Parent
        delResult = bst.DeleteNodeByKey(bst.Root.NodeKey)
        nodes = getBstNodes(bst)
        self.assertEqual(bst.Root, replacementNode)
        self.assertEqual(replacementNode.Parent, None)
        self.assertEqual(replacementNode.RightChild, deletedNode.RightChild)
        self.assertEqual(replacementNode.LeftChild, deletedNode.LeftChild)
        self.assertEqual(replacementNode.RightChild.Parent, replacementNode)
        self.assertEqual(replacementNode.LeftChild.Parent, replacementNode)
        self.assertEqual(replacementNodePrevParent.LeftChild, None)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

    def testDeleteLastNode(self):
        bst = makeFullBST(levelCount = 1)
        keyToDel = bst.Root.NodeKey
        delResult = bst.DeleteNodeByKey(keyToDel)
        self.assertEqual(bst.Root, None)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

    def testDeleteNodeReplacementIsRightChildAndHasSibing(self):
        rootKey = 10
        deletedKey = rootKey - 2
        replacementKey = deletedKey + 1
        deletedNodeLeftKey = deletedKey - 1
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        deletedNode = BSTNode(key = deletedKey, val = deletedKey, parent = rootNode)
        rootNode.LeftChild = deletedNode

        replacementNode = BSTNode(key = replacementKey , val  = replacementKey, parent = deletedNode)
        deletedNode.RightChild = replacementNode
        deletedNodeLeftChild = BSTNode(key = deletedNodeLeftKey , val  = deletedNodeLeftKey, parent = deletedNode)
        deletedNode.LeftChild = deletedNodeLeftChild

        bst = BST(rootNode)
        delResult = bst.DeleteNodeByKey(deletedKey)
        nodes = getBstNodes(bst)
        self.assertEqual(bst.Root.LeftChild, replacementNode)
        self.assertEqual(replacementNode.Parent.NodeKey, bst.Root.NodeKey)
        self.assertEqual(replacementNode.Parent, bst.Root)
        self.assertEqual(replacementNode.LeftChild, deletedNodeLeftChild)
        self.assertEqual(replacementNode.RightChild, None)
        self.assertEqual(replacementNode.LeftChild.Parent.NodeKey, replacementNode.NodeKey)
        self.assertEqual(replacementNode.LeftChild.Parent, replacementNode)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

    def testDeleteNodeReplacementIsRightChildAndHasNoSibing(self):
        rootKey = 10
        deletedKey = rootKey - 2
        replacementKey = deletedKey + 1
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        deletedNode = BSTNode(key = deletedKey, val = deletedKey, parent = rootNode)
        rootNode.LeftChild = deletedNode

        replacementNode = BSTNode(key = replacementKey , val  = replacementKey, parent = deletedNode)
        deletedNode.RightChild = replacementNode

        bst = BST(rootNode)
        delResult = bst.DeleteNodeByKey(deletedKey)
        nodes = getBstNodes(bst)
        self.assertEqual(bst.Root.LeftChild, replacementNode)
        self.assertEqual(replacementNode.Parent.NodeKey, bst.Root.NodeKey)
        self.assertEqual(replacementNode.Parent, bst.Root)
        self.assertEqual(replacementNode.LeftChild, None)
        self.assertEqual(replacementNode.RightChild, None)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))
            

    def testDeleteNodeLeftSucessorHasNoRightNode(self):
        rootKey = 10
        keyToRemove = rootKey - 2
        replacementKey = keyToRemove - 1
        replacementLeftChildKey = replacementKey - 1 
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        removedNode = BSTNode(key = keyToRemove, val = keyToRemove, parent = rootNode)
        rootNode.LeftChild = removedNode

        replacementNode = BSTNode(key = replacementKey , val  = replacementKey, parent = removedNode)
        removedNode.LeftChild = replacementNode
        replacementLeftChild = BSTNode(key = replacementLeftChildKey , val  = replacementKey, parent = replacementNode)
        replacementNode.LeftChild = replacementLeftChild

        bst = BST(rootNode)

        delResult = bst.DeleteNodeByKey(keyToRemove)
        nodes = getBstNodes(bst)
        self.assertEqual(bst.Root.LeftChild, replacementNode)
        self.assertEqual(replacementNode.Parent.NodeKey, bst.Root.NodeKey)
        self.assertEqual(replacementNode.Parent, bst.Root)
        self.assertEqual(replacementNode.LeftChild, replacementLeftChild)
        self.assertEqual(replacementNode, replacementLeftChild.Parent)
        self.assertEqual(replacementNode.RightChild, None)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

    def testDeleteRightSucessorHasNoRightNode(self):
        rootKey = 10
        keyToRemove = rootKey + 3
        removedRightChildKey  = keyToRemove + 2
        replacementKey = removedRightChildKey - 1
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        nodeToRemove = BSTNode(key = keyToRemove, val = keyToRemove, parent = rootNode)
        rootNode.RightChild = nodeToRemove

        removedNodeRightChild = BSTNode(key = removedRightChildKey , val  = removedRightChildKey, parent = nodeToRemove)
        nodeToRemove.RightChild = removedNodeRightChild

        replacementNode = BSTNode(key = replacementKey , val  = replacementKey, parent = removedNodeRightChild)
        removedNodeRightChild.LeftChild = replacementNode

        bst = BST(rootNode)
        delResult = bst.DeleteNodeByKey(keyToRemove)
        nodes = getBstNodes(bst)      
        self.assertEqual(bst.Root.RightChild.NodeKey, replacementNode.NodeKey)
        self.assertEqual(bst.Root.RightChild, replacementNode)
        self.assertEqual(replacementNode.Parent.NodeKey, bst.Root.NodeKey)
        self.assertEqual(replacementNode.Parent, bst.Root)
        self.assertEqual(replacementNode.LeftChild, None)
        self.assertEqual(replacementNode.RightChild, removedNodeRightChild)
        self.assertEqual(removedNodeRightChild.Parent.NodeKey, replacementNode.NodeKey)
        self.assertEqual(removedNodeRightChild.Parent, replacementNode)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))


    def testDeleteSingleLeadNode(self):
        rootKey = 10
        deletedKey = rootKey - 2
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        deletedNode = BSTNode(key = deletedKey, val = deletedKey, parent = rootNode)
        rootNode.LeftChild = deletedNode

        bst = BST(rootNode)
        delResult = bst.DeleteNodeByKey(deletedKey)
        nodes = getBstNodes(bst)
        self.assertEqual(bst.Root.LeftChild, None)
        self.assertEqual(bst.Root.RightChild, None)
        self.assertEqual(bst.Root, rootNode)
        self.assertTrue(delResult)
        self.assertTrue(verifyBST(bst))

    def testDeleteRootNode2(self):
        rootKey = 34
        rootRightCHildKey = 42
        replacementKey = 36
        replacementRightChildKey = 38
        rootNode = BSTNode(key = rootKey , val = rootKey, parent = None)
        rootRightChild = BSTNode(key = rootRightCHildKey , val = rootKey, parent = rootKey)   
        rootNode.RightChild = rootRightChild
        replacement = BSTNode(key = replacementKey, val = replacementKey, parent = rootRightChild)
        rootRightChild.LeftChild = replacement
        replacementRightChild = BSTNode(key = replacementRightChildKey, val = replacementRightChildKey, parent = replacement)
        replacement.RightChild = replacementRightChild

        bst = BST(rootNode)
        delResult = bst.DeleteNodeByKey(rootKey)
        nodes = getBstNodes(bst)

        self.assertEqual(bst.Root, replacement)
        self.assertEqual(replacement.RightChild, rootRightChild)
        self.assertEqual(rootRightChild.Parent, replacement)
        self.assertEqual(rootRightChild.LeftChild, replacementRightChild)
        self.assertEqual(rootRightChild.NodeKey, replacementRightChild.Parent.NodeKey)
        self.assertEqual(rootRightChild, replacementRightChild.Parent)

        self.assertTrue(delResult)
        #self.assertTrue(verifyBST(bst))


class TestBstInGeneral(unittest.TestCase):
    def testMakeFullBST(self):
        bst = makeFullBST(levelCount = 4)
        self.assertTrue(verifyBST(bst))

    def testDeleteAllElementsFromRoot(self):
        bst = makeFullBST(levelCount = 4)
        while bst.Root is not None:
            delResult = bst.DeleteNodeByKey(bst.Root.NodeKey)
            nodes = getBstNodesAscending(bst)
            self.assertTrue(verifyBST(bst))
            self.assertTrue(delResult)
            self.assertEqual(len(nodes), bst.Count())
            if len(nodes) > 0:
                self.assertEqual(bst.FinMinMax(bst.Root, FindMax = True), nodes[-1])
                self.assertEqual(bst.FinMinMax(bst.Root, FindMax = False), nodes[0])

    def testAddAndDeleteElements(self):
        bst = makeFullBST(levelCount = 7)
        nodes = getBstNodes(bst)
        nodesKeysToDel = [x.NodeKey for x in nodes]
        nodesKeysToAdd = [x.NodeKey + 1 for x in nodes]
        for i in range(0, len(nodesKeysToDel)):
            delResult =  bst.DeleteNodeByKey(nodesKeysToDel[i])
            self.assertTrue(verifyBST(bst))
            addResult =  bst.AddKeyValue(nodesKeysToAdd[i], nodesKeysToAdd[i])
            self.assertTrue(verifyBST(bst))
            nodes = getBstNodesAscending(bst)
            self.assertTrue(delResult)
            self.assertEqual(len(nodes), bst.Count())
            if len(nodes) > 0:
                self.assertEqual(bst.FinMinMax(bst.Root, FindMax = True), nodes[-1])
                self.assertEqual(bst.FinMinMax(bst.Root, FindMax = False), nodes[0])
