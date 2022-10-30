
class BSTNode:
	
    def __init__(self, key, val, parent):
        self.NodeKey = key # ключ узла
        self.NodeValue = val # значение в узле
        self.Parent = parent # родитель или None для корня
        self.LeftChild = None # левый потомок
        self.RightChild = None # правый потомок


class BSTFind: # промежуточный результат поиска

    def __init__(self):
        self.Node = None # None если 
        # в дереве вообще нету узлов

        self.NodeHasKey = False # True если узел найден
        self.ToLeft = False # True, если родительскому узлу надо 
        # добавить новый узел левым потомком

class BST:

    def __init__(self, node):
        self.Root = node # корень дерева, или None

    def FindNodeByKey(self, key):
        if self.Root is None: return None

        currentNode = self.Root
        searchIsNotFinished = True
        while searchIsNotFinished:
            if key == currentNode.NodeKey:
                nodeIsFoundResult = BSTFind()
                nodeIsFoundResult.Node = currentNode
                nodeIsFoundResult.NodeHasKey = True 
                nodeIsFoundResult.ToLeft = False
                return nodeIsFoundResult

            if key < currentNode.NodeKey:
                if currentNode.LeftChild is not None:
                    currentNode = currentNode.LeftChild
                    continue
                searchIsNotFinished = False
                nodeNotFoundInsertToLeftChild = BSTFind()
                nodeNotFoundInsertToLeftChild.Node = currentNode
                nodeNotFoundInsertToLeftChild.NodeHasKey = False 
                nodeNotFoundInsertToLeftChild.ToLeft = True
                return nodeNotFoundInsertToLeftChild                

            if key > currentNode.NodeKey:
                if currentNode.RightChild is not None:
                    currentNode = currentNode.RightChild
                    continue
                searchIsNotFinished = False
                nodeNotFoundInsertToRightChild = BSTFind()
                nodeNotFoundInsertToRightChild.Node = currentNode
                nodeNotFoundInsertToRightChild.NodeHasKey = False 
                nodeNotFoundInsertToRightChild.ToLeft = False
                return nodeNotFoundInsertToRightChild
        return None

    def AddKeyValue(self, key, val):
        searchResult = self.FindNodeByKey(key)
        if searchResult.NodeHasKey: 
            return False

        parent = searchResult.Node
        if searchResult.ToLeft:
            parent.LeftChild = BSTNode(key, val, parent)
        else:
            parent.RightChild = BSTNode(key, val, parent)

        return True 
  
    def FinMinMax(self, FromNode, FindMax):
        # ищем максимальный/минимальный ключ в поддереве
        # возвращается объект типа BSTNode
        if self.Root is None: return None
        currentNode = FromNode
        while (True):
            nextNode = currentNode.RightChild if FindMax else currentNode.LeftChild
            if nextNode is None: return currentNode.NodeValue
            currentNode = nextNode
	
    def _findSuccessorNode(self, node):
        isLeaf = (node.LeftChild is None and node.RightChild is None)
        if isLeaf: return None
        suceessorCandidate = node.RightChild

        while suceessorCandidate.LeftChild is not None:
            suceessorCandidate = suceessorCandidate.LeftChild
        return suceessorCandidate

    def _replaceChild(self, replacedChildNode, replacementNode):
        parent = replacedChildNode.Parent
        if parent is None: return
        if parent.LeftChild == replacedChildNode: parent.LeftChild = replacementNode
        if parent.RightChild == replacedChildNode: parent.RightChild = replacementNode        

    def DeleteNodeByKey(self, key):
        searchResult = self.FindNodeByKey(key)
        if not searchResult.NodeHasKey:  return False # если узел не найден
        deletedNode = searchResult.Node
        deletedNodeChildren = (deletedNode.LeftChild, deletedNode.RightChild)
        deletedNodeParent = deletedNode.Parent
        
        replacementNode = self._findSuccessorNode(deletedNode)
        self._replaceChild(deletedNode, replacementNode)
        if replacementNode is None: return True

        self._replaceChild(replacementNode.Parent, None)
        replacementNode.LeftChild, replacementNode.RightChild = deletedNodeChildren
        replacementNode.Parent = deletedNodeParent
        return True

    def Count(self):
        if self.Root is None: return 0
        nodesList = [self.Root]
        currentNodeIndex = 0
        while currentNodeIndex < len(nodesList) :
            currentNode : BSTNode = nodesList[currentNodeIndex]
            if currentNode.LeftChild is not None: nodesList.append(currentNode.LeftChild)
            if currentNode.RightChild is not None: nodesList.append(currentNode.RightChild)
            currentNodeIndex += 1
        return len(nodesList)
