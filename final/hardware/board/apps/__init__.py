from adafruit_display_text import label
import displayio
import terminalio
import time

import apps.face
import apps.brick_game
import apps.others
import apps.music

### Loading Screen ##############################################################
def display_fpga_loading_menu(hw_state):
    main = hw_state["display"].root_group
    # Draw a text label
    text = "Loading\nFPGA..."
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    text_group = displayio.Group(scale=2)
    text_group.append(text_area) 
    main.append(text_group)
    text_group.x = 120 #+ int(r * math.sin(theta))
    text_group.y = 120 #+ int(r * math.cos(theta))
    
    
### Menu #########################################################################
def menu_layout(hw_state, text_in):
    main = hw_state["display"].root_group
    val = main.pop()
    
    header_text_area = label.Label(terminalio.FONT, text="Welcome to \nGreyMecha/Army", color=0xFFFF00,
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

def menu(hw_state):
    #splashscreen()
    #time.sleep(0.5)
    
    print("menu")
    curr = 0
    options = ["Hi I'm Locked In", "Live Firing", "Animation", "Face", "Music", "Brick Game", "Controller"]
    menu_layout(hw_state, options[curr])
    fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
    
    
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
            menu_layout(hw_state, options[curr])
            time.sleep(0.5)
            trigger = False
        
        # Select Code
        if hw_state["btn_action"][0].value == False:
            if options[curr] == "Face":
                apps.face.face_mode(hw_state)
            if options[curr] == "Animation":
                apps.face.face_gif_mode(hw_state)
            if options[curr] == "Live Firing":
                apps.face.live_firing(hw_state)
                fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
            if options[curr] == "Music":
                apps.music.music_app(hw_state)
            if options[curr] == "Brick Game":
                apps.brick_game.brick_game(hw_state)
            if options[curr] == "Controller":
                apps.others.controller(hw_state)
            menu_layout(hw_state, options[curr])
            time.sleep(0.5)
