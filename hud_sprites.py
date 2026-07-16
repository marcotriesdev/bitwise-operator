from bitflags import *

hud_sword = {"id": "hud sword",
            "file": "sprites/hud_sword.png",
            "bitflag": Inventory.SWORD}

hud_shield = {"id": "hud shield",
            "file": "sprites/hud_shield.png",
            "bitflag": Inventory.SHIELD}

hud_wand = {"id": "hud wand",
            "file": "sprites/hud_wand.png",
            "bitflag": Inventory.WAND}

hud_potion = {"id": "hud potion",
            "file": "sprites/hud_potion.png",
            "bitflag": Inventory.POTION}

hud_empty = {"id": "hud empty",
            "file": "sprites/hud_empty.png",
            "bitflag": Inventory.POTION}

hud_heart = {"id": "hud heart",
            "file": "sprites/heart.png",
            "bitflag": None
            }

hud_selector ={"id": "hud selector",
            "file": "sprites/selector.png",
            "bitflag": None
            }
item_size = 16 #the square size of the sprites

                #never move hud_empty from index 0 or it will break rendering hehe
                #always add to the list when adding a new graphic
TOTAL_SPRITES = [hud_empty,
                hud_shield,
                hud_sword,
                hud_potion,
                hud_wand,
                hud_heart,
                hud_selector]