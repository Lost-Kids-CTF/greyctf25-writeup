import gifio, asyncio
import struct, time, random, gc
import displayio
import adafruit_imageload

def load_image(hw_state, img_filename):
    print(img_filename)
    img_bitmap, img_palette = adafruit_imageload.load(img_filename)
    img_tilegrid = displayio.TileGrid(img_bitmap, pixel_shader=img_palette)
    hw_state["display"].root_group.append(img_tilegrid)
    del img_bitmap, img_palette
    gc.collect()

### Load Gif Oneshot ############################################
def load_gif_oneshot(display_bus, filename):
    odg = gifio.OnDiskGif(filename)
    #next_delay = odg.next_frame()  # Load the first frame

    for i in range(odg.frame_count):
        # Direct write to LCD
        next_delay = odg.next_frame()
        time.sleep(next_delay)
        display_bus.send(42, struct.pack(">hh", 0, odg.bitmap.width - 1))
        display_bus.send(43, struct.pack(">hh", 0, odg.bitmap.height - 1))
        display_bus.send(44, odg.bitmap)

def load_gif_oneshot_selective(display_bus, filename, frame_gen=None):
    odg = gifio.OnDiskGif(filename)
    #next_delay = odg.next_frame()  # Load the first frame
    
    if frame_gen == None:
        frame_gen = reversed(range(odg.frame_count))
    for i in frame_gen:
        # damn stupid way to play in reverse
        
        # go forward
        for j in range(i - 1):
            next_delay = odg.next_frame()
        
        next_delay = odg.next_frame()
        # Direct write to LCD
        time.sleep(next_delay)
        display_bus.send(42, struct.pack(">hh", 0, odg.bitmap.width - 1))
        display_bus.send(43, struct.pack(">hh", 0, odg.bitmap.height - 1))
        display_bus.send(44, odg.bitmap)
        
        # go backward
        for j in range(odg.frame_count - i): 
            next_delay = odg.next_frame()

def load_gif_oneshot_reverse(display_bus, filename, frame_gen=None):
    load_gif_oneshot_selective(display_bus, filename, None)