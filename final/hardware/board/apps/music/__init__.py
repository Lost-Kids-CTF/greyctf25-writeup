import time
from apps.music.old import *
import board
import adafruit_rtttl

SuperMario = 'Super Mario - Main Theme:d=4,o=5,b=125:a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16f,16p,8c6,8a.,g,16c,a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16a#,16a,16g,2f,16p,8a.,8f.,8c,8a.,f,16g#,16f,16c,16p,8g#.,2g,8a.,8f.,8c,8a.,f,16g#,16f,8c,2c6'
QZKago = ('QZKago:d=4,o=5,b=125:8c,8d,8d#,8g4,8f#4,16g4,8g#4,8d#,16d#,8d,8d#,' +
          '8f,8d#,8d,16d#,8d,8c,16b4,8c,8d,'+
          '8d#,8g#4,16g4,8g#4,8g4,16d#,16d,16d#,8d,8c,8b4,8a4,8b4,c'+
          '8c,8d,8d#,8g4,8f#4,16g4,8g#4,8d#,16d#,8d,8d#,' +
          '8f,8d#,8d,16d#,8d,16c,16c,4g,'+
          '8d#,8g#4,16g4,8g#4,8g4,16g4,16f#4,16g4,16.,16g,16f#,16g,16.,'+
          '16f,16d#,16d,16c,16d,16d#,16f,16b4,4c')
SovietUnion = "tetris:d=4,o=4,b=150:e5,8b,8c5,8d5,15e5,15d5,8c5,8b,a,8a,8c5,e5,8d5,8c5,b,8b,8c5,d5,e5,c5,a,2a,8p,d5,8f5,a5,8g5,8f5,e5,8e5,8c5,e5,8d5,8c5,b,8b,8c5,d5,e5,c5,a,a"
MirrorTune = "mirrortune:d=16,o=5,b=160:32c6,32p,c6,a#5,c6,p,a#5,p,c#6,p,c6,a#5,p,c6,p,a#5,p,32f5,32p,f5,g5,p,f5,p,d5,p,c5,p,a#4,p,c5,p,g4,f4,8p,a#5,c6,p,a#5,p,c#6,p,c6,a#5,p,c6,p,a#5,p,f5,f#5,g5,p,32g6,32p,32g6,32p,32g6,32p,32g6,32p,32g6,32p,32g6,32p,g6,f6,p,g6,4p,a#5,c6,p,a#5,p,c#6,p,c6,a#5,p,c6,p,a#5,p,32f5,32p,f5,g5,p,f5,p,d5,p,c5,p,a#4,p,c5,p,g4,f4,8p,a#5,c6,p,a#5,p,c#6,p,c6,a#5,p,c6,p,a#5,p,f5,f#5,g5,p,f5,f#5,g5,p,f5,f#5,4g5,8p"

def play_rtttl(hw_state, songtext):
    hw_state["buzzer"].deinit()
    adafruit_rtttl.play(board.GP21, songtext)
    hw_state["buzzer"] = hw_state["buzzer_init"]()
    
### Music Menu #############################################################
from adafruit_display_text import label
import displayio
import terminalio
import time

def menu_layout(hw_state, text_in):
    main = hw_state["display"].root_group
    val = main.pop()
    
    header_text_area = label.Label(terminalio.FONT, text="Music Playback\nand Buzzing", color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    #header_text_area.x = 0
    header_text_area.y = -20
    ## Menu Text
    text = text_in
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    #text_area.x = 0
    text_area.y = 15
    
    direction = label.Label(terminalio.FONT, text="< >  A/B", color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    direction.y = 50
    
    text_group = displayio.Group(scale=2)
    text_group.append(header_text_area) 
    text_group.append(text_area) 
    text_group.append(direction) 
    main.append(text_group)
    
    text_group.x = 120 
    text_group.y = 120

def music_app(hw_state):
    #splashscreen()
    
    print("menu")
    curr = 0
    options = [
        ("mario", lambda:play_rtttl(hw_state, SuperMario)),
        ("mirrortune", lambda:play_rtttl(hw_state, MirrorTune)),
        ("sovietunion",lambda:play_rtttl(hw_state, SovietUnion)),
        ("qzkago",lambda:play_rtttl(hw_state, QZKago)),
        ("maimai",lambda:buzz_intro(hw_state)),
        ("eye",lambda:buzz_eye(hw_state)),
    ]
    menu_layout(hw_state, options[curr][0])
    fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
    time.sleep(0.5)
    
    
    trigger = False
    while True:
        # Menu Display Code
        if fpga_buttons[0].value == False:
            curr = (curr - 1) % len(options)
            trigger = True
        if fpga_buttons[4].value == False:
            curr = (curr + 1) % len(options)
            trigger = True
        if trigger:
            menu_layout(hw_state, options[curr][0])
            time.sleep(0.5)
            trigger = False
        
        # Select Code
        if hw_state["btn_action"][0].value == False:
            options[curr][1]()
        if hw_state["btn_action"][1].value == False:
            return

############################################################
song_index = 0
song_total = 2
def buzz(ref):
    global song_index
    if song_index == 0:
        buzz_intro(ref)
    elif song_index == 1:
        buzz_eye(ref)
    song_index = (song_index + 1) % song_total

