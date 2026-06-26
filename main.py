
import pyray as pr
import asyncio
import platform
import input_config as Inputs
from animation import *
from enum import IntFlag
from math import sqrt

pr.VIOLET = pr.Color(240,180,220,255)

class State(IntFlag):

    ALIVE  =          0
    WALK   =         1
    ATTK   =        2

class Inventory(IntFlag):  

    SHLD   =       3
    SWORD  =      4
    POTION =     5
    WAND   =    6
    EMPTY  =   7

class Controller(IntFlag):

    UP =    0
    RIGHT = 1
    DOWN =  2
    LEFT =  3

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


def draw_rec(w,h,locx,locy):

    pr.draw_rectangle(locx,locy,w,h,pr.SKYBLUE)


def mirror_sprite(controls,mirror):

    if controls & 1<< Controller.RIGHT:
        return 1
    elif controls & 1<< Controller.LEFT:
        return -1

    return mirror



def draw_sprite(spritesheet,rect,posx,posy):
    
    pr.draw_texture_pro(spritesheet,
                        rect,
                        pr.Rectangle(posx,posy,16*10,16*10),
                        pr.Vector2(0,0),
                        0,
                        pr.WHITE)
    

def animate_sprite(resource,posx,posy,controls,mirror):
    
    
    if resource["counter"] < resource["time"][resource["current_time"]]:
        resource["counter"] += 1
    else:
        resource["counter"] = 0
        if resource["current_time"] + 1 < len(resource["time"]):
            resource["current_time"] += 1 
        else:
            resource["current_time"] = 0

    
    rect = pr.Rectangle(resource["current_time"]*16,0,16*mirror_sprite(controls,mirror),16)

    draw_sprite(resource["spritesheet"],rect,posx,posy)

def load_textures(animation_list):

    for anim in animation_list:

        anim["spritesheet"] = pr.load_texture(anim["spritesheet"])
        pr.set_texture_filter(anim["spritesheet"],pr.TEXTURE_FILTER_POINT)

def unload_textures(animation_list):

    unloaded = set()

    for anim in animation_list:
        if id(anim["spritesheet"]) not in unloaded:
            unloaded.add(id(anim["spritesheet"]))
            pr.unload_texture(anim["spritesheet"])
            
def select_player_sprite(controls):


    if controls:

        sprite  = wizard_walk

    else:

        sprite = wizard_idle

    return sprite

async def main():
    
    WIDTH = 1280
    HEIGHT = 720

    debug = False
    controls = 0b0000   #init controller
    mirror = 1
    
    player_pos = (100,100)
    player = 0b00000000 #init player

    player_speed = 2.5

    player = activate(player,State.ALIVE)

    pr.init_window(WIDTH, HEIGHT, "Bit Wizard")

    load_textures(TOTAL_ANIMATIONS)

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
        mirror = mirror_sprite(controls,mirror)
        
        player_pos = (player_pos[0]+update_player_pos(controls,player_speed)[0], 
                      player_pos[1]+update_player_pos(controls,player_speed)[1])

        player_sprite = select_player_sprite(controls)                  
        print(mirror)


        #RENDER:
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)

        animate_sprite(player_sprite,player_pos[0],player_pos[1],controls,mirror)

        pr.draw_text("Bit Wizard", 30, 30, 20, pr.VIOLET)
        pr.draw_text(f"Press O for debug data", 30, 50, 20, pr.DARKGREEN)


        if debug:
            pr.draw_rectangle(80,220,600,200,pr.Color(20,20,20,180))    
            pr.draw_text(f"Controller bits: {str(bin(controls))}", 90, 230, 20, pr.VIOLET)
            pr.draw_text(f"Player position: {str(player_pos)}", 90, 260, 20, pr.VIOLET)
            pr.draw_text(f"Movement vector: {str(update_player_pos(controls,player_speed))}", 90, 290, 20, pr.VIOLET)
            pr.draw_text(("Current animation: " + player_sprite["id"]), 90, 310, 20, pr.VIOLET)
            pr.draw_text(("Current frame: " + str(player_sprite["current_time"])), 90, 340, 20, pr.VIOLET)

        pr.end_drawing()
        await asyncio.sleep(0)

    unload_textures(TOTAL_ANIMATIONS)
    pr.close_window()

asyncio.run(main())