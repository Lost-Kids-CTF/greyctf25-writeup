import gc
import hardware
import apps

gc.enable()

### Initialisation ####################################
hw_state = hardware.hw_state
apps.display_fpga_loading_menu(hw_state)
hw_state["fpga_overlay"].init()

### Menu ############################################
apps.menu(hw_state)
