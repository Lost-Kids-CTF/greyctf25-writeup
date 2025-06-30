import board
import busio
import displayio
import digitalio
import gc9a01
import pwmio

### Initialisations
fpga_interconnect_pins = [board.GP8, board.GP9, board.GP10, board.GP11,	board.GP12, board.GP13, board.GP14, board.GP15]
button_pins = [board.GP7, board.GP1]

tft_clk = board.GP2 # must be a SPI CLK
tft_mosi= board.GP3 # must be a SPI TX
tft_rst = board.GP6
tft_dc  = board.GP4
tft_cs  = board.GP5 # optional, can be "None"
tft_bl  = None      # optional, can be "None"


### GC9A01 Display
def rp2350_init_display():
    displayio.release_displays()
    spi = busio.SPI(clock=tft_clk, MOSI=tft_mosi)
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)
    display = gc9a01.GC9A01(display_bus, width=240, height=240, backlight_pin=tft_bl)
    return display, display_bus

### Select Buttons
button_a = digitalio.DigitalInOut(button_pins[0])
button_b = digitalio.DigitalInOut(button_pins[1])
button_a.direction = digitalio.Direction.INPUT
button_b.direction = digitalio.Direction.INPUT

### Buzzer
def buzzer_init():
    return pwmio.PWMOut(board.GP21, variable_frequency=True)
buzzer = buzzer_init()
buzzer.frequency = 440
#buzzer.duty_cycle = ON
BUZZ_ON = 2**15
BUZZ_OFF = 0

