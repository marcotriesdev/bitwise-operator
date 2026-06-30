from enum import IntFlag

class State(IntFlag):

    ALIVE =  0
    WALK  =  1
    ATTK  =  2

class Inventory(IntFlag):  

    SHIELD = 3
    SWORD  = 4
    POTION = 5
    WAND   = 6
    EMPTY  = 7

class Controller(IntFlag):

    UP     = 0
    RIGHT  = 1
    DOWN   = 2
    LEFT   = 3
    USE    = 4
    CHANGE = 5
    MENU   = 6
    