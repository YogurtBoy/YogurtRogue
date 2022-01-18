import tcod 

from engine import Engine
from game_map import GameMap
from entity import Entity
from input_handlers import EventHandler

""" http://rogueliketutorials.com/tutorials/tcod/v2/ """


def main() -> None:
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    map_width = SCREEN_WIDTH
    map_height = SCREEN_HEIGHT - 5

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = EventHandler()

    player = Entity(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), "@", (255, 255, 255))
    npc = Entity(int(SCREEN_WIDTH/2 - 5), int(SCREEN_HEIGHT/2 - 5), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(width=map_width, height=map_height)

    sterling = Engine(entities=entities, 
                      event_handler=event_handler, 
                      game_map=game_map, 
                      player=player)


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
            sterling.handle_events(events=tcod.event.wait())


if __name__ == "__main__":
    main()
