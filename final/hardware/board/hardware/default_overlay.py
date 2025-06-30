import hardware.fpga
import board
import digitalio
import busio

fpga_interconnect_pins = [board.GP8, board.GP9, board.GP10, board.GP11,	board.GP12, board.GP13, board.GP14, board.GP15]

# GPIO 13, 14, 15 -> mode pins -> output
class Overlay:
    DATA_PINS_NO = [board.GP8, board.GP9, board.GP10, board.GP11, board.GP12]
    MODE_PINS_NO = [board.GP13, board.GP14, board.GP15]
    
    def __init__(self):
        self.mode_set = False
        self.mode_pins = []
        for p in Overlay.MODE_PINS_NO:
            d = digitalio.DigitalInOut(p)
            d.direction = digitalio.Direction.OUTPUT
            self.mode_pins.append(d)
        self.existing_state = None
    
    def init(self):
        self.jtag_rst = hardware.fpga.upload_bitstream("/hardware/bitstreams/main.bit")
        
    def set_mode(self, new_mode):
        for i in range(len(new_mode)):
            self.mode_pins[2-i].value = new_mode[i]
        self.mode_set = True

    def is_current_mode(self, mode):
        if self.mode_set == False:
            return False
        for i in range(len(mode)):
            if self.mode_pins[2-i].value != mode[i]:
                return False
        return True
    
    def set_mode_buttons(self):
        mode_pins = (0, 0, 0)
        if self.is_current_mode(mode_pins):
            return self.existing_state
        self.set_mode(mode_pins)
        
        button_pins = []
        for p in Overlay.DATA_PINS_NO:
            d = digitalio.DigitalInOut(p)
            d.direction = digitalio.Direction.INPUT
            button_pins.append(d)
        self.existing_state = button_pins
        return button_pins
    
    def deinit_mode_buttons(self):
        for p in self.existing_state:
            p.deinit()
        self.mode_set = False
            
    def set_mode_uart(self):
        mode_pins = (0, 1, 1)
        if self.is_current_mode(mode_pins):
            return self.existing_state
        self.set_mode(mode_pins)
        
        ### Hacky Shit to clear pins
        self.set_mode((0, 0, 0))
        for p in Overlay.DATA_PINS_NO:
            d = digitalio.DigitalInOut(p)
            d.direction = digitalio.Direction.OUTPUT
            d.value = False
            d.deinit()
        
        self.set_mode(mode_pins)
        uart = busio.UART(board.GP8, board.GP9, baudrate=9600, timeout=0.1)
        self.existing_state = uart
        return uart
    
    def deinit_mode_uart(self):
        self.existing_state.deinit()
        self.mode_set = False
    
    def deinit(self):
        for p in self.mode_pins:
            p.deinit()