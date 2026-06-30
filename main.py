
import pyray as pr
import asyncio
import platform
import input_config as Inputs
import animation as Animation
import collectables as Collectables
import backgrounds as bg
import bitflags as Bitflags
from math import sqrt



scaling = 8
bgscaling = scaling * 0.6
pr.VIOLET = pr.Color(240,180,220,255)

shadow_color = pr.Color(2,2,2,200)
collision_color = pr.Color(50,50,200,180)

current_object = Bitflags.Inventory.EMPTY

def web_resizing_test():
    try:
        print("Executing from browser, resizing window...")
        platform.window.window_resize()
    except AttributeError:
        print("Executing from desktop, not resizing...")

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
    if          (any(pr.is_key_down(key) for key in Inputs.move_UP) 
        and not any(pr.is_key_down(key2) for key2 in Inputs.move_DOWN)):
        controls |= 1 << Bitflags.Controller.UP
         

    elif            (any(pr.is_key_down(key) for key in Inputs.move_DOWN) 
        and not any(pr.is_key_down(key2) for key2 in Inputs.move_UP)):
        controls |= 1 << Bitflags.Controller.DOWN
      

    if           (any(pr.is_key_down(key) for key in Inputs.move_R) 
        and not any(pr.is_key_down(key2) for key2 in Inputs.move_L)):
        controls |= 1 << Bitflags.Controller.RIGHT      


    elif        (any(pr.is_key_down(key) for key in Inputs.move_L) 
        and not any(pr.is_key_down(key2) for key2 in Inputs.move_R)):
        controls |= 1 << Bitflags.Controller.LEFT



    #RELEASE KEYS
    if any(pr.is_key_released(key) for key in Inputs.move_UP):
        controls &= ~(1<<Bitflags.Controller.UP)

    if any(pr.is_key_released(key) for key in Inputs.move_DOWN):
        controls &= ~(1<<Bitflags.Controller.DOWN)    

    if any(pr.is_key_released(key) for key in Inputs.move_L):
        controls &= ~(1<<Bitflags.Controller.LEFT)

    if any(pr.is_key_released(key) for key in Inputs.move_R):
        controls &= ~(1<<Bitflags.Controller.RIGHT)        

    return controls

def update_player_pos(controls,player_speed):

    mov_x, mov_y = 0,0

    if controls & 1<<Bitflags.Controller.UP:
        mov_y = -1
    if controls & 1<<Bitflags.Controller.RIGHT:
        mov_x = 1
    if controls & 1<<Bitflags.Controller.DOWN:
        mov_y = 1
    if controls & 1<<Bitflags.Controller.LEFT:
        mov_x = -1

    magnitude = sqrt(mov_x**2 + mov_y**2)
    
    if magnitude != 0:
        return ((mov_x/magnitude)*player_speed, 
                (mov_y/magnitude)*player_speed)
    else:
        return (0,0)

def debug_toggle(debug):

    if any(pr.is_key_pressed(key) for key in Inputs.debug_ON):

        debug = not debug

    return debug

def draw_rec(w,h,locx,locy):

    pr.draw_rectangle(locx,locy,w,h,pr.SKYBLUE)

def mirror_sprite(controls,mirror):

    if controls & 1<< Bitflags.Controller.RIGHT:
        return 1
    elif controls & 1<< Bitflags.Controller.LEFT:
        return -1

    return mirror

def draw_sprite(spritesheet,rect,posx,posy):
    global scaling
    pr.draw_texture_pro(spritesheet,
                        rect,
                        pr.Rectangle(posx,posy,16*scaling,16*scaling),
                        pr.Vector2(0,0),
                        0,
                        pr.WHITE)
    
def animate_draw_sprite(resource,posx,posy,controls,mirror):
    
    
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

def load_animations(animation_list):

    for anim in animation_list:

        anim["spritesheet"] = pr.load_texture(anim["spritesheet"])
        pr.set_texture_filter(anim["spritesheet"],pr.TEXTURE_FILTER_POINT)

def load_static_sprites(sprite_list):

    for item in sprite_list:
        item["file"] = pr.load_texture(item["file"])
        pr.set_texture_filter(item["file"],pr.TEXTURE_FILTER_POINT)

def load_background(resource):

    background = pr.load_texture(resource)
    pr.set_texture_wrap(background,pr.TEXTURE_WRAP_REPEAT)

    return background

def unload_animations(animation_list):

    unloaded = set()

    for anim in animation_list:
        if id(anim["spritesheet"]) not in unloaded:
            unloaded.add(id(anim["spritesheet"]))
            print("unloaded successfully: ",anim)
            pr.unload_texture(anim["spritesheet"])

def unload_static_sprites(sprite_list):

    unloaded = set()
    for item in sprite_list:
        if id(item["file"]) not in unloaded:
            unloaded.add(id(item["file"]))
            print("unloaded sprite successfully: ",item)
            pr.unload_texture(item["file"])
            
def select_player_sprite(controls):


    if controls:

        sprite  = Animation.wizard_walk

    else:

        sprite = Animation.wizard_idle

    return sprite

def spawn_collectable(item,item_list,init_location):
               #pup_item,list,tuple

    new_item            = {}
 
    new_item["locX"]    = init_location[0]
    new_item["locY"]    = init_location[1]   
    new_item["id"]      = item["id"]
    new_item["file"]  = item["file"]
    new_item["bitflag"] = item["bitflag"]

    item_list.append(new_item)


    return item_list

def draw_collectables(item_list):
    global scaling

    shadow_offset = 20

    for item in item_list:
        
        pr.draw_texture_pro(item["file"],
                            pr.Rectangle(0,0,16,16),
                            pr.Rectangle(item["locX"]+shadow_offset,item["locY"]+shadow_offset,16*scaling,16*scaling),
                            (0,0),
                            0,
                            shadow_color)
        pr.draw_texture_pro(item["file"],
                            pr.Rectangle(0,0,16,16),
                            pr.Rectangle(item["locX"],item["locY"],16*scaling,16*scaling),
                            (0,0),
                            0,
                            pr.WHITE)

def collectable_collision():
    pass

def draw_player_collision(player_position):
    global scaling

    pr.draw_rectangle(int(player_position[0]),
                      int(player_position[1]),
                      16*scaling,
                      16*scaling,
                      collision_color)

def draw_collectables_collisions(item_list):
    global scaling

    for item in item_list:
        pr.draw_rectangle(item["locX"],item["locY"],16*scaling,16*scaling,collision_color)

async def main():

    web_resizing_test()

    WIDTH = 1280
    HEIGHT = 720

    global scaling
    global bgscaling

    debug_window_x = 30
    debug_window_y = 60
    debug_margin_text = 35

    pr.init_window(WIDTH, HEIGHT, "Bit Wizard")    

    #offset = 0

    debug = False
    controls = 0b0000   #init controller
    player = 0b00000000 #init player state and inventory in one byte
    player = activate(player,Bitflags.State.ALIVE)
    mirror = 1

    player_speed = 2.5
    player_pos = (50,50)
    player_size = 16
    
    collectables_list = []
    enemies_list      = []

    background1 = load_background(bg.background_rocks)
    load_animations(Animation.TOTAL_ANIMATIONS)
    load_static_sprites(Collectables.TOTAL_SPRITES)
    
    #SPAWN COLLECTABLES
    spawn_collectable(Collectables.pup_sword,
                collectables_list,
                (250,250))


    #CHANGE FOR AN ACTUAL GUI INVENTORY
    print("do you have sword: ",evaluate(player,Bitflags.Inventory.SWORD))
    print("Are you Alive? ",evaluate(player,Bitflags.State.ALIVE))

    while not pr.window_should_close():

        #LOGIC:
        debug = debug_toggle(debug)
        controls = player_input(controls)
        mirror = mirror_sprite(controls,mirror)
        
        player_pos = (player_pos[0]+update_player_pos(controls,player_speed)[0], 
                      player_pos[1]+update_player_pos(controls,player_speed)[1])

        player_sprite = select_player_sprite(controls)                  

        #RENDER
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        
        #RENDER BACKGROUND
        #offset += 1
        pr.draw_texture_pro(background1,
                            pr.Rectangle(0,0,WIDTH,HEIGHT),
                            pr.Rectangle(0,0,WIDTH*(bgscaling),
                            HEIGHT*(bgscaling)),
                            (0,0),
                            0,
                            pr.Color(100,100,100,255))
        #RENDER COLLECTABLES
        draw_collectables(collectables_list)

        #RENDER PLAYER
        animate_draw_sprite(player_sprite,player_pos[0],player_pos[1],controls,mirror)

        #GUI TEXT
        pr.draw_text("Bit Wizard", 30, 30, 20, pr.VIOLET)
        pr.draw_text(f"Press O for debug data", 30, 50, 20, pr.DARKGREEN)


        if debug:
            draw_player_collision(player_pos)
            draw_collectables_collisions(collectables_list)
            pr.draw_rectangle(debug_window_x,
                                debug_window_y,
                                600,200,
                                pr.Color(20,20,20,180))   

            pr.draw_text(f"Controller bits: {str(bin(controls))}",
                         debug_window_x, 
                         debug_window_y+debug_margin_text, 
                         20, 
                         pr.VIOLET)

            pr.draw_text(f"Player position: {str(player_pos)}", 
                        debug_window_x, 
                        debug_window_y+(debug_margin_text*2), 
                        20, 
                        pr.VIOLET)

            pr.draw_text(f"Movement vector: {str(update_player_pos(controls,player_speed))}", 
                        debug_window_x, 
                        debug_window_y+(debug_margin_text*3), 
                        20, 
                        pr.VIOLET)

            pr.draw_text(("Current animation: " + player_sprite["id"]), 
                        debug_window_x,
                        debug_window_y+(debug_margin_text*4), 
                        20, 
                        pr.VIOLET)

            pr.draw_text(("Current frame: " + str(player_sprite["current_time"])), 
                        debug_window_x,debug_window_y+(debug_margin_text*5), 
                        20, 
                        pr.VIOLET)

        pr.end_drawing()
        await asyncio.sleep(0)

    unload_animations(Animation.TOTAL_ANIMATIONS)
    unload_static_sprites(Collectables.TOTAL_SPRITES)
    pr.unload_texture(background1)

    pr.close_window()

asyncio.run(main())