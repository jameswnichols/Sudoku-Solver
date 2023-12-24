from __future__ import annotations
import math

class Vector2:
    def __init__(self, x : int, y : int):
        self.x, self.y = x, y
        self.width, self.height = x, y
    
    def __add__(self, other : Vector2):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other : Vector2):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def distance(self, other : Vector2):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __eq__(self, other : Vector2):
        if isinstance(other, Vector2):
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

class Square:
    def __init__(self, number : int, subGrid : SubGrid):
        self.number = number
        self.notedNumbers = []
        self.subGrid = subGrid

class SubGrid:
    def __init__(self):
        self.squares : list[Square] = []
    
    def addSquare(self, square : Square):
        self.squares.append(square)

    def hasNumber(self, number : int):
        return number in [sq.number for sq in self.squares]

class Board:
    def __init__(self):
        self.board = {}
        self.subGrids = {}

    def _generatePreSubgridHashes(self, numberLocations : dict):
        pass

    def setup(self, numberLocations : dict = {}):
        self.board = {}
        self.subGrids = {}

        #TODO - Generate subgrid-hash : [list of numbers] dict for pre-supplied numbers

        for y in range(0, 9):
            currentSubGridY = (y + 1) // 3
            for x in range(0, 9):
                currentSubGridX = (x + 1) // 3

                positionVector = Vector2(x, y)
                subGridVector = Vector2(currentSubGridX, currentSubGridY)

                if subGridVector not in self.subGrids:
                    self.subGrids[subGridVector] = SubGrid()

                self.board[positionVector] = Square(None, self.subGrids[subGridVector])
                self.subGrids[subGridVector].addSquare(self.board[positionVector])

sudokuBoard = Board()
sudokuBoard.setup({Vector2(4, 4).hash() : 1})