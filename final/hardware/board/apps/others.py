### Controller #############################################
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_display_text import label
import displayio
import terminalio
import time

def display_text(hw_state, text):
    main = hw_state["display"].root_group
    val = main.pop()
    #text = "stuff"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    text_group = displayio.Group(scale=2)
    text_group.append(text_area) 
    main.append(text_group)
    text_group.x = 120 #+ int(r * math.sin(theta))
    text_group.y = 120 #+ int(r * math.cos(theta))
        
def controller(hw_state):
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
    display_text(hw_state, "Controller\nMode")
    
    fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
    button_list = fpga_buttons[:5] + hw_state["btn_action"]
    
    keycode_list = [Keycode.LEFT_ARROW, Keycode.UP_ARROW, Keycode.A, Keycode.DOWN_ARROW, Keycode.RIGHT_ARROW, Keycode.ENTER, Keycode.BACKSPACE]
    
    while True:
        for i in range(len(button_list)):
            if i==2: continue
            if button_list[i].value == False:
                keyboard.press(keycode_list[i])
            else:
                keyboard.release(keycode_list[i])
        if button_list[2].value == False:
            return
