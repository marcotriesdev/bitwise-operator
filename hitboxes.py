from pyray import Rectangle
from bitflags import Inventory

width = 8
height = 12


sword_hitbox = {"width": width,
                "height": height,
                "size": (width,height),
                "bitflag":Inventory.SWORD,
                "Xoffset": 50,
                "Yoffset":-15}