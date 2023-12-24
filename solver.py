from __future__ import annotations
import math
import pygame
import pickle

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
    def __init__(self, number : int, subGrid : SubGrid, position : Vector2):
        self.number = number
        self.notedNumbers = []
        self.subGrid = subGrid
        self.position = position

class SubGrid:
    def __init__(self):
        self.squares : list[Square] = []
        self.emptySquares = []
    
    def addSquare(self, square : Square):
        self.squares.append(square)
        self.emptySquares.append(square)

    def hasNumber(self, number : int):
        return number in [sq.number for sq in self.squares]

    def getRemainingNumbers(self):
        return [x for x in range(1, 10) if x not in [sq.number for sq in self.squares]]

class Board:
    def __init__(self, width : int, height : int):
        self.board = {}
        self.subGrids = {}
        self.width, self.height = width, height
        self.topLeftPosition = Vector2(0, 0)
        self.renderSize = Vector2(0, 0)
        self.scanned = False

    def _getAdjecentToPosition(self, position : Vector2):
        possibleLocations = set()
        for y in range(0, self.height):
            possibleLocations.add(Vector2(position.x, y))
        for x in range(0, self.width):
            possibleLocations.add(Vector2(x, position.y))
        possibleLocations.remove(position)
        return list(possibleLocations)

    def scanSquares(self):
        for position, square in self.board.items():
            square.notedNumbers = [x for x in range(1, 10)]

        for position, square in self.board.items():
            #Remove noted numbers for number in grid

            self.lastFreeCell(position)
            self.lastRemainingCell(position)
    
    def lastFreeCell(self, position : Vector2):
        square = self.board[position]
        subGrid = square.subGrid
        for subSquare in subGrid.squares:
            if square.number in subSquare.notedNumbers:
                subSquare.notedNumbers.remove(square.number)

    def lastRemainingCell(self, position : Vector2):
        square = self.board[position]
        possibleLocations = self._getAdjecentToPosition(position)
        for possibleLocation in possibleLocations:
            if square.number in self.board[possibleLocation].notedNumbers:
                self.board[possibleLocation].notedNumbers.remove(square.number)

    def obviousSingle(self):
        for subGrid in self.subGrids.values():
            for emptySquare in subGrid.emptySquares:
                if len(emptySquare.notedNumbers) == 1:
                    self.setNumber(emptySquare.position, emptySquare.notedNumbers[0])
                    return True
        return False
    
    def obviousPairs(self):
        for subGrid in self.subGrids.values():
            pairs = []
            for emptySquare in subGrid.emptySquares:
                if len(emptySquare.notedNumbers) == 1:
                    pass

    def setNumber(self, position : Vector2, number : int):
        self.board[position].number = number
        if self.board[position] in self.board[position].subGrid.emptySquares:
            self.board[position].subGrid.emptySquares.remove(self.board[position])
    
    def removeNumber(self, position : Vector2):
        self.board[position].number = None
        if self.board[position] not in self.board[position].subGrid.emptySquares:
            self.board[position].subGrid.emptySquares.append(self.board[position])

    def setup(self):
        self.board = {}
        self.subGrids = {}

        for y in range(0, self.height):
            currentSubGridY = y // 3
            for x in range(0, self.width):
                currentSubGridX = x // 3

                positionVector = Vector2(x, y)
                subGridVector = Vector2(currentSubGridX, currentSubGridY)

                if subGridVector not in self.subGrids:
                    self.subGrids[subGridVector] = SubGrid()

                #If the position is in the pre-supplied numbers, then use that number instead.
                self.board[positionVector] = Square(None, self.subGrids[subGridVector], positionVector)

                #All possible numbers can be in every box unless that subgrid has been added to the lookup table.
                #self.board[positionVector].notedNumbers = [i for i in range(1, 10)]

                self.subGrids[subGridVector].addSquare(self.board[positionVector])
        
        #self.scanSquares()
    
    def render(self, screen : pygame.Surface):

        centreVector = Vector2(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        renderedBoardWidth, renderedBoardHeight = self.width * BOARD_SCALE, self.height * BOARD_SCALE

        halfRenderedBoardVector = Vector2(renderedBoardWidth//2, renderedBoardHeight//2)

        for y in range(0, self.height):
            for x in range(0, self.width):
                square = self.board[Vector2(x, y)]

                squarePosition = Vector2(x * BOARD_SCALE, y * BOARD_SCALE)

                halfBoardScale = BOARD_SCALE / 2

                #Centre square coordinate to its position relative to the centre of the screen.
                squarePosition = squarePosition + centreVector - halfRenderedBoardVector

                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(squarePosition.x, squarePosition.y, BOARD_SCALE, BOARD_SCALE), 1)

                gridTopLeft = centreVector - halfRenderedBoardVector

                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(gridTopLeft.x, gridTopLeft.y, renderedBoardWidth, renderedBoardHeight), 2)

                #Show noted numbers instead
                if not square.number:
                    notedSurface = pygame.Surface((BOARD_SCALE, BOARD_SCALE), pygame.SRCALPHA)

                    for i, notedNumber in enumerate(self.board[Vector2(x, y)].notedNumbers):
                        notedX = (i % 3) * (BOARD_SCALE / 3)
                        notedY = ((i // 3) * (BOARD_SCALE / 3)) + 3
                        notedText = FONT[8].render(str(notedNumber), False, (0, 0, 0))
                        centeredNotedPosition = Vector2(notedX, notedY) + Vector2(notedText.get_width()//2, notedText.get_height()//2)
                        notedSurface.blit(notedText, (centeredNotedPosition.x, centeredNotedPosition.y))

                    screen.blit(notedSurface, (squarePosition.x, squarePosition.y))
                else:
                    textSurface = FONT[15].render(str(square.number), False, (0,0,0))

                    textSizeHalfVector = Vector2(textSurface.get_width()//2, textSurface.get_height()//2)

                    #Centre text relative to its square coordinate
                    textPosition = squarePosition + Vector2(halfBoardScale, halfBoardScale) - textSizeHalfVector

                    screen.blit(textSurface, (textPosition.x, textPosition.y))
        
        for subY in range(0, (self.height) // 3):
            for subX in range(0, (self.width) // 3):
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(gridTopLeft.x+subX*3*BOARD_SCALE, gridTopLeft.y+subY*3*BOARD_SCALE,3*BOARD_SCALE,3*BOARD_SCALE), 2)

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(gridTopLeft.x, gridTopLeft.y, renderedBoardWidth, renderedBoardHeight), 4)

        self.topLeftPosition = gridTopLeft
        self.renderSize = Vector2(renderedBoardWidth, renderedBoardHeight)
    
    def getMouseHoveredVector(self):
        gridRect = pygame.Rect(self.topLeftPosition.x, self.topLeftPosition.y, self.renderSize.width, self.renderSize.height)
        mousePosition = Vector2(*pygame.mouse.get_pos())
        if not gridRect.collidepoint(mousePosition.x, mousePosition.y):
            return None

        mousePositionShifted = mousePosition - self.topLeftPosition
        roundedMousePosition = Vector2(mousePositionShifted.x // BOARD_SCALE, mousePositionShifted.y // BOARD_SCALE)

        if roundedMousePosition not in self.board:
            return None

        return roundedMousePosition

sudokuBoard = Board(9, 9)
sudokuBoard.setup()

commandOrder = [sudokuBoard.obviousSingle]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

running = True

progress = False

while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            #If number key pressed
            if 49 <= event.key <= 57:
                hoveredVector = sudokuBoard.getMouseHoveredVector()
                if not hoveredVector:
                    continue
                sudokuBoard.setNumber(hoveredVector, event.key-48)
            
            if event.key == pygame.K_0:
                sudokuBoard.removeNumber(sudokuBoard.getMouseHoveredVector())
            
            if event.key == pygame.K_s:
                with open("output.sav","wb") as f:
                    pickle.dump(sudokuBoard, f)
                
            if event.key == pygame.K_l:
                with open("output.sav", "rb") as f:
                    sudokuBoard = pickle.load(f)

            if event.key == pygame.K_p:
                sudokuBoard.scanSquares()
            
            if event.key == pygame.K_RETURN:
                progress = True

    #sudokuBoard.scanSquares()

    if progress:
        progress = False
        
        for command in commandOrder:
            result = command()
            if result:
                break

    sudokuBoard.render(screen)

    

    pygame.display.flip()
    clock.tick_busy_loop(60)

pygame.quit()