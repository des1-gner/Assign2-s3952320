# -------------------------------------------------
# DON'T CHANGE THIS FILE.
# Utility classes and methods.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------


class Coordinates3D:
    """
    Forward declaration.
    """
    def getRow(self)->int:
        pass

    def getCol(self)->int:
        pass

    def getLevel(self)->int:
        pass



class Coordinates3D:
    """
    Represent 3D coordinates for maze cells.
    Note this is not exactly the same as Coordinate from Assignment 1.
    """

    def __init__(self, level: int, row:int, col:int):
        """
        Constructor.
        
        @param row: Row of coordinates.
        @param col: Column of coordinates.
        """
        self.m_level: int = level
        self.m_r: int = row
        self.m_c: int = col


    def getRow(self)->int:
        """
        @returns Row of coordinate.
        """
        return self.m_r
    


    def getCol(self)->int:
        """
        @returns Column of coordinate.
        """
        return self.m_c
    


    def getLevel(self)->int:
        """
        @returns Level of coordinate.
        """
        return self.m_level
    


    def __eq__(self, other: Coordinates3D):
        """
        Define == operator.

        @param other: Other coordinates that we are comparing with.
        """
        if other != None:
            return self.m_level == other.getLevel() and self.m_r == other.getRow() and self.m_c == other.getCol()
        else:
            return False
        

    
    def __lt__(self, other: Coordinates3D):
        """
        Define < operator.

        @param other: Other coordinates that we are comparing with.
        """

        if other != None:
            return (self.m_level < other.getLevel()) or \
                (self.m_level == other.getLevel() and self.m_r < other.getRow()) or \
                    (self.m_level == other.getLevel() and self.m_r == other.getRow() and self.m_c < other.getCol())
        else:
            return False



    def __add__(self, other:Coordinates3D)->Coordinates3D:
        """
        Override + operator.
        @param other: Other coordinates that we are adding.
        """

        if other != None:
            return Coordinates3D(self.getLevel() + other.getLevel(), self.getRow() + other.getRow(), self.getCol() + other.getCol())



    def __hash__(self):
        """
        Returns has value of Coordinates.  Needed for being a key in dictionaries.
        """
        return hash(str(self.m_level) + '|' + str(self.m_r)+'|'+str(self.m_c))
    


    def __str__(self):
        """
        Returns has value of Coordinates.  Needed for being a key in dictionaries.
        """
        return '({level}, {row}, {col})'.format(level=self.m_level, row=self.m_r, col=self.m_c)

        
###########################################################################################################3
        

# Forward declaration
class WallCoordinates:
    def getFirst(self)->Coordinates3D:
        pass  

    def getSecond(self)->Coordinates3D:
        pass  



class WallCoordinates:
    """
    Represent a wall coordinate essentially a pair of coordinates that uniquely identifies a wall.
    """

    def __init__(self, coord1: Coordinates3D, coord2: Coordinates3D):
        """
        Constructor.  We store the smaller coord as m_coord1st, and other as m_coord2nd.
        
        @param coord1: Coordinate on one side of the wall.
        @param coord2: Coordinate on the other side of the wall
        """

        if coord1 < coord2:
            self.m_coord1st = coord1
            self.m_coord2nd = coord2
        else:
            self.m_coord1st = coord2
            self.m_coord2nd = coord1

    

    def getFirst(self)->Coordinates3D:
        """
        @return First element of the pair of coordinates that this Wall Coordinate is representing.
        """
        return self.m_coord1st
    


    def getSecond(self)->Coordinates3D:
        """
        @return First element of the pair of coordinates that this Wall Coordinate is representing.
        """
        return self.m_coord2nd



    def __eq__(self, other: WallCoordinates):
        """
        Define == operator.

        @param other: Other coordinates that we are comparing with.
        """
        if other != None:
            # we don't need to test for reverse, as WallCoordinates always have the first coordinate as the smaller coordinates.
            return (self.m_coord1st == other.getFirst() and self.m_coord2nd == other.getSecond()) 
        else:
            return False



    def __hash__(self):
        """
        @return: Returns hash value of WallCoordinates.  Needed for being a key in dictionaries.
        """
        return hash(str(self.m_coord1st)+'-'+str(self.m_coord2nd))