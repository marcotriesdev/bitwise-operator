from bitflags import *

wizard_walk = {"spritesheet": "sprites/bit_walk.png",
                "time"      : [30,30],
                "counter": 0 ,
                "current_frame": 0,
                "id": "walk"}

wizard_idle = {"spritesheet":  "sprites/bit_idle.png",
                "time"      : [360,15,120,15,480,15,60,15],
                "counter": 0  ,
                "current_frame": 0 ,
                "id": "idle"}                

wizard_death = {"spritesheet":  "sprites/bit_die.png",
                "time"      : [30,35,30,30,20,1],
                "counter": 0  ,
                "current_frame": 0 ,
                "id": "death"}         

shield_atk = {"spritesheet": "sprites/bit_shield.png",
                "time"      : [5,30,1],
                "counter": 0   ,
                "current_frame": 0 ,
                "id": "shield use",
                "bitflag":Inventory.SHIELD}    


sword_atk = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15,18,15],
                "counter": 0  ,
                "current_frame": 0  ,
                "id": "sword attack",
                "bitflag":Inventory.SWORD} 
potion_atk = {"spritesheet":  "sprites/bit_potion.png",
                "time"      : [15,30],
                "counter": 0   ,
                "current_frame": 0,
                "id": "potion use",
                "bitflag":Inventory.POTION}       
wand_atk = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15,18,10],
                "counter": 0   ,
                "current_frame": 0,
                "id": "wand attack",
                "bitflag":Inventory.WAND}       

shield = {"spritesheet": "sprites/bit_shield.png",
                "time"      : [30],
                "counter": 0   ,
                "current_frame": 0 ,
                "id": "shield idle",
                "bitflag":Inventory.SHIELD}    


sword = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15],
                "counter": 0   ,
                "current_frame": 0,
                "id": "sword idle",
                "bitflag":Inventory.SWORD} 

potion = {"spritesheet":  "sprites/bit_potion.png",
                "time"      : [15],
                "counter": 0   ,
                "current_frame": 0,
                "id": "potion idle",
                "bitflag":Inventory.POTION}       


wand = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15],
                "counter": 0   ,
                "current_frame": 0,
                "id": "wand idle",
                "bitflag":Inventory.WAND}       

item_size = 16 #the square size of the sprites

TOTAL_ANIMATIONS = (wizard_walk,
                    wizard_idle,
                    wizard_death,                    
                    shield_atk,                   
                    sword_atk,                   
                    potion_atk,
                    wand_atk)

TOTAL_IDLE_ITEMS = (shield,
                    sword,
                    potion,
                    wand)