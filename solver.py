from __future__ import annotations
import math
import pygame

pygame.init()

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
    def __init__(self, width : int, height : int):
        self.board = {}
        self.subGrids = {}
        self.width, self.height = width, height

    def _generatePreSubgridHashes(self, numberLocations : dict[Vector2, int]):
        subgridNumbers = {}
        for location, number in numberLocations.items():
            subGridVector = Vector2((location.x+1)//3, (location.y+1)//3)
            if subGridVector not in subgridNumbers:
                subgridNumbers[subGridVector] = set([number])
            else:
                subgridNumbers[subGridVector].add(number)
        
        return {k : list(set(range(1, 10)) - v) for k, v in subgridNumbers.items()}
    
    def setup(self, numberLocations : dict[Vector2, int] = {}):
        self.board = {}
        self.subGrids = {}

        #Generates a list of possible numbers that can be in each square in each subgrid, minus pre-supplied numbers.
        notedNumberLookup = self._generatePreSubgridHashes(numberLocations)

        for y in range(0, self.height):
            currentSubGridY = (y + 1) // 3
            for x in range(0, self.width):
                currentSubGridX = (x + 1) // 3

                positionVector = Vector2(x, y)
                subGridVector = Vector2(currentSubGridX, currentSubGridY)

                if subGridVector not in self.subGrids:
                    self.subGrids[subGridVector] = SubGrid()

                #If the position is in the pre-supplied numbers, then use that number instead.
                squareNumber = numberLocations[positionVector] if positionVector in numberLocations else None
                self.board[positionVector] = Square(squareNumber, self.subGrids[subGridVector])

                #All possible numbers can be in every box unless that subgrid has been added to the lookup table.
                notedNumbers = [range(1, 10)] if subGridVector not in notedNumberLookup else notedNumberLookup[subGridVector]
                self.board[positionVector] = notedNumbers

                self.subGrids[subGridVector].addSquare(self.board[positionVector])

sudokuBoard = Board(9, 9)
sudokuBoard.setup(numberLocations={Vector2(4, 4) : 1})