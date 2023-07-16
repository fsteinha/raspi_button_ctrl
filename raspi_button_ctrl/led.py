""" class for control a led - at default the power led of the raspberry pi

    author:     Fred Steinhaeuser
    copyright:  no copyright claimed
    licence:    free
"""

import threading
from time import sleep
import argparse
from led_pwr_callback import *

# class definition
##############################################################################
class CLed():
    """ class for control the led
        Follow features are provide:
            - thread for blinking,
            - on, off, toggle
            - callbacks fuction for init, on and off a led
        At default the power led for the rasberry pi 4 are provied
    """

    def __init__(self, calbck_init,
                       calbck_on,
                       calbck_off,
                       calbck_stat) -> None:
        """set PWR_LED to gpio mode
        """
        # det the callbacks
        self.calbck_on = calbck_on
        assert(self.calbck_on != None)

        self.calbck_off = calbck_off
        assert(self.calbck_off != None)

        self.calbck_stat = calbck_stat
        assert(self.calbck_stat != None)

        if calbck_init != None:
            calbck_init()

        # set the thread
        self.thread = None
        self.thread_ctrl_stop = True

        #set the default duty time in ms
        self.set_duty_time_ms(500)
        pass

    def set_duty_time_ms(self, duty_time_ms):
        """function for setting the duty time

        Args:
            duty_time_ms (_type_): time in ms (for on + for off)
        """
        self.duty_time_ms = duty_time_ms
        #print (f"set duty time {self.duty_time_ms}")
        pass

    def toggle(self):
        """provides a toggle
        """
        led_state = self.calbck_stat()

        if led_state == True:
            self.off()
        else:
            self.on()

    def on(self):
        """provides a led on
        """
        self.calbck_on()

    def off(self):
        """provides a led off
        """
        self.calbck_off()


    def thread_ctrl_start_blink(self, duty_time_ms:int = 500):
        """starts a thread for bliking the led

        Args:
            freq (int, optional): blinl in Hz. Defaults to 1.
        """
        self.set_duty_time_ms(duty_time_ms)

        if self.duty_time_ms > 0:
            if self.thread != None and self.thread_ctrl_stop != False:
                self.thread_ctrl_stop = True
                self.thread.join()

            self.thread_ctrl_stop = False

            self.thread = threading.Thread(target=self.thread_func_blink)
            self.thread.start()


    def thread_ctrl_stop_all(self):
        """stops all running threads
        """
        self.thread_ctrl_stop = True
        pass

    def thread_func_blink(self):
        """thread function for blinking

        Args:
            freq (int): _description_
        """

        while(self.thread_ctrl_stop == False):
            self.toggle()
            sleep(float(self.duty_time_ms)/1000)
        print ("Thread ends")

# run as standallone
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Control the led')
    parser.add_argument('command', choices = ['on', 'off', 'toggle'])
    args = parser.parse_args()

    led = CLed(led_pwr_cbck_led_init,
               led_pwr_cbck_on,
               led_pwr_cbck_off,
               led_pwr_cbck_state)

    # Greife auf das übergebene Positional Argument zu
    if (args.command == 'on'):
        led.on()
        pass
    elif (args.command == 'off'):
        led.off()
        pass
    elif (args.command == 'toggle'):
        while True:
            sleep(0.5)
            led.toggle()



