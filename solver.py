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
    
    def hash(self):
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

    def setup(self, numberLocations : dict = {}):
        self.board = {}
        self.subGrids = {}

        #TODO - Generate subgrid-hash : [list of numbers] dict for pre-supplied numbers

        for y in range(0, 9):
            currentSubGridY = (y + 1) // 3
            for x in range(0, 9):
                currentSubGridX = (x + 1) // 3

                positionVectorHash = Vector2(x, y).hash()
                subGridVectorHash = Vector2(currentSubGridX, currentSubGridY).hash()

                if subGridVectorHash not in self.subGrids:
                    self.subGrids[subGridVectorHash] = SubGrid()

                self.board[positionVectorHash] = Square(None, self.subGrids[subGridVectorHash])
                self.subGrids[subGridVectorHash].addSquare(self.board[positionVectorHash])

sudokuBoard = Board()
sudokuBoard.setup({})