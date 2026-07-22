from pyray import Rectangle
from bitflags import Inventory

sw_width = 8
sw_height = 12

sword_hitbox = {"width": sw_width,
                "height": sw_height,
                "size": (sw_width,sw_height),
                "bitflag":Inventory.SWORD,
                "Xoffset": 50,
                "Yoffset":-5}