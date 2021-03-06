# Handle the loading and initialization of game sessions
from __future__ import annotations

import copy
import lzma
import pickle 
import traceback 
from typing import Optional

import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers


# Load the background image and remove the alpha channel
background_image = tcod.image.load("menu_background.png")[:, :, :3]


# Return a brand new game session as an Engine instance
def new_game() -> Engine:
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    sterling = Engine(player = player)

    sterling.game_world = GameWorld(engine=sterling,
                                    max_rooms=max_rooms,
                                    room_min_size=room_min_size,
                                    room_max_size=room_max_size,
                                    map_width=map_width,
                                    map_height=map_height)
    sterling.game_world.generate_floor()
    sterling.update_fov()

    sterling.message_log.add_message("Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text)

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message = False)
    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message = False)
    
    return sterling

# Load an engine instance from a file
def load_game(filename: str) -> Engine:
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    # Render the main menu on a background image
    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)

        console.print(console.width // 2,
                      console.height // 2 - 4, 
                      "TOMBS OF THE ANCIENT KINGS", 
                      fg = color.menu_title, 
                      alignment = tcod.CENTER)
        console.print(console.width // 2,
                      console.height - 2, 
                      "By (your name here)", 
                      fg = color.menu_title, 
                      alignment = tcod.CENTER)
        
        menu_width = 24
        for i, text in enumerate(["[N] Play a new game", 
                                  "[C] Continue last game", 
                                  "[Q] Quit"]):
            console.print(console.width // 2,
                          console.height // 2 - 2 + i, 
                          text.ljust(menu_width), 
                          fg = color.menu_text,
                          bg = color.black, 
                          alignment = tcod.CENTER,
                          bg_blend = tcod.BKGND_ALPHA(64))
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f"Failed to load save: \n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None

