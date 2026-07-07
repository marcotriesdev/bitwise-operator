from bitflags import *

pup_sword = {"id": "collectable sword",
            "file": "sprites/pup_sword.png",
            "bitflag": Inventory.SWORD}

pup_shield = {"id": "collectable shield",
            "file": "sprites/pup_shield.png",
            "bitflag": Inventory.SHIELD}

pup_wand = {"id": "collectable wand",
            "file": "sprites/pup_wand.png",
            "bitflag": Inventory.WAND}

pup_potion = {"id": "collectable potion",
            "file": "sprites/pup_potion.png",
            "bitflag": Inventory.POTION}

pup_heart = {"id": "collectable heart",
            "file": "sprites/heart.png",
            "bitflag": None}


TOTAL_SPRITES = [pup_sword,pup_shield,pup_wand,pup_potion,pup_heart]