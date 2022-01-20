""" http://rogueliketutorials.com/tutorials/tcod/v2/ """

import copy

import tcod 

from engine import Engine
from procgen import generate_dungeon
import entity_factories


def main() -> None:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    map_width = SCREEN_WIDTH
    map_height = SCREEN_HEIGHT - 5

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = copy.deepcopy(entity_factories.player)

    sterling = Engine(player=player)

    sterling.game_map = generate_dungeon(
        max_rooms=max_rooms, 
        room_min_size=room_min_size,
        room_max_size=room_max_size, 
        map_width=map_width, 
        map_height=map_height, 
        max_monsters_per_room=max_monsters_per_room,
        engine=sterling)
    sterling.update_fov()

    
    with tcod.context.new_terminal(
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        tileset=tileset, 
        title="Yet Another Roguelike Tutorial", 
        vsync=True, 
    ) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:            
            sterling.render(console=root_console, context=context)
            sterling.event_handler.handle_events()


if __name__ == "__main__":
    main()
