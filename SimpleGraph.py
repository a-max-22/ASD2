class Vertex:

    def __init__(self, val):
        self.Value = val
        self.Hit = False
  
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
        if not self._isVertexWithIndexExist(v): return
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

    def GetFirstAdjacentUnvisitedVertex(self, vertexIndex):
        for i in range(self.max_vertex):
            if self.vertex[i] is None: continue
            if self.m_adjacency[vertexIndex][i] != 1: continue
            if self.vertex[i].Hit: continue
            return i
        return None

    def GetAllAdjacentUnvisitedVertices(self, vertexIndex):
        unsvisitedVertices = []
        for i in range(self.max_vertex):
            if self.vertex[i] is None: continue
            if self.m_adjacency[vertexIndex][i] != 1: continue
            if self.vertex[i].Hit: continue
            unsvisitedVertices.append(i)
        return unsvisitedVertices

    def _clearAllHitFlags(self):
        for v in self.vertex:
            v.Hit = False

    def DepthFirstSearch(self, VFrom, VTo):
        if not self._isVertexWithIndexExist(VFrom) or not self._isVertexWithIndexExist(VTo):
            return []
        self._clearAllHitFlags()

        visitedVerticesStack = []        
        visitedVerticesStack.append(VFrom)

        while len(visitedVerticesStack) > 0:
            currentVertex = visitedVerticesStack[-1]
            self.vertex[currentVertex].Hit = True

            nextAdjacentVertex = self.GetFirstAdjacentUnvisitedVertex(currentVertex)
                
            if nextAdjacentVertex == VTo:
                visitedVerticesStack.append(nextAdjacentVertex)
                return [self.vertex[v] for v in visitedVerticesStack]

            if nextAdjacentVertex is not None:                
                visitedVerticesStack.append(nextAdjacentVertex)
                currentVertex = nextAdjacentVertex
                continue
            
            visitedVerticesStack.pop()

        return []

    def _constructPathFromParentsArray(self, parents,  initialIndex, finalIndex):
        i = initialIndex
        path = []
        iterationsLimit = self.max_vertex
        itersCount = 0
        while i != None and itersCount <= iterationsLimit:
            path.append(i)
            i = parents[i]
            itersCount += 1
        assert itersCount <= iterationsLimit, "_constructPathFromParentsArray(): Iterations limit exceeded"
        return path

    def BreadthFirstSearch(self, VFrom, VTo):
        if not self._isVertexWithIndexExist(VFrom) or not self._isVertexWithIndexExist(VTo):
            return []
        self._clearAllHitFlags()
        
        verticesIndicesQueue = []
        verticesIndicesQueue.append(VFrom) 
        parents = [None]*self.max_vertex

        while len(verticesIndicesQueue) > 0:
            currentVertexIndex = verticesIndicesQueue[0]
            self.vertex[currentVertexIndex].Hit = True
            del verticesIndicesQueue[0]
            
            unvisitedVertices = self.GetAllAdjacentUnvisitedVertices(currentVertexIndex)
            verticesIndicesQueue += unvisitedVertices

            for i in unvisitedVertices:
                if parents[i] is None: 
                    parents[i] = currentVertexIndex
            
            if currentVertexIndex == VTo:
                way  = self._constructPathFromParentsArray(parents, currentVertexIndex, VFrom)
                return [self.vertex[v] for v in way[::-1]]

        return []
    
