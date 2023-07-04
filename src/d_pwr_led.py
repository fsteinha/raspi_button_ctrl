import os
import time



import time
from time import sleep
from threading import Event
from led import CLed
from button import CButton
from led_pwr_callback import *
import RPi.GPIO as GPIO

# Globals
##############################################################################
# power led
PWR_LED = CLed(led_pwr_cbck_led_init,
               led_pwr_cbck_on,
               led_pwr_cbck_off,
               led_pwr_cbck_state)

# button on gpio 22
BUTTON_CHANNEL = 22
BUTTON  = CButton(BUTTON_CHANNEL)
# duty time within the range in [s] the duty time in ms is valid
DUTY_TIME = {
    range(0,1): 500,
    range(1,5): 250,
    range(5,10): 50,
}

def my_callback(channel):
    """callback function for gpio event

    Args:
        channel: pressed button input pin
    """
    start = time.perf_counter()
    duty_time_ms = None
    duty_time_ms_tmp = None

    while BUTTON.status(): # and check again the input
        #print (BUTTON.status())
        sleep(0.5)  # confirm the movement by waiting 1.5 sec
        stop = time.perf_counter()
        time_diff = int(stop - start)
        duty_time_ms_tmp = None
        #print(f"{time_diff}")

        for r in DUTY_TIME.keys():
            if time_diff in r:
                duty_time_ms_tmp = DUTY_TIME[r]
                break

        #print (f"{time_diff}  {duty_time_ms_tmp} {duty_time_ms}")
        if (duty_time_ms != None) and (duty_time_ms_tmp == None):
            duty_time_ms = -1
            PWR_LED.thread_ctrl_stop_all()
            break
        elif (duty_time_ms == None) and (duty_time_ms_tmp != None):
            duty_time_ms = duty_time_ms_tmp
            PWR_LED.thread_ctrl_start_blink(duty_time_ms)
        elif (duty_time_ms_tmp != duty_time_ms):
            duty_time_ms = duty_time_ms_tmp
            PWR_LED.set_duty_time_ms(duty_time_ms)

    # LED static on
    PWR_LED.on()

    # wait until the button is released
    while BUTTON.status(): # and check again the input
        sleep(0.5)

    # Button was press to the end
    if (duty_time_ms == -1):
        # LED static off
        PWR_LED.off()
        print(f"poweroff")
        #os.system("sudo poweroff")


if __name__ == "__main__":
    PWR_LED.on()
    GPIO.add_event_detect(BUTTON.gpio_pin, GPIO.RISING, callback=my_callback, bouncetime=10)

    # you can continue doing other stuff here
    Event().wait() # wait until resumed
    pass




