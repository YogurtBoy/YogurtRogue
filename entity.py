from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

# A generic object to represent players, enemies, items, etc.
class Entity:
    gamemap: GameMap

    def __init__(self, 
                 gamemap: Optional[GameMap] = None, 
                 x: int = 0, 
                 y: int = 0, 
                 char: str = "?", 
                 color: Tuple[int, int, int] = (255, 255, 255), 
                 name: str = "<Unnamed>", 
                 blocks_movement: bool = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color 
        self.name = name
        self.blocks_movement = blocks_movement
        # If gamemap isn't provided now, it will be set later
        if gamemap:
            self.gamemap = gamemap
            gamemap.entities.add(self)


    # Spawn a copy of this instance at the given location
    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y 
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone
    
    # Place this entity at a new location. Handles moving across GameMaps
    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"): # If uninitialized
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)
        
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by the input amount
        self.x += dx
        self.y += dy

        
