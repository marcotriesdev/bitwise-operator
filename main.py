import pyray as pr
import asyncio
import platform
from enum import IntFlag


player =     0b00000000

class State(IntFlag):

    ALIVE  =          0
    WALK   =         1
    ATTK   =        2
    DEFN   =       3

class Inventory(IntFlag):  

    SWORD  =         4
    POTION =        5
    WAND   =       6
    EMPTY  =      7


current_object = Inventory.EMPTY

def activate(object):
    global player
    player |=  1 << object

def deactivate(object):
    global player
    player &= ~(1 << object)

def evaluate(object):
    global player
    return bool(player & 1 << object)

async def main():
    WIDTH = 1280
    HEIGHT = 720




    pr.init_window(WIDTH, HEIGHT, "Bit Wizard")

    try:
        print("Executing from browser, resizing window...")
        platform.window.window_resize()
    except AttributeError:
        print("Executing from desktop, not resizing...")

    #activate(Inventory.SWORD)

    print("do you have sword: ",evaluate(Inventory.SWORD))

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        pr.draw_text("Bit Wizard", 190, 200, 20, pr.VIOLET)
        pr.end_drawing()
        await asyncio.sleep(0)

    pr.close_window()

asyncio.run(main())