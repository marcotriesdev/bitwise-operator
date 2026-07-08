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

shield = {"spritesheet": "sprites/bit_shield.png",
                "time"      : [30],
                "counter": 0   ,
                "current_frame": 0 ,
                "id": "shield"}    


sword_atk = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15,18,10],
                "counter": 0  ,
                "current_frame": 0  ,
                "id": "sword attack"} 

wand_atk = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15,18,10],
                "counter": 0   ,
                "current_frame": 0,
                "id": "wand attack"}       

sword = {"spritesheet":  "sprites/bit_sword.png",
                "time"      : [15],
                "counter": 0   ,
                "current_frame": 0,
                "id": "sword idle"} 

wand = {"spritesheet":  "sprites/bit_wand.png",
                "time"      : [15],
                "counter": 0   ,
                "current_frame": 0,
                "id": "wand idle"}       



TOTAL_ANIMATIONS = [wizard_walk,wizard_idle,wizard_death,shield,sword,sword_atk,wand_atk,wand]