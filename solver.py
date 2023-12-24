from __future__ import annotations
import math
import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

BOARD_SCALE = 50

FONT : dict[int, pygame.Font] = {x : pygame.Font("dogicapixelbold.ttf", x) for x in range(1, 100)}

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
        self.unscannedPositions = []
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

    def _getAdjecentToPosition(self, position : Vector2):
        possibleLocations = set()
        for y in range(0, self.height):
            possibleLocations.add(Vector2(position.x, y))
        for x in range(0, self.width):
            possibleLocations.add(Vector2(x, position.y))
        possibleLocations.remove(position)
        return list(possibleLocations)

    def scanSquares(self):
        while self.unscannedPositions:
            position = self.unscannedPositions.pop()
            squareNumber = self.board[position].number
            possibleLocations = self._getAdjecentToPosition(position)
            for location in possibleLocations:
                if squareNumber in self.board[location].notedNumbers:
                    self.board[location].notedNumbers.remove(squareNumber)

    def setNumber(self, position : Vector2, number : int):
        self.board[position].number = number
        self.unscannedPositions.append(position)

    def setup(self, numberLocations : dict[Vector2, int] = {}):
        self.board = {}
        self.subGrids = {}
        self.unscannedPositions = [] #list(numberLocations.keys())

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
                self.board[positionVector] = Square(None, self.subGrids[subGridVector])

                self.setNumber(positionVector, squareNumber)

                #All possible numbers can be in every box unless that subgrid has been added to the lookup table.
                self.board[positionVector].notedNumbers = [i for i in range(1, 10)] if subGridVector not in notedNumberLookup else notedNumberLookup[subGridVector]

                self.subGrids[subGridVector].addSquare(self.board[positionVector])
        
        self.scanSquares()
    
    def render(self, screen : pygame.Surface):

        centreVector = Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        renderedBoardWidth, renderedBoardHeight = self.width * BOARD_SCALE, self.height * BOARD_SCALE

        for y in range(0, self.height):
            for x in range(0, self.width):
                number = self.board[Vector2(x, y)].number
                number = "" if not number else number

                textSurface = FONT[15].render(str(number), False, (0,0,0))

                squarePosition = Vector2(x * BOARD_SCALE, y * BOARD_SCALE)

                halfBoardScale = BOARD_SCALE / 2

                #Centre square coordinate to its position relative to the centre of the screen.
                squarePosition = squarePosition + centreVector - Vector2(renderedBoardWidth//2, renderedBoardHeight//2)

                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(squarePosition.x, squarePosition.y, BOARD_SCALE, BOARD_SCALE), 1)

                textSizeHalfVector = Vector2(textSurface.get_width()//2, textSurface.get_height()//2)

                #Centre text relative to its square coordinate
                textPosition = squarePosition + Vector2(halfBoardScale, halfBoardScale) - textSizeHalfVector

                screen.blit(textSurface, (textPosition.x, textPosition.y))

sudokuBoard = Board(9, 9)
sudokuBoard.setup(numberLocations={Vector2(4, 4) : 1})

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

running = True

while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sudokuBoard.render(screen)

    pygame.display.flip()
    clock.tick_busy_loop(60)

pygame.quit()