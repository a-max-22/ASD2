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
        if self.Root is None:
            result = BSTFind()
            result.Node = None
            result.NodeHasKey = False
            result.ToLeft = False
            return result

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
        if parent is None:
            self.Root = BSTNode(key, val, None)
            return True

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
            if nextNode is None: return currentNode
            currentNode = nextNode
	
    def _findSuccessorNode(self, node):
        isLeaf = (node.LeftChild is None and node.RightChild is None)
        if isLeaf: return None

        suceessorCandidate = node.RightChild
        if suceessorCandidate is None: return node.LeftChild 

        while suceessorCandidate.LeftChild is not None:
            suceessorCandidate = suceessorCandidate.LeftChild
        return suceessorCandidate

    def _replaceChild(self, replacedChildNode, replacementNode):
        parent = replacedChildNode.Parent
        if parent is None: return
        if parent.LeftChild == replacedChildNode: parent.LeftChild = replacementNode
        if parent.RightChild == replacedChildNode: parent.RightChild = replacementNode        

    def _replaceParent(self, modifiedNode, newParent):
        if modifiedNode is None: return 
        modifiedNode.Parent = newParent

    def DeleteNodeByKey(self, key):
        searchResult = self.FindNodeByKey(key)
        if not searchResult.NodeHasKey:  return False

        deletedNode = searchResult.Node        
        replacementNode = self._findSuccessorNode(deletedNode)

        if deletedNode == self.Root:
            self.Root = replacementNode
        
        if replacementNode is None:
            self._replaceChild(deletedNode, None)
            return True

        if deletedNode.RightChild == replacementNode:
            replacementNode.Parent = deletedNode.Parent
            replacementNode.LeftChild = deletedNode.LeftChild
            self._replaceParent(deletedNode.LeftChild, replacementNode)
            self._replaceChild(deletedNode, replacementNode)
            return True

        if deletedNode.LeftChild == replacementNode:
            replacementNode.Parent = deletedNode.Parent
            self._replaceChild(deletedNode, replacementNode)
            return True

        #if we reach here - replacement node is leaf and is left child of it's parent 
        replacementNode.Parent.LeftChild = replacementNode.RightChild
        if replacementNode.RightChild is not None:
            replacementNode.RightChild.Parent = replacementNode.Parent
        replacementNode.RightChild = deletedNode.RightChild
        replacementNode.LeftChild = deletedNode.LeftChild
        replacementNode.Parent = deletedNode.Parent
        self._replaceParent(deletedNode.LeftChild, replacementNode)
        self._replaceParent(deletedNode.RightChild, replacementNode)        
        self._replaceChild(deletedNode, replacementNode)
        return True

    def Count(self):
        if self.Root is None: return 0
        nodesList = [self.Root]
        currentNodeIndex = 0
        while currentNodeIndex < len(nodesList) :
            currentNode = nodesList[currentNodeIndex]
            if currentNode.LeftChild is not None: nodesList.append(currentNode.LeftChild)
            if currentNode.RightChild is not None: nodesList.append(currentNode.RightChild)
            currentNodeIndex += 1
        return len(nodesList)
