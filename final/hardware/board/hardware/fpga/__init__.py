### ECP5 Programming #####################
#import hardware.fpga.jtag as jtag
from hardware.fpga import ecp5p
from hardware.fpga import ecp5f
import digitalio, board, time

def upload_bitstream(path):
    jtag_rst = digitalio.DigitalInOut(board.GP20)
    jtag_rst.direction = digitalio.Direction.OUTPUT
    #print("0x%08x" % jtag.idcode())
    
    ## Configure Reset Pin
    jtag_rst.value = False
    time.sleep(0.1)
    jtag_rst.value = True
    
    ## Upload Bitsream
    #ecp5f.flash(path)
    ecp5p.prog(path)
    return jtag_rst
