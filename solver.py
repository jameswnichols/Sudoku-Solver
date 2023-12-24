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

class Board:
    def __init__(self):
        self.board = {}

    def reset(self):
        self.board = {}
        for y in range(0, 9):
            for x in range(0, 9):
                self.board[(x, y)]