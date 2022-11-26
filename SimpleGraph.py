class Vertex:

    def __init__(self, val):
        self.Value = val
  
class SimpleGraph:
	
    def __init__(self, size):
        self.max_vertex = size
        self.m_adjacency = [[0] * size for _ in range(size)]
        self.vertex = [None] * size
        
    def _findFirstFreeSlotForVertex(self):
        slotIndex = 0
        for v in self.vertex:
            if v is None: break
            slotIndex += 1 
        
        if slotIndex >= self.max_vertex: 
            return None 
        return slotIndex

    def AddVertex(self, v):
        newVertex = Vertex(v)
        freeSlotIndex = self._findFirstFreeSlotForVertex()
        if freeSlotIndex is not None: 
            self.vertex[freeSlotIndex] = newVertex
	
    # здесь и далее, параметры v -- индекс вершины
    # в списке  vertex
    def RemoveVertex(self, v):
        if self._isVertexWithIndexExist(v):            
            for index in range(self.max_vertex):
                if self.IsEdge(v, index):
                    self.RemoveEdge(v, index)
            self.vertex[v] = None


    def _isVertexIndexValid(self, vertexIndex):
        if vertexIndex < 0 or vertexIndex >= self.max_vertex: return False
        return True

    def _isVertexWithIndexExist(self, vertexIndex):
        if self._isVertexIndexValid(vertexIndex): 
            return  self.vertex[vertexIndex] is not None
        else:
            return False

    def IsEdge(self, v1, v2):
        if self._isVertexWithIndexExist(v1) and self._isVertexWithIndexExist(v2):
            return self.m_adjacency[v1][v2] == 1 and self.m_adjacency[v2][v1] == 1

    def AddEdge(self, v1, v2):
        if self._isVertexWithIndexExist(v1) and self._isVertexWithIndexExist(v2):
            self.m_adjacency[v1][v2] = 1
            self.m_adjacency[v2][v1] = 1
	
    def RemoveEdge(self, v1, v2):
        if self._isVertexWithIndexExist(v1) and self._isVertexWithIndexExist(v2):
            self.m_adjacency[v1][v2] = 0
            self.m_adjacency[v2][v1] = 0


    def FindFirstVertexIndex(self, initialIndex):
        for i in range(initialIndex, self.max_vertex):
            if self.vertex[i] is not None: return i
        return None

    def GetAllAdjacentVertices(self, vertexIndex):
        adjacentVertices = []
        for i in range(self.max_vertex):
            if self.m_adjacency[vertexIndex][i] != 1: continue
            adjacentVertices.append(i)
        return adjacentVertices

    def FindSubtreesVerticesCount(self, vertexIndex, subtreeVerticesCounts):
        adjacentVertices = self.GetAllAdjacentVertices(vertexIndex)
        for adjacentVertIndex in adjacentVertices:
            if subtreeVerticesCounts[adjacentVertIndex] > 0: continue
            subtreeVerticesCounts[vertexIndex] += 1
            count = self.FindSubtreesVerticesCount(adjacentVertIndex, subtreeVerticesCounts)
            subtreeVerticesCounts[vertexIndex] += count
        return subtreeVerticesCounts[vertexIndex]

    def FindEdgesToRemove(self, vertexIndex, subtreeVerticesCounts):
        edgesToRemove = []
        adjacentVertices = self.GetAllAdjacentVertices(vertexIndex)
        for adjacentVertIndex in adjacentVertices:
            if subtreeVerticesCounts[adjacentVertIndex] > subtreeVerticesCounts[vertexIndex]: continue
            isSubtreeOdd = (subtreeVerticesCounts[adjacentVertIndex] + 1) % 2 == 0
            mayDeleteEdge =  isSubtreeOdd
            if mayDeleteEdge:
                edgesToRemove.append((vertexIndex, adjacentVertIndex))
            edgesToRemove += self.FindEdgesToRemove(adjacentVertIndex, subtreeVerticesCounts)
        return edgesToRemove

    # для каждой вершины определить, сколько вершин в её поддеревьях. (исключая родительскую вершину)
    def EvenTrees(self):
        initialVertexIndex = self.FindFirstVertexIndex(0)
        if initialVertexIndex is None: return [] 
        edgesIndexesToRemove = []
        subtreeVerticesCounts = [0] * self.max_vertex
        self.FindSubtreesVerticesCount(initialVertexIndex, subtreeVerticesCounts)
        if (subtreeVerticesCounts[initialVertexIndex] + 1) % 2 != 0:
            return []
            
        edgesIndexesToRemove = self.FindEdgesToRemove(initialVertexIndex, subtreeVerticesCounts)        
        vertexesListToRemove = []
        for indexes in edgesIndexesToRemove:
            vertexesListToRemove.append(self.vertex[indexes[0]])
            vertexesListToRemove.append(self.vertex[indexes[1]])
        return vertexesListToRemove
