from concurrent.futures.process import _chain_from_iterable_of_lists
import imp
import unittest

from SimpleTree import SimpleTree, SimpleTreeNode


def makeSingleChildTree():
    rootVal = 0
    childVal = 1
    rootNode = SimpleTreeNode(rootVal, parent = None)
    childNode = SimpleTreeNode(rootVal, parent = None)
    tree = SimpleTree(rootNode)
    tree.AddChild(rootNode, childNode)
    return tree, rootNode, childNode

def makeTree(levelsCount, childCountForEachNode):
    allNodesList = []
    rootVal = 0
    rootNode = SimpleTreeNode(rootVal, parent = None)
    tree = SimpleTree(rootNode)
    allNodesList.append(rootNode)

    previousLevelChildren = [rootNode]
    for currentLevel in range(1, levelsCount):
        currentLevelChildren = [] 
        for currentParent in previousLevelChildren:
            for i in range(0, childCountForEachNode):
                childNode = SimpleTreeNode(currentLevel, parent = None)
                tree.AddChild(currentParent, childNode)
                currentLevelChildren.append(childNode)
        allNodesList += currentLevelChildren
        previousLevelChildren = currentLevelChildren  
    return tree, allNodesList

def getNodesEqualToValue(nodesList, value):
    return [x for x in nodesList if x.NodeValue == value]

class TestAddChild(unittest.TestCase):
    def testAddToRoot(self):
        rootVal = 0
        childVal = 1
        rootNode = SimpleTreeNode(rootVal, parent = None)
        childNode = SimpleTreeNode(rootVal, parent = None)
        tree = SimpleTree(rootNode)
        tree.AddChild(rootNode, childNode)
        self.assertEqual(rootNode.Children, [childNode])
        self.assertEqual(childNode.Parent, rootNode)

class TestDeleteNode(unittest.TestCase):
    def testDeleteChildOfRoot(self):
        tree, rootNode, childNode = makeSingleChildTree()
        tree.DeleteNode(childNode)
        self.assertEqual(rootNode.Children, [])
        self.assertEqual(childNode.Parent, None)

    def testDeleteRoot(self):
        tree, rootNode, childNode = makeSingleChildTree()
        tree.DeleteNode(rootNode) # не удаляет корневой элемент
        self.assertEqual(rootNode.Parent, None)
        self.assertEqual(tree.Root, rootNode)

    def testDeleteNonExistentNode(self):
        tree, rootNode, childNode = makeSingleChildTree()
        tree.DeleteNode(childNode)
        tree.DeleteNode(childNode)
        self.assertEqual(rootNode.Children, [])
        self.assertEqual(childNode.Parent, None)

class TestGetAllNodes(unittest.TestCase):
    def testGetAllNodesForRoot(self):
        rootVal = 0
        rootNode = SimpleTreeNode(rootVal, parent = None)
        tree = SimpleTree(rootNode)
        nodesList = tree.GetAllNodes()
        self.assertEqual(nodesList, [rootNode])

    def testGetNodesForEmptyTree(self):
        tree = SimpleTree(None)
        nodesList = tree.GetAllNodes()
        self.assertEqual(nodesList, [])

    def testGetNodesForSingleChild(self):
        tree, rootNode, childNode = makeSingleChildTree()
        nodesList = tree.GetAllNodes()
        self.assertEqual(nodesList, [rootNode, childNode])

    def testGetNodesForTwoLevelTree(self):
        tree, expectedNodesList = makeTree(levelsCount = 2, childCountForEachNode = 2)
        actualNodesList = tree.GetAllNodes()
        self.assertCountEqual(actualNodesList, expectedNodesList)

class TestFindNodesByValue(unittest.TestCase):
    def testFindInEmptyTree(self):
        tree = SimpleTree(None)
        nodesList = tree.FindNodesByValue(val = 3)
        self.assertEqual(nodesList, [])

    def testFindAbsentNode(self):
        tree, treeNodesList = makeTree(levelsCount = 2, childCountForEachNode = 2)
        nodesList = tree.FindNodesByValue(val = 4)
        self.assertEqual(nodesList, [])

    def testFindPresentNodes(self):
        tree, treeNodesList = makeTree(levelsCount = 4, childCountForEachNode = 2)
        val = 1
        nodesList = tree.FindNodesByValue(val)
        expectedList = getNodesEqualToValue(treeNodesList, val)
        self.assertCountEqual(nodesList, expectedList)

class TestMoveNode(unittest.TestCase):
    def testMoveNode(self):
        # root tree with two child nodes
        tree, treeNodesList = makeTree(levelsCount = 2, childCountForEachNode = 2)
        originalNode = treeNodesList[1]
        orignalParent = originalNode.Parent
        newParentNode = treeNodesList[2]
        tree.MoveNode(originalNode, newParentNode)
        self.assertEqual(originalNode.Parent, newParentNode)
        self.assertCountEqual([originalNode], newParentNode.Children)
        self.assertEqual(orignalParent.Children, [newParentNode])

class TestCount(unittest.TestCase):
   def testCount(self):
        # root tree with two child nodes
        tree, treeNodesList = makeTree(levelsCount = 2, childCountForEachNode = 2)
        self.assertEqual(tree.Count(), len(treeNodesList))

class TestLeafCount(unittest.TestCase):
   def testLeafCount(self):
        # root tree with two child nodes
        tree, treeNodesList = makeTree(levelsCount = 2, childCountForEachNode = 2)
        self.assertEqual(tree.LeafCount(), 2)

class TestLevels(unittest.TestCase):
   def testLelvels(self):
        tree, treeNodesList = makeTree(levelsCount = 3, childCountForEachNode = 2)
        tree.AssignLevelToNodes()
        levelsList = [x.Level for x in treeNodesList]
        expectedList = [0,1,1,2,2,2,2]
        self.assertEqual(expectedList, levelsList)