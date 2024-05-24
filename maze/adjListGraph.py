# ------------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Adjacent list implementation.
#
# __author__ = 'Jeffrey Chan', <YOU>
# __copyright__ = 'Copyright 2024, RMIT University'
# ------------------------------------------------------------------------


from typing import List

from maze.util import Coordinates3D, WallCoordinates
from maze.graph import Graph


class AdjListGraph(Graph):
    """
    Represents an undirected graph.  Please DO NOT modify this class.
    """

    def __init__(self):

        # dictionary where the keys are source vertices, and the values is a list of neighbouring vertices.
        # Essentially implements an adjacency list.
        self.m_vertListMap :dict[Coordinates3D,List[(Coordinates3D,bool)]] = {}


        
    def addVertex(self, label:Coordinates3D):

        if not self.hasVertex(label):
            self.m_vertListMap[label] = []



    def addVertices(self, vertLabels:List[Coordinates3D]):

        for label in vertLabels:
            self.addVertex(label)



    def addEdge(self, vert1:Coordinates3D, vert2:Coordinates3D, addWall:bool = False)->bool:

        if self.hasVertex(vert1) and self.hasVertex(vert2):
            # need to check if edge exists already, if it does, we just return
            for (neigh,_) in self.m_vertListMap[vert1]:
                if vert2 == neigh:
                    return False
                
            for (neigh,_) in self.m_vertListMap[vert2]:
                if vert1 == neigh:
                    return False
                    
            # okay if reach here edge doesn't exist
            self.m_vertListMap[vert1].append((vert2,addWall))
            self.m_vertListMap[vert2].append((vert1,addWall))
            return True
        else:
            return False
        


    def updateWall(self, vert1:Coordinates3D, vert2:Coordinates3D, wallStatus:bool)->bool:

        # need to check if vertices are there, and whether edge is there already
        if self.hasEdge(vert1, vert2):
            for i in range(len(self.m_vertListMap[vert1])):
                if self.m_vertListMap[vert1][i][0] == vert2:
                    self.m_vertListMap[vert1][i] = (vert2, wallStatus)
                    break

            for j in range(len(self.m_vertListMap[vert2])):
                if self.m_vertListMap[vert2][j][0] == vert1:
                    self.m_vertListMap[vert2][j] = (vert1, wallStatus)
                    break
    
            return True
        
        # all other cases we return False
        return False



    def removeEdge(self, vert1:Coordinates3D, vert2:Coordinates3D)->bool:
        
        if self.hasEdge(vert1, vert2):
            for i in range(len(self.m_vertListMap[vert1])):
                if self.m_vertListMap[vert1][i][0] == vert2:
                    self.m_vertListMap[vert1][i] = []
                    break

            for j in range(len(self.m_vertListMap[vert2])):
                if self.m_vertListMap[vert2][j][0] == vert1:
                    self.m_vertListMap[vert2][j] = []
                    break

            return True
        else:
            return False
        


    def hasVertex(self, label:Coordinates3D)->bool:
        return label in self.m_vertListMap



    def hasEdge(self, vert1:Coordinates3D, vert2:Coordinates3D)->bool:
        
        # check if vertices exist first
        if self.hasVertex(vert1) and self.hasVertex(vert2):
            for (neigh, _) in self.m_vertListMap[vert1]:
                if neigh == vert2:
                    return True

        return False



    def getWallStatus(self, vert1:Coordinates3D, vert2:Coordinates3D)->bool:
        
        # check if vertices exist first
        if self.hasEdge(vert1,vert2):
            for (neigh, bEdge) in self.m_vertListMap[vert1]:
                if neigh == vert2:
                    return bEdge
        
        # all other cases return False
        return False
        
    

    def neighbours(self, label:Coordinates3D)->List[Coordinates3D]:

        if self.hasVertex(label):
            return [neigh for (neigh,_) in self.m_vertListMap[label]]
        else:
            return []
        


    def neighbourWalls(self, label:Coordinates3D)->List[WallCoordinates]:

        if self.hasVertex(label):
            return [(label, neigh) for (neigh,hasWall) in self.m_vertListMap[label] if hasWall]
        


    def vertices(self)->List[Coordinates3D]:
        return self.m_vertListMap.keys()