import gifio, asyncio, struct, time, random, os
import gc
from apps.face.load import *

def face_mode(hw_state):
    button_a = hw_state["btn_action"][0]
    button_b = hw_state["btn_action"][1]
    display = hw_state["display"]
    main = display.root_group
    display_bus = hw_state["display_bus"]
    overlay = hw_state["fpga_overlay"]
    buzzer = hw_state["buzzer"]
    fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
    
    time.sleep(0.5)
    val = main.pop()
    del val
    
    ## Rough UI
    prev_fpga_buttons = [x.value for x in fpga_buttons]
    
    files_total = os.listdir("/image")
    files = []
    for f in files_total:
        if ".jpg" in f:
            files.append(f)
    file_index = 0
    print(files)
    load_image(hw_state, "/image/" + files[file_index])
    while True:
        if fpga_buttons[0].value == False: # and fpga_buttons[3].value != prev_fpga_buttons[3]:
            file_index = (file_index-1) % len(files)
            val = main.pop()
            del val
            gc.collect()
            print("Free memory at code point 1: {} bytes".format(gc.mem_free()) )
            load_image(hw_state, "/image/" + files[file_index])
            time.sleep(0.5)
        if fpga_buttons[4].value == False: # and fpga_buttons[3].value != prev_fpga_buttons[3]:
            file_index = (file_index+1) % len(files)
            val = main.pop()
            del val
            load_image(hw_state, "/image/" + files[file_index])
            time.sleep(0.5)
        prev_fpga_buttons = [x.value for x in fpga_buttons]
        if button_a.value == False:
            if hw_state["fpga_overlay"].is_current_mode((0, 1, 1)):
                hw_state["fpga_overlay"].set_mode((0, 0, 0))
            else:
                hw_state["fpga_overlay"].set_mode((0, 1, 1))
            time.sleep(0.5)
        if button_b.value == False:
            hw_state["fpga_overlay"].set_mode((0, 0, 0))
            print("exit")
            break

def face_gif_mode(hw_state):
    time.sleep(0.5)
    button_a = hw_state["btn_action"][0]
    button_b = hw_state["btn_action"][1]
    display = hw_state["display"]
    main = display.root_group
    display_bus = hw_state["display_bus"]
    overlay = hw_state["fpga_overlay"]
    buzzer = hw_state["buzzer"]
    fpga_buttons = hw_state["fpga_overlay"].set_mode_buttons()
    
    files_total = os.listdir("/image")
    files = []
    for f in files_total:
        if ".gif" in f:
            files.append(f)
    file_index = 0
    
    filename = files[file_index]
    odg = gifio.OnDiskGif("/image/"+filename)
    #next_delay = odg.next_frame()  # Load the first frame

    while True:
        # Direct write to LCD
        next_delay = odg.next_frame()
        display_bus.send(42, struct.pack(">hh", 0, odg.bitmap.width - 1))
        display_bus.send(43, struct.pack(">hh", 0, odg.bitmap.height - 1))
        display_bus.send(44, odg.bitmap)
        time.sleep(next_delay)
        
        if fpga_buttons[0].value == False:
            file_index = (file_index-1) % len(files)
            filename = files[file_index]
            print("Free memory at code point 1: {} bytes".format(gc.mem_free()) )
            del odg
            print("Free memory at code point 1: {} bytes".format(gc.mem_free()) )
            odg = gifio.OnDiskGif("/image/"+filename)
            gc.collect()
            print("Free memory at code point 1: {} bytes".format(gc.mem_free()) )
            time.sleep(0.5)
        if fpga_buttons[4].value == False:
            file_index = (file_index+1) % len(files)
            filename = files[file_index]
            del odg
            odg = gifio.OnDiskGif("/image/"+filename)
            gc.collect()
            print("Free memory at code point 2: {} bytes".format(gc.mem_free()) )
            time.sleep(0.5)
        if button_a.value == False:
            time.sleep(0.5)
            if button_a.value == False: # Enable LEDs
                if hw_state["fpga_overlay"].is_current_mode((0, 1, 1)):
                    hw_state["fpga_overlay"].set_mode((0, 0, 0))
                else:
                    hw_state["fpga_overlay"].set_mode((0, 1, 1))
            else: # Pause
                time.sleep(0.5)
                while button_a.value == True:
                    pass
            time.sleep(0.5)
        if button_b.value == False:
            hw_state["fpga_overlay"].set_mode((0, 0, 0))
            print("exit")
            break


expressions = [
    #"face/expressions/greycat_eyes_middle_to_left.gif",
    #"face/expressions/greycat_eyes_middle_to_right.gif",
    #"face/expressions/greycat_cheeks.gif",
    #"face/expressions/greycat_sad.gif",
    #"face/expressions/greycat_angy.gif"
    "lazer"
]

def live_firing(hw_state):
    button_a = hw_state["btn_action"][0]
    button_b = hw_state["btn_action"][1]
    display_bus = hw_state["display_bus"]
    overlay = hw_state["fpga_overlay"]
    buzzer = hw_state["buzzer"]

    play_sound = button_b.value # Press button b to NOT play sound
    
    # Awakening
    #load_gif_oneshot_selective(display_bus, "face/expressions/greycat_awakening.gif", [8])
    load_gif_oneshot(display_bus, "/apps/face/expressions/greycat_awakening.gif")
    overlay.deinit_mode_buttons()
    u = overlay.set_mode_uart()
    
    # Random Choice
    time.sleep(1)
    while button_a.value == True and button_b.value == True:
        expression = expressions[random.randint(0, len(expressions)-1)]
        if expression == "lazer":
            load_gif_oneshot(display_bus, "/apps/face/expressions/greycat_angy.gif")
            load_gif_oneshot_selective(display_bus, "/apps/face/expressions/greycat_lazer_attack.gif", range(4))
            time.sleep(1)
            
            # Lazer Attack
            target = random.randint(0, 7)
            #for i in range(target, target+4): u.write(chr(ord("A")+target))
            load_gif_oneshot_selective(display_bus, "/apps/face/expressions/greycat_lazer_attack.gif", [5])
            buzzer.frequency = 329
            if play_sound:
                buzzer.duty_cycle = 2**15 # BUZZ_ON
            u.write("A" + chr(ord("A")+target) + "A")
    
            time.sleep(1)
            buzzer.duty_cycle = 0 # hardware.BUZZ_OFF
            
            # Resume
            load_gif_oneshot_selective(display_bus, "/apps/face/expressions/greycat_lazer_attack.gif", range(4, 0, -1))
            load_gif_oneshot_reverse(display_bus, "/apps/face/expressions/greycat_angy.gif")
            time.sleep(0.5)
            u.write(b"A`A")
            time.sleep(1)
            continue
        load_gif_oneshot(display_bus, expression)
        time.sleep(1)
        load_gif_oneshot_reverse(display_bus, expression)
        time.sleep(1)
        
    
    # Sleeping
    load_gif_oneshot_reverse(display_bus, "/apps/face/expressions/greycat_awakening.gif")
    #u.write("abcdefg")
    u.deinit()
    