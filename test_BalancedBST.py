from BalancedBST import BalancedBST, BSTNode
import unittest

def checkLevelForNode(node:BSTNode, expectedLevel):
    if node is None: return True
    if node.Level != expectedLevel:
        return False
    return checkLevelForNode(node.LeftChild, expectedLevel+1) and checkLevelForNode(node.RightChild, expectedLevel+1)


def checkLevels(bst:BalancedBST):
    return checkLevelForNode(bst.Root, expectedLevel = 0)

def visitBstNode(node):
    if node is None: return []
    return visitBstNode(node.LeftChild) + [node] + visitBstNode(node.RightChild) 

def getBstNodesAscending(bst):
    nodesLitsAscending = visitBstNode(bst.Root)
    return nodesLitsAscending

def printNode(node):
    print(node.NodeKey, node.LeftChild.NodeKey if node.LeftChild is not None else None , node.RightChild.NodeKey if node.RightChild is not None else None)

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

def makeParentAndAllChildren(parentKey):
    root = BSTNode(key = parentKey, parent = None)
    left = BSTNode(key = parentKey - (parentKey // 2), parent = root)
    right = BSTNode(key = parentKey + (parentKey // 2), parent = root)
    root.LeftChild = left
    right.RightChild  =  right 
    return root  


def addLeftChild(parentNode: BSTNode):
    parentKey = parentNode.NodeKey
    left = BSTNode(key = parentKey - (parentKey // 2), parent = parentNode)
    parentNode.LeftChild = left
    return left

def addRightChild(parentNode: BSTNode):
    parentKey = parentNode.NodeKey
    right = BSTNode(key = parentKey + (parentKey // 2), parent = parentNode)
    parentNode.RightChild = right
    return right

def makeUnbalancedTreeDepth3():
    depth = 3
    root = makeParentAndAllChildren(parentKey = 2**(depth+1))
    addedNode = addLeftChild(root.LeftChild)
    addedNode = addLeftChild(addedNode)
    addedNode = addLeftChild(addedNode)
    bbst = BalancedBST()
    bbst.Root = root
    return bbst 
 
def makeChildNodes(parent: BSTNode, childrenLevelCount):
    if childrenLevelCount == 1: return 

    childKeyEvaluationDelta = 2 ** (childrenLevelCount-1)
    leftChildKey = parent.NodeKey - childKeyEvaluationDelta
    rightChildKey = parent.NodeKey + childKeyEvaluationDelta
    leftChild = BSTNode(key = leftChildKey, parent = parent)
    rightChild = BSTNode(key = rightChildKey, parent = parent)
    parent.LeftChild = leftChild
    parent.RightChild = rightChild
    makeChildNodes(leftChild, childrenLevelCount-1)
    makeChildNodes(rightChild, childrenLevelCount-1)

def makeFullBST(levelCount):
    basicValue = 2 ** (levelCount+1)
    rootNode = BSTNode(key = basicValue, parent = None)
    makeChildNodes(rootNode, levelCount)
    resultTree = BalancedBST()
    resultTree.Root = rootNode
    return resultTree


class TestIsBalanced(unittest.TestCase):
    def testEmptyTree(self):
        bbst = BalancedBST()
        self.assertTrue(bbst.IsBalanced(None))

    def testSingleNodeTree(self):
        root = BSTNode(key = 0 , parent = None)
        bbst = BalancedBST()
        self.assertTrue(bbst.IsBalanced(root))
    
    def testBalancedTreeDepth1(self):
        bbst = BalancedBST()
        bbst.Root = makeParentAndAllChildren(parentKey = 16)
        self.assertTrue(bbst.IsBalanced(bbst.Root))
    
    def testUnbalancedTreeDepth3(self):
        bbst = makeUnbalancedTreeDepth3()
        self.assertFalse(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))

    def testIsFullTreeBalanced(self):
        bbst = makeFullBST(levelCount = 4)
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))

    def testUnbalancedTreeBalancedSubtrees(self):
        rightSubtree = makeFullBST(levelCount = 4)
        leftSubtree = makeParentAndAllChildren(parentKey = 4)
        root = BSTNode(key = 9, parent = None)
        root.LeftChild = leftSubtree
        leftSubtree.Parent = root
        root.RightChild = rightSubtree.Root
        rightSubtree.Root.Parent = root
        bbst = BalancedBST()
        bbst.Root = root
        self.assertFalse(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))


class TestGenerateBalancedTree(unittest.TestCase):

    def testGenerateTreeFromEmptyList(self):
        keys = []
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))

    def testGenerateTreeFromSingleElemList(self):
        keys = [0]
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        nodes = getBstNodesAscending(bbst)
        self.assertEqual(keys, [x.NodeKey for x in nodes])
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))
        self.assertTrue(checkLevels(bbst))

    def testGenerateTreeFromTwoElemList(self):
        keys = [0, 1]
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        nodes = getBstNodesAscending(bbst)
        self.assertEqual(keys, [x.NodeKey for x in nodes])
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))
        self.assertTrue(checkLevels(bbst))

    def testGenerateTreeFromThreeElemList(self):
        keys = [0, 1, 2]
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        nodes = getBstNodesAscending(bbst)
        self.assertEqual(keys, [x.NodeKey for x in nodes])
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))
        self.assertTrue(checkLevels(bbst))

    def testGenerateTreeFromFourElemList(self):
        keys = [0, 1, 3, 4]
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        nodes = getBstNodesAscending(bbst)
        self.assertEqual(keys, [x.NodeKey for x in nodes])
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))
        self.assertTrue(checkLevels(bbst))

    def testGenerateTreeFromThreeElemList(self):
        keys = [16, 12, 20, 10, 14, 18, 22, 9, 11, 13, 15, 17, 19, 21, 23]
        bbst = BalancedBST()
        bbst.GenerateTree(keys)
        nodes = getBstNodesAscending(bbst)
        keys.sort()
        self.assertEqual(keys, [x.NodeKey for x in nodes])
        self.assertTrue(bbst.IsBalanced(bbst.Root))
        self.assertTrue(verifyBST(bbst))
        self.assertTrue(checkLevels(bbst))
