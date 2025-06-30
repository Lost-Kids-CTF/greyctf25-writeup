import hardware.rp2350
import hardware.default_overlay
import displayio

display, display_bus = hardware.rp2350.rp2350_init_display()
display.root_group = displayio.Group()

overlay = hardware.default_overlay.Overlay()

hw_state = {
    # OLED Display
    "display": display, 
    "display_bus": display_bus, 
    # Buttons
    "btn_action": [hardware.rp2350.button_a, hardware.rp2350.button_b], 
    # Buzzer
    "buzzer": hardware.rp2350.buzzer,
    "buzzer_init": hardware.rp2350.buzzer_init,
    # FPGA overlay
    "fpga_overlay": overlay
}


### Display Challenge Info ##################################
from adafruit_display_text import label
import displayio
import terminalio
def display_text(hw_state, text):
    main = hw_state["display"].root_group
    #val = main.pop()
    #text = "stuff"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00,
                            anchor_point=(0.5,0.5), anchored_position=(0,0))
    text_group = displayio.Group(scale=2)
    text_group.append(text_area) 
    main.append(text_group)
    text_group.x = 120 #+ int(r * math.sin(theta))
    text_group.y = 120 #+ int(r * math.cos(theta))