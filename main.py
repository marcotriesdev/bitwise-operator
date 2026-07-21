
import pyray as pr
import asyncio
import platform
from math import sqrt, sin, pi

import bitflags as Bitflags
import input_config as Inputs

import animation as Animation
import collectables as Collectables
import hud_sprites as HUD
import backgrounds as bg
import fonts 

scaling = 6
hud_scaling = scaling * 0.6
bgscaling = scaling * 0.7
item_scaling = scaling * 0.7
pr.VIOLET = pr.Color(240,180,220,255)

shadow_color = pr.Color(2,2,2,200)
empty_hud_color = pr.Color(100,100,75,255)
collision_color = pr.Color(50,50,200,180)



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

def player_input(controls,player):


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

    if (any(pr.is_key_down(key) for key in Inputs.attack)):
        player = activate(player,Bitflags.State.ATTK)


    #RELEASE KEYS
    if any(pr.is_key_released(key) for key in Inputs.move_UP):
        controls &= ~(1<<Bitflags.Controller.UP)

    if any(pr.is_key_released(key) for key in Inputs.move_DOWN):
        controls &= ~(1<<Bitflags.Controller.DOWN)    

    if any(pr.is_key_released(key) for key in Inputs.move_L):
        controls &= ~(1<<Bitflags.Controller.LEFT)

    if any(pr.is_key_released(key) for key in Inputs.move_R):
        controls &= ~(1<<Bitflags.Controller.RIGHT)        

    if any(pr.is_key_released(key) for key in Inputs.attack):
        player &= ~(1<<Bitflags.State.ATTK)        


    return controls, player

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
    
def animate_sprite(resource,posx,posy,controls,mirror):
    
    #SUM 1+ TO COUNTER BASED ON CURRENT FRAME LIMIT INSIDE OF "TIME" ARRAY OF FRAMES
    if resource["counter"] < resource["time"][resource["current_frame"]]:
        #STOP IF THE CURRENT FRAME IS 1 FOR NON LOOPING ANIMATION
        if resource["time"][resource["current_frame"]] != 1:
            
            resource["counter"] += 1
        else:
            #SUM 0 IF THE CURRENT FRAME IS 1 SO ANIMATION STOPS, USED FOR NON LOOPING ANIMATIONS
            resource["counter"] += 0
    else:
        #COUNTER REACHES 0 IF IT REACHES THE CURRENT FRAME LIMIT 
        resource["counter"] = 0
        #ADVANCE THE CURRENT FRAME INDEX WHEN THE COUNTER REACHES MAXIMUM PREVIOUSLY
        if resource["current_frame"] + 1 < len(resource["time"]):
            resource["current_frame"] += 1 
        else:
            # RESTART THE ANIMATION
            resource["current_frame"] = 0
    
    rect = pr.Rectangle(resource["current_frame"]*16,
                        0,
                        16*mirror_sprite(controls,mirror),
                        16)

    return rect
    
def reset_animation(animation):

    if animation["current_frame"] != 0:
        animation["current_frame"] = 0

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
            
def select_player_sprite(controls,player):

    if evaluate(player,Bitflags.State.ALIVE):
        if controls:

            sprite  = Animation.wizard_walk

        else:

            sprite = Animation.wizard_idle

    else:
        sprite = Animation.wizard_death

    return sprite

def spawn_collectable(item,item_list,init_location):
               #pup_item,list,tuple

    new_item            = {}
 
    new_item["locX"]    = init_location[0]
    new_item["locY"]    = init_location[1]   
    new_item["id"]      = item["id"]
    new_item["file"]  = item["file"]
    new_item["bitflag"] = item["bitflag"]
    new_item["rect"] = pr.Rectangle(new_item["locX"],
                                    new_item["locY"],
                                    16*item_scaling,
                                    16*item_scaling)

    item_list.append(new_item)


    return item_list

def draw_collectables(item_list):
    global scaling

    shadow_offset = 20

    for item in item_list:
        
        pr.draw_texture_pro(item["file"],
                            pr.Rectangle(0,0,16,16),
                            pr.Rectangle(item["locX"]+shadow_offset,
                            item["locY"]+shadow_offset,
                            16*item_scaling,
                            16*item_scaling),
                            (0,0),
                            0,
                            shadow_color)
        pr.draw_texture_pro(item["file"],
                            pr.Rectangle(0,0,16,16),
                            pr.Rectangle(item["locX"],
                            item["locY"],
                            16*item_scaling,
                            16*item_scaling),
                            (0,0),
                            0,
                            pr.WHITE)

def collectable_collision(player,player_rect,item_list,player_lives,max_lives):

    for item in item_list:
        if pr.check_collision_recs(player_rect,item["rect"]):
            if not item["id"] == "collectable heart":
                if not evaluate(player, item["bitflag"]):
                    print("collecting item: ",item["id"])
                    player = activate(player,item["bitflag"])
                    print("removing item from collectables item")
                    item_list.remove(item) 
            else:

                if (player_lives < max_lives): player_lives += 1; print("pickup heart"); item_list.remove(item)
                else: print("max hearts reached")

                

                
    return player, player_lives

def draw_player_collision(player_rec):
    global scaling

    pr.draw_rectangle_rec(player_rec,collision_color)

def draw_collectables_collisions(item_list):
    global scaling

    for item in item_list:
        pr.draw_rectangle_rec(item["rect"],collision_color)

def delta_process(delta):

    delta += 0.1

    return delta

def oscillator(delta):

    speed_multiplier = 0.3
    osc= sin(delta*speed_multiplier) 

    return osc

def floaty_collectibles(item_list,delta,intensity):

    for item in item_list:
        item["locY"] += oscillator(delta)*intensity

def hud_render(player,screen_width,screen_height,font,game_title,hearts,current_item):
    global hud_scaling

    hud_locX = screen_width*0.38
    hud_locY = 20
    hearts_spacing = 10
    hearts_locX = hud_locX
    hearts_locY = hud_locY+(HUD.item_size*hud_scaling)+hearts_spacing

    heart_frame_X = 350
    heart_frame_y = hud_locY
    
    frame_thick = 8
    frame_color = pr.Color(150,140,100,255)
    frame_color_bright = pr.Color(180,170,110,255)
    frame_color_dark = pr.Color(75,70,50,255)

    title_color = pr.Color(120,110,70,255)
    title_color_bright = pr.Color(170,160,120,255)
    title_color_dark = pr.Color(90,80,60,255)



    title_locX = frame_thick+60
    title_locY = frame_thick

    #TITLE BOX

    pr.draw_rectangle(0,5,screen_width,int(HUD.item_size*hud_scaling+5),title_color)

    pr.draw_rectangle(0,0,screen_width,int(HUD.item_size*hud_scaling+5),frame_color)

    #EMPTY SPRITE 
    for i in range(4):
        offset = HUD.item_size * i
        pr.draw_texture_pro(HUD.hud_empty["file"],
                            pr.Rectangle(0,0,HUD.item_size,HUD.item_size),
                            pr.Rectangle(hud_locX+(offset*hud_scaling),
                                         hud_locY,
                                         (HUD.item_size*hud_scaling),
                                         (HUD.item_size*hud_scaling)),
                            pr.Vector2(0,0),
                            0.0,
                            empty_hud_color)

        #ITEM SPRITE                        the +1 offset to the index is to skip the empty inventory sprite      
        if evaluate(player,HUD.TOTAL_SPRITES[i+1]["bitflag"]):
            pr.draw_texture_pro(HUD.TOTAL_SPRITES[i+1]["file"],
                                pr.Rectangle(0,0,HUD.item_size,HUD.item_size),
                                pr.Rectangle(hud_locX+(offset*hud_scaling),
                                             hud_locY,
                                             (HUD.item_size*hud_scaling),
                                             (HUD.item_size*hud_scaling)),
                                pr.Vector2(0,0),
                                0.0,
                                pr.WHITE)
        #SELECTOR SPRITE
        if current_item == Bitflags.allItems[i+1]:
            pr.draw_texture_pro(HUD.hud_selector["file"],
                                pr.Rectangle(0,0,HUD.item_size,HUD.item_size),
                                pr.Rectangle(hud_locX+(offset*hud_scaling),
                                            hud_locY,
                                            (HUD.item_size*hud_scaling),
                                            (HUD.item_size*hud_scaling)),
                                pr.Vector2(0,0),
                                0.0,
                                pr.WHITE)

    #HUD ITEM FRAME

    pr.draw_rectangle_lines_ex(pr.Rectangle(hud_locX- frame_thick,
                      hud_locY- frame_thick,
                      (4*(HUD.item_size*hud_scaling)+ frame_thick*2.5),
                      (HUD.item_size*hud_scaling)+ frame_thick*2.5),
                       frame_thick,
                      title_color)

    pr.draw_rectangle_lines_ex(pr.Rectangle(hud_locX- frame_thick,
                      hud_locY- frame_thick,
                      (4*(HUD.item_size*hud_scaling)+ frame_thick*2.0),
                      (HUD.item_size*hud_scaling)+ frame_thick*2.0),
                       frame_thick,
                      frame_color)

    #HEARTS FRAME
    pr.draw_rectangle_gradient_ex(pr.Rectangle(hud_locX- frame_thick+heart_frame_X,
                                               hud_locY- frame_thick,
                                               (3*(HUD.item_size*hud_scaling)+ frame_thick*2.5),
                                               (HUD.item_size*hud_scaling)+ frame_thick*2.5),
                                title_color_bright,
                                title_color_dark,
                                title_color_bright,
                                title_color_dark)


    pr.draw_rectangle_lines_ex(pr.Rectangle(hud_locX- frame_thick+heart_frame_X,
                      hud_locY- frame_thick,
                      (3*(HUD.item_size*hud_scaling)+ frame_thick*2.5),
                      (HUD.item_size*hud_scaling)+ frame_thick*2.5),
                       frame_thick,
                      title_color)

    pr.draw_rectangle_lines_ex(pr.Rectangle(hud_locX- frame_thick+heart_frame_X,
                      hud_locY- frame_thick,
                      (3*(HUD.item_size*hud_scaling)+ frame_thick*2.0),
                      (HUD.item_size*hud_scaling)+ frame_thick*2.0),
                       frame_thick,
                      frame_color)

    #HEARTS
    for i in range(hearts):
        offset = i*HUD.item_size

        pr.draw_texture_pro(HUD.hud_heart["file"],
                            pr.Rectangle(0,0,HUD.item_size,HUD.item_size),
                            pr.Rectangle(hearts_locX+(offset*hud_scaling)+(hearts_spacing*i)+heart_frame_X+5,
                                        heart_frame_y,
                                        HUD.item_size*hud_scaling*0.60,
                                        HUD.item_size*hud_scaling*0.8),
                                pr.Vector2(0,0),
                                0.0,
                                pr.WHITE)


    #SCREEN FRAME
    pr.draw_rectangle_lines_ex(pr.Rectangle(0,0,screen_width,screen_height),
                                frame_thick,
                               frame_color)   



    #HUD TITLE
    pr.draw_text_ex(font,
                    game_title,
                    pr.Vector2(title_locX+2,title_locY+2),
                    60,
                    2,
                    title_color_dark)

    pr.draw_text_ex(font,
                    game_title,
                    pr.Vector2(title_locX-2,title_locY-2),
                    60,
                    2,
                    title_color_bright)
             
    pr.draw_text_ex(font,
                    game_title,
                    pr.Vector2(title_locX,title_locY),
                    60,
                    2,
                    title_color)

#DEPRECATED:
def limit_lives(player_lives):

    if player_lives > 3:
        print("limiting player lives to 3")
        player_lives = 3
    
    if player_lives < 0:
        player_lives = 0

    return player_lives

def dead_alpha(title_alpha,counter,title_speed):
    #print(title_alpha)
    if counter < title_speed:
        counter += 1
    else:
        counter = 1
        if title_alpha < 255:
            title_alpha += 1

    #print(counter)
    return title_alpha, counter

def draw_dead_menu(screen_w,screen_h,font,title_alpha):

    #DRAW INSTRUCTION

    if title_alpha > 130:
        pr.draw_text_ex(font,
                        "Press <R> to resuscitate",
                        pr.Vector2(200+150,250+200),
                        50,5,
                        pr.Color(180,180,120,255)
                        )

    #DRAW TITLE

    pr.draw_text_ex(font,
                    "To die unprepared.\n In a state of sin...",
                    pr.Vector2(200-3,250-3),
                    100,10,
                    pr.Color(5,0,0,title_alpha))

    pr.draw_text_ex(font,
                    "To die unprepared.\n In a state of sin...",
                    pr.Vector2(200,250),
                    100,10,
                    pr.Color(255,10,30,title_alpha))
        
def player_take_damage(player_lives):

    #USEFUL ONLY FOR DEBUGGIN'
    if pr.is_key_pressed(pr.KEY_T):
        player_lives -= 1

    return player_lives

def revive_player(player,player_lives,title_alpha):

    if title_alpha > 140 and pr.is_key_pressed(pr.KEY_R):
        player = activate(player,Bitflags.State.ALIVE)
        player_lives = 3
        title_alpha = 0

    return player, player_lives, title_alpha

def check_lives(player_lives,player):
    if not player_lives:
        player = deactivate(player,Bitflags.State.ALIVE)

    return player

def spawn_bulk_collectables(object_list,*args):

    for item_tuple in args:
        #                collect enum, object_list, positions     
        spawn_collectable(item_tuple[0],object_list,item_tuple[1])

def draw_active_item(current_item,player_position,controls,mirror,player):
    global scaling
    #This is currently not very data driven of me but a mere ducktaped answer to unorganized data.
    sprite = None 
    animated_sprite = None

    match current_item:

        case Bitflags.Inventory.SHIELD:
            sprite = Animation.shield
            animated_sprite = Animation.shield_atk

        case Bitflags.Inventory.SWORD:
            sprite = Animation.sword
            animated_sprite = Animation.sword_atk

        case Bitflags.Inventory.POTION:
            sprite = Animation.potion
            animated_sprite = Animation.potion_atk  

        case Bitflags.Inventory.WAND:
            sprite = Animation.wand
            animated_sprite = Animation.wand_atk

        case Bitflags.Inventory.EMPTY:
            sprite = None
            animated_sprite = None

    # Draw static item sprite when not attacking
    if sprite != None and evaluate(player,sprite["bitflag"]): # if there's a sprite not empty and player bit has current item 
        if not evaluate(player,Bitflags.State.ATTK):          # if not attacking
            reset_animation(animated_sprite)
            pr.draw_texture_pro(sprite["spritesheet"],
                                pr.Rectangle(0,0,Animation.item_size*mirror_sprite(controls,mirror),Animation.item_size),
                                pr.Rectangle(player_position[0],player_position[1],Animation.item_size*scaling,Animation.item_size*scaling),
                                pr.Vector2(0,0),
                                0.0,
                                pr.WHITE)

        #Animate and draw the item animation       
        else:
            
            pr.draw_texture_pro(animated_sprite["spritesheet"],
                                animate_sprite(animated_sprite,
                                               player_position[0],
                                               player_position[1],
                                               controls,mirror),
                                pr.Rectangle(player_position[0],player_position[1],Animation.item_size*scaling,Animation.item_size*scaling),
                                pr.Vector2(0,0),
                                0.0,
                                pr.WHITE)

def defend_shield():
    pass
def attack_sword():
    pass
def attack_wand():
    pass

def use_active_item(current_item,controls,mirror,player,player_lives):

    if evaluate(player,Bitflags.State.ATTK) and evaluate(player,current_item):
        match current_item:
            case Bitflags.Inventory.SHIELD:
                defend_shield()
            case Bitflags.Inventory.SWORD:
                attack_sword()
            case Bitflags.Inventory.POTION:
                player_lives = 3
                deactivate(player,Bitflags.Inventory.POTION)
            case Bitflags.Inventory.WAND:
                attack_wand()

    return player, player_lives

def select_item(current_item):

    if any(pr.is_key_pressed(key) for key in Inputs.select):
        if current_item + 1 < Bitflags.emptyItem+1:
            current_item += 1
        else:
            current_item = Bitflags.firstItem

    return current_item


async def main():

    web_resizing_test()

    WIDTH = 1280
    HEIGHT = 720
    game_title = "> Bit Wizard <"

    delta = 0

    global scaling
    global bgscaling

    debug_window_x = 30
    debug_window_y = 60
    debug_margin_text = 35

    pr.init_window(WIDTH, HEIGHT, "Bit Wizard")    

    debug = False
    controls = 0b0000   #init controller
    player = 0b00000000 #init player state and inventory in one byte
    player = activate(player,Bitflags.State.ALIVE)

    mirror = 1

    player_lives = 2
    player_max_lives = 3
    player_active_item = Bitflags.Inventory.EMPTY
    player_speed = 2.5
    player_pos = (250,250)
    player_size = 16
    player_rect = pr.Rectangle(player_pos[0],
                               player_pos[1],
                               player_size*scaling,
                               player_size*scaling)
    
    collectables_list = []
    enemies_list      = [] #not implemented yet hehe!

    background1 = load_background(bg.background_rocks)
    load_animations(Animation.TOTAL_ANIMATIONS)
    load_animations(Animation.TOTAL_IDLE_ITEMS)
    load_static_sprites(Collectables.TOTAL_SPRITES)
    load_static_sprites(HUD.TOTAL_SPRITES)
    font1 = pr.load_font(fonts.medieval_font["file"])

    dead_title_alpha = 0
    dead_title_counter = 1
    deat_title_speed = 3
    
    #SPAWN COLLECTABLES

    spawn_bulk_collectables(collectables_list,
                            (Collectables.pup_sword,(350,250)),
                            (Collectables.pup_potion,(350,420)),
                            (Collectables.pup_wand,(150,520)),
                            (Collectables.pup_shield,(650,620)),
                            (Collectables.pup_heart,(700,200))
                            )

    while not pr.window_should_close():

        #LOGIC
        delta = delta_process(delta)

        floaty_collectibles(collectables_list,delta,0.2)

        debug = debug_toggle(debug)
        player_lives = player_take_damage(player_lives)

        player = check_lives(player_lives,player)
        player_active_item = select_item(player_active_item)
        player, player_lives = use_active_item(player_active_item,controls,mirror,player,player_lives) 

        #EVALUATE IF PLAYER IS DEAD OR NOT. DEATH TITLE MENU PLAYS HERE
        if evaluate(player,Bitflags.State.ALIVE):
            controls, player = player_input(controls,player)
            mirror = mirror_sprite(controls,mirror)
            reset_animation(Animation.wizard_death)
        else:
            controls = 0b0
            dead_title_alpha, dead_title_counter = dead_alpha(dead_title_alpha,
                                                              dead_title_counter,
                                                              deat_title_speed)    

            player, player_lives, dead_title_alpha = revive_player(player,
                                                                   player_lives,
                                                                   dead_title_alpha)
        
        player_pos = (player_pos[0]+update_player_pos(controls,player_speed)[0], 
                      player_pos[1]+update_player_pos(controls,player_speed)[1])

        player_rect = pr.Rectangle(player_pos[0],
                                   player_pos[1],
                                   player_size*scaling,
                                   player_size*scaling)

        player_sprite = select_player_sprite(controls,player)
        #print("lives:", player_lives)

        #COLLISION LOGIC
        player, player_lives = collectable_collision(player,player_rect,collectables_list,player_lives,player_max_lives)

        #RENDER
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        
        #RENDER BACKGROUND
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
        
        draw_sprite(player_sprite["spritesheet"],
                    animate_sprite(player_sprite,player_pos[0],player_pos[1],controls,mirror), #calculates current 
                    player_pos[0],                                                             #animation frame     
                    player_pos[1])
        #RENDER ACTIVE ITEM
        draw_active_item(player_active_item,player_pos,controls,mirror,player)

        #HUD RENDER duuuh!
        hud_render(player,WIDTH,HEIGHT,font1,game_title,player_lives,player_active_item)
        pr.draw_text(f"Press O for debug data", 50, 680, 20, pr.GREEN)
        pr.draw_text(f"WASD OR ARROWS TO MOVE", 50, 70, 20, pr.GREEN)
        pr.draw_text(f"PICKUP STUFF, SELECT WITH SHIFT KEY", 50, 90, 20, pr.GREEN)
        pr.draw_text(f"AND ATTACK WITH SPACE KEY", 50, 110, 20, pr.GREEN)

        #DEAD SCREEN
        draw_dead_menu(WIDTH,HEIGHT,font1,dead_title_alpha)

        #DEBUG INFO
        if debug:
            draw_player_collision(player_rect)
            draw_collectables_collisions(collectables_list)
            pr.draw_rectangle(debug_window_x,
                                debug_window_y,
                                600,200,
                                pr.Color(20,20,20,180))   
 
            pr.draw_text(f"Player Byte: {str(bin(player))}",
                         debug_window_x, 
                         debug_window_y, 
                         20, 
                         pr.VIOLET)

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

            pr.draw_text(("Current frame: " + str(player_sprite["current_frame"])), 
                        debug_window_x,debug_window_y+(debug_margin_text*5), 
                        20, 
                        pr.VIOLET)
            pr.draw_text(f"Player active Item: {player_active_item}",
                         debug_window_x,debug_window_y+(debug_margin_text*6),
                         20,
                         pr.VIOLET)
            pr.draw_text(f"Attacking?: {bool(evaluate(player,Bitflags.State.ATTK))}",
                         debug_window_x,debug_window_y+(debug_margin_text*7),
                         20,
                         pr.RED)

        pr.end_drawing()
        await asyncio.sleep(0)

    unload_animations(Animation.TOTAL_ANIMATIONS)
    unload_static_sprites(Collectables.TOTAL_SPRITES)
    unload_static_sprites(HUD.TOTAL_SPRITES)
    pr.unload_texture(background1)

    pr.close_window()

asyncio.run(main())