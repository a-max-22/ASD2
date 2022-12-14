from SimpleGraph import SimpleGraph, Vertex

import unittest

def isVertexWithSpecifiedValuePresent(g:SimpleGraph, vertexValue:int):
    for vertex in g.vertex:
        if vertex is None: continue
        if vertex.Value != vertexValue: continue
        return True
    return False

def validateGraph(g:SimpleGraph):
    if g.max_vertex < len(g.vertex): return False
    for v1Index in range(g.max_vertex):
        for v2Index in range(g.max_vertex):
            if (g.vertex[v1Index] is None or g.vertex[v2Index] is None) and (g.m_adjacency[v1Index][v2Index] == 1 \
                or g.m_adjacency[v2Index][v1Index] == 1 ):
                return False
    return True 

def areVerticesAdjacent(g:SimpleGraph, vertIndex1: int , vertIndex2: int):
    if vertIndex1 < 0 or vertIndex1 > g.max_vertex: return False
    if vertIndex2 < 0 or vertIndex2 > g.max_vertex: return False
    if g.vertex[vertIndex1] is None: return False
    if g.vertex[vertIndex2] is None: return False
    return g.m_adjacency[vertIndex1][vertIndex2] == 1 and g.m_adjacency[vertIndex2][vertIndex1] == 1


class TestAddVertex(unittest.TestCase):
    def testAddToEmptyGraph(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 2
        g.AddVertex(newVertexValue)
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))

    def testAddToNonEmptyGraph(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 2        
        g.AddVertex(newVertexValue)
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
    
    def testAddToFullGraph(self):
        g = SimpleGraph(size = 1)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertFalse(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        

class TestAddEdge(unittest.TestCase):
    def testAddToExistingVertices(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, 1)
        self.assertTrue(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

    def testAddToNonExistentVertices(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        
        g.AddEdge(0, 1)
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

    def testVerticesIndicesOutOfRange(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, -1)
        self.assertTrue(validateGraph(g))

    def testVerticesIndicesOutOfRange2(self):
        graphSize = 2
        g = SimpleGraph(size = graphSize)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, graphSize + 1)
        self.assertTrue(validateGraph(g))


class TestIsEdge(unittest.TestCase):
    def testNonExistentEdgeWithExistentVertices(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        self.assertFalse(g.IsEdge(0,1))
        self.assertFalse(g.IsEdge(1,0))
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

    def testNonExistentVertices(self):
        g = SimpleGraph(size = 2)
        self.assertFalse(g.IsEdge(0,1))
        self.assertFalse(g.IsEdge(1,0))
        self.assertTrue(validateGraph(g))

    def testExistentEdge(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, 1)
        self.assertTrue(g.IsEdge(0,1))
        self.assertTrue(g.IsEdge(1,0))
        self.assertTrue(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))


    def testOutOfRange(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, 1)
        self.assertFalse(g.IsEdge(-1,0))
        self.assertFalse(g.IsEdge(0,-1))
        self.assertTrue(validateGraph(g))
    
    def testOutOfRange2(self):
        newSize = 2
        g = SimpleGraph(size = newSize)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, 1)
        self.assertFalse(g.IsEdge(0, newSize + 1))
        self.assertFalse(g.IsEdge(newSize + 1, 0))
        self.assertTrue(validateGraph(g))
    


class TestRemoveEdge(unittest.TestCase):
    def testNonExistentEdgeWithExistentVertices(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        
        g.RemoveEdge(0,1)
        g.RemoveEdge(1,0)

        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

    def testNonExistentEdgeWithNonExistentVertices(self):
        g = SimpleGraph(size = 2)
        g.RemoveEdge(0,1)
        g.RemoveEdge(1,0)

        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

    def testOutOfRange(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        
        g.RemoveEdge(0,-11)
        g.RemoveEdge(-11,0)
        self.assertTrue(validateGraph(g))

    
    def testOutOfRange2(self):
        newSize = 2
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        
        g.RemoveEdge(newSize + 1, 0)
        g.RemoveEdge(0 ,newSize + 1)
        self.assertTrue(validateGraph(g))

    def testRemoveExistentEdge(self):
        g = SimpleGraph(size = 2)
        newVertexValue = 3
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))
        
        newVertexValue = 4
        g.AddVertex(newVertexValue) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))

        g.AddEdge(0, 1)
        self.assertTrue(g.IsEdge(0,1))
        self.assertTrue(g.IsEdge(1,0))
        self.assertTrue(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))

        g.RemoveEdge(0, 1)
        self.assertFalse(g.IsEdge(0,1))
        self.assertFalse(g.IsEdge(1,0))
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(validateGraph(g))


class TestRemoveVertex(unittest.TestCase):
    def testRemoveNonExistentVertex(self):
        g = SimpleGraph(size = 2)
        self.assertFalse(isVertexWithSpecifiedValuePresent(g, vertexValue = 0))
        g.RemoveVertex(0)
        self.assertFalse(isVertexWithSpecifiedValuePresent(g, vertexValue = 0))
        self.assertTrue(validateGraph(g))

    def testRemoveExistentVertexNoEdges(self):
        g = SimpleGraph(size = 2)
        newVertexValue1 = 3
        g.AddVertex(newVertexValue1) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue1))
        self.assertTrue(validateGraph(g))
        
        newVertexValue2 = 4
        g.AddVertex(newVertexValue2) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue2))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        
        g.RemoveVertex(1)
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue1))
        self.assertFalse(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue2))
        self.assertTrue(validateGraph(g))        
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        


    def testRemoveExistentVertexWithAllEdges(self):
        g = SimpleGraph(size = 3)
        newVertexValue1 = 3
        g.AddVertex(newVertexValue1) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue1))
        self.assertTrue(validateGraph(g))
        
        newVertexValue2 = 4
        g.AddVertex(newVertexValue2) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue2))
        self.assertTrue(validateGraph(g))        

        newVertexValue3 = 5
        g.AddVertex(newVertexValue3) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue3))
        self.assertTrue(validateGraph(g))        

        g.AddEdge(0,1)
        g.AddEdge(1,2)
        self.assertTrue(areVerticesAdjacent(g, 0, 1))
        self.assertTrue(areVerticesAdjacent(g, 1, 2))

        g.RemoveVertex(1)
        self.assertFalse(areVerticesAdjacent(g, 0, 1))
        self.assertFalse(areVerticesAdjacent(g, 1, 2))
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue1))
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue3))
        self.assertFalse(isVertexWithSpecifiedValuePresent(g, vertexValue = newVertexValue2))
        self.assertTrue(validateGraph(g))


def determineVerticesCount(edgesList):
    vertices = set()
    for edge in edgesList:
        vertices.add(edge[0])
        vertices.add(edge[1])

    return len(vertices)        

def makeGraphByEdgeList(edgesList):
    verticesCount = determineVerticesCount(edgesList)
    g = SimpleGraph(size = verticesCount)
    for v in range(verticesCount):
        g.AddVertex(v)
    for edge in edgesList:
        g.AddEdge(edge[0], edge[1])
    return g

def selectVerticesByIndices(g:SimpleGraph, verticesIndexesList):
    return [g.vertex[v] for v in verticesIndexesList]

class TestDepthFirstSearch(unittest.TestCase):
    def testDfsNonExistentNode(self):
        g = SimpleGraph(size = 3)
        vertexVal = 3
        g.AddVertex(vertexVal) 
        self.assertTrue(isVertexWithSpecifiedValuePresent(g, vertexValue = vertexVal))
        self.assertTrue(validateGraph(g))
                
        way = g.DepthFirstSearch(0,1)
        self.assertEqual(way, [])
        self.assertTrue(validateGraph(g))        


    def testDfsEmptyGraph(self):
        g = SimpleGraph(size = 3)
        way = g.DepthFirstSearch(0,1)
        self.assertEqual(way, [])
        self.assertTrue(validateGraph(g))        

    def testDfsOneEdge(self):
        g = makeGraphByEdgeList([(0,1)])
        expectedWay = selectVerticesByIndices(g, [0,1])
        actualWay = g.DepthFirstSearch(0,1)
        self.assertEqual(actualWay, expectedWay)
        self.assertTrue(validateGraph(g))        

    def testDfsTwoEdges(self):
        g = makeGraphByEdgeList([(0,1),(1,2)])
        expectedWay = selectVerticesByIndices(g, [0, 1, 2])
        actualWay = g.DepthFirstSearch(0,2)
        self.assertEqual(actualWay, expectedWay)
        self.assertTrue(validateGraph(g))        

    def testDfsMultiEdges(self):
        g = makeGraphByEdgeList([(0,1),(1,2), (0,3), (3,4)])
        expectedWay = selectVerticesByIndices(g, [0, 3, 4])
        actualWay = g.DepthFirstSearch(0, 4)
        self.assertEqual(actualWay, expectedWay)
        self.assertTrue(validateGraph(g))        

    def testDfsCycleEdges(self):
        g = makeGraphByEdgeList([(0,1),(1,2), (2,3), (0,4), (4,3)])
        expectedWay = selectVerticesByIndices(g, [0, 1, 2, 3])
        actualWay = g.DepthFirstSearch(0, 3)
        self.assertEqual(actualWay, expectedWay)

    def testDfsCycleEdges2(self):
        g = makeGraphByEdgeList([(0,1),(1,2), (2,3), (3,4), (4,5), (5,6), (6,0)])
        expectedWay = selectVerticesByIndices(g, [0, 1, 2, 3, 4, 5, 6])
        actualWay = g.DepthFirstSearch(0, 6)
        self.assertEqual(actualWay, expectedWay)

    def testDfsNoEdges(self):
        g = SimpleGraph(size = 2)
        g.AddVertex(0)
        g.AddVertex(1)
        actualWay = g.DepthFirstSearch(0, 1)
        self.assertEqual(actualWay, [])
        self.assertTrue(validateGraph(g))

    def testDfsNoWay(self):
        g = makeGraphByEdgeList([(0,1),(1,2), (2,3), (4,5), (5,6), (6,7)])
        actualWay = g.DepthFirstSearch(0, 7)
        self.assertEqual(actualWay, [])
        self.assertTrue(validateGraph(g))


    def testSequentialDfs(self):
        g = makeGraphByEdgeList([(0,1),(1,2), (2,3), (0,4), (4,3)])
        expectedWay = selectVerticesByIndices(g, [0, 1, 2, 3])
        actualWay = g.DepthFirstSearch(0, 3)
        self.assertEqual(actualWay, expectedWay)
        actualWay = g.DepthFirstSearch(0, 3)
        self.assertEqual(actualWay, expectedWay)
        self.assertTrue(validateGraph(g))        
