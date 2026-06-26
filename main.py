import pyray as pr
import asyncio
import platform
import  input_config as Inputs
from enum import IntFlag
from math import sqrt




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

class Controller(IntFlag):

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

current_object = Inventory.EMPTY

def activate(player,object):
     
    player |=  1 << object

    return player

def deactivate(player,object):
     
    player &= ~(1 << object)

    return player

def evaluate(player,object):
     
    return bool(player & 1 << object)

def player_input(controls):


    #PRESS KEYS
    if pr.is_key_down(Inputs.move_UP) and not pr.is_key_down(Inputs.move_DOWN):
        controls |= 1 << Controller.UP
         

    elif pr.is_key_down(Inputs.move_DOWN) and not pr.is_key_down(Inputs.move_UP):
        controls |= 1 << Controller.DOWN
      

    if pr.is_key_down(Inputs.move_R) and not pr.is_key_down(Inputs.move_L):
        controls |= 1 << Controller.RIGHT      


    elif pr.is_key_down(Inputs.move_L) and not pr.is_key_down(Inputs.move_R):
        controls |= 1 << Controller.LEFT


    #RELEASE KEYS
    if pr.is_key_released(Inputs.move_UP):
        controls &= ~(1<<Controller.UP)

    if pr.is_key_released(Inputs.move_DOWN):
        controls &= ~(1<<Controller.DOWN)    

    if pr.is_key_released(Inputs.move_L):
        controls &= ~(1<<Controller.LEFT)

    if pr.is_key_released(Inputs.move_R):
        controls &= ~(1<<Controller.RIGHT)        

    return controls

def update_player_pos(controls,player_speed):

    mov_x, mov_y = 0,0

    if controls & 1<<Controller.UP:
        mov_y = -1
    if controls & 1<<Controller.RIGHT:
        mov_x = 1
    if controls & 1<<Controller.DOWN:
        mov_y = 1
    if controls & 1<<Controller.LEFT:
        mov_x = -1

    magnitude = sqrt(mov_x**2 + mov_y**2)
    
    if magnitude != 0:
        return ((mov_x/magnitude)*player_speed, 
                (mov_y/magnitude)*player_speed)
    else:
        return (0,0)

def debug_toggle(debug):

    if pr.is_key_pressed(Inputs.debug_ON):

        debug = not debug

    return debug

async def main():

    WIDTH = 1280
    HEIGHT = 720

    debug = False

    player_pos = (100,100)
    player = 0b00000000 #init player
    controls = 0b0000   #init controller
    player_speed = 0.1

    player = activate(player,State.ALIVE)

    pr.init_window(WIDTH, HEIGHT, "Bit Wizard")

    try:
        print("Executing from browser, resizing window...")
        platform.window.window_resize()
    except AttributeError:
        print("Executing from desktop, not resizing...")

 

    print("do you have sword: ",evaluate(player,Inventory.SWORD))
    print("Are you Alive? ",evaluate(player,State.ALIVE))

    while not pr.window_should_close():

        #LOGIC:
        debug = debug_toggle(debug)
        controls = player_input(controls)
        
        player_pos = (player_pos[0]+update_player_pos(controls,player_speed)[0], 
                      player_pos[1]+update_player_pos(controls,player_speed)[1])

                   

        #RENDER:
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)



        pr.draw_text("Bit Wizard", 30, 30, 20, pr.VIOLET)
        pr.draw_text(f"Press O for debug data", 30, 50, 20, pr.DARKGREEN)


        if debug:
                
            pr.draw_text(f"Controller bits: {str(bin(controls))}", 190, 230, 20, pr.VIOLET)
            pr.draw_text(f"Player position: {str(player_pos)}", 190, 260, 20, pr.VIOLET)
            pr.draw_text(f"Movement vector: {str(update_player_pos(controls,player_speed))}", 190, 290, 20, pr.VIOLET)

        pr.end_drawing()
        await asyncio.sleep(0)

    pr.close_window()

asyncio.run(main())