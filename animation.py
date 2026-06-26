

wizard_walk = {"spritesheet": "sprites/bit_walk.png",
                "time"      : [30,30],
                "current_frame": 0,
                "counter": 0 ,
                "current_time": 0,
                "id": "walk"}

wizard_idle = {"spritesheet":  "sprites/bit_idle.png",
                "time"      : [30,5],
                "current_frame": 0,
                "counter": 0  ,
                "current_time": 0 ,
                "id": "idle"}                

shield = {"spritesheet":  "sprites/bit_shield.png",
                "time"      : [30],
                "current_frame": 0,
                "counter": 0   ,
                "current_time": 0 ,
                "id": "shield"}    


sword_atk = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15,18,10],
                "current_frame": 0,
                "counter": 0  ,
                "current_time": 0  ,
                "id": "sword attack"} 

wand_atk = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15,18,10],
                "current_frame": 0 ,
                "counter": 0   ,
                "current_time": 0,
                "id": "wand attack"}       

sword = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15],
                "current_frame": 0 ,
                "counter": 0   ,
                "current_time": 0,
                "id": "sword idle"} 

wand = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15],
                "current_frame": 0 ,
                "counter": 0   ,
                "current_time": 0,
                "id": "wand idle"}       

TOTAL_ANIMATIONS = [wizard_walk,wizard_idle,shield,sword,sword_atk,wand_atk,wand]