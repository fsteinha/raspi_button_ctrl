import os
import subprocess


# default call backs for led calls
##############################################################################
def led_pwr_cbck_led_init():
    """callback for init the led
    """
    #print("default_calbck_led_init")
    os.system(f"sudo echo gpio > /sys/class/leds/led1/trigger")

def led_pwr_cbck_on():
    """callback for switch the led on
    """
    #print("default_calbck_on")
    #os.system(f"echo 1 | sudo tee /sys/class/leds/led1/brightness")
    os.system(f"sudo echo 1 > /sys/class/leds/led1/brightness")

def led_pwr_cbck_off():
    """callback for switch led off
    """
    #print("default_calbck_off")
    #os.system(f"echo 0 | sudo tee /sys/class/leds/led1/brightness")
    os.system(f"sudo echo 0 > /sys/class/leds/led1/brightness")

def led_pwr_cbck_state():
    """callback for read the state of led

    Returns:
        bool: True - Led on, False - LEd off
    """
    #print("default_calbck_state")
    led_state = subprocess.getoutput("sudo cat /sys/class/leds/led1/brightness")
    if int(led_state) > 0:
        return True
    return False
