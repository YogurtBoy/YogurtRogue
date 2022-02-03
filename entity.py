from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

# A generic object to represent players, enemies, items, etc.
class Entity:
    parent: GameMap

    def __init__(self, 
                 parent: Optional[GameMap] = None, 
                 x: int = 0, 
                 y: int = 0, 
                 char: str = "?", 
                 color: Tuple[int, int, int] = (255, 255, 255), 
                 name: str = "<Unnamed>", 
                 blocks_movement: bool = False, 
                 render_order: RenderOrder = RenderOrder.CORPSE,
                 ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color 
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        # If parent isn't provided now, it will be set later
        if parent:
            self.gamemap = parent
            parent.entities.add(self)
        
    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap


    # Spawn a copy of this instance at the given location
    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y 
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone
    
    # Place this entity at a new location. Handles moving across GameMaps
    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"): # If uninitialized
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)
        
    def move(self, dx: int, dy: int) -> None:
        # Move the entity by the input amount
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
        self, 
        *, 
        x: int = 0,
        y: int = 0,
        char: str = "?", 
        color: Tuple[int, int, int] = (255, 255, 255), 
        name: str = "<Unnamed>", 
        ai_cls: Type[BaseAI], 
        fighter: Fighter
    ):
        super().__init__(
            x=x, 
            y=y, 
            char=char, 
            color=color, 
            name=name, 
            blocks_movement=True,
            render_order=RenderOrder.ACTOR, 
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

    # Returns True as long as long as this actor can perform actions
    @property
    def is_alive(self) -> bool:
        return bool(self.ai)

        
