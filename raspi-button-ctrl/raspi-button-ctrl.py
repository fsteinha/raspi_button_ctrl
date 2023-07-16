import os
import time
from time import sleep
from threading import Event
from led import CLed
from button import CButton
from led_pwr_callback import *
import argparse
from argparse import RawTextHelpFormatter
import sys
import textwrap
import RPi.GPIO as GPIO

# Globals
##############################################################################
CONFIG = {
    # power led
    "RASP_POWER_LED":  CLed(led_pwr_cbck_led_init,
                            led_pwr_cbck_on,
                            led_pwr_cbck_off,
                            led_pwr_cbck_state),
    #button
    "BUTTON_CHANNEL": None,
    "BUTTON"        : None,
    # press time configuration
    "PRESS_TIME_CFG"     : {},
}

# callback function for the input event
def button_callback(channel):
    """callback function for gpio event

    Args:
        channel: pressed button input pin
    """
    start = time.perf_counter()
    duty_time_ms = None
    duty_time_ms_tmp = None
    command = None

    while CONFIG['BUTTON'].status(): # and check again the input
        #print (BUTTON.status())
        sleep(0.5)  # confirm the movement by waiting 1.5 sec
        stop = time.perf_counter()
        time_diff = int(stop - start)
        duty_time_ms_tmp = None
        #print(f"{time_diff}")

        for r in CONFIG['PRESS_TIME_CFG'].keys():
            if time_diff in r:
                duty_time_ms_tmp = CONFIG['PRESS_TIME_CFG'][r]['blink_period']
                command = CONFIG['PRESS_TIME_CFG'][r]['command']
                break

        #print (f"{time_diff}  {duty_time_ms_tmp} {duty_time_ms}")
        if (duty_time_ms != None) and (duty_time_ms_tmp == None):
            CONFIG['RASP_POWER_LED'].thread_ctrl_stop_all()
            break
        elif (duty_time_ms == None) and (duty_time_ms_tmp != None):
            duty_time_ms = duty_time_ms_tmp
            CONFIG['RASP_POWER_LED'].thread_ctrl_start_blink(duty_time_ms)
        elif (duty_time_ms_tmp != duty_time_ms):
            duty_time_ms = duty_time_ms_tmp
            CONFIG['RASP_POWER_LED'].set_duty_time_ms(duty_time_ms)

    # LED static on
    CONFIG['RASP_POWER_LED'].on()

    # wait until the button is released
    while CONFIG['BUTTON'].status(): # and check again the input
        sleep(0.5)

    CONFIG['RASP_POWER_LED'].off()
    CONFIG['RASP_POWER_LED'].thread_ctrl_stop_all()
    os.system(f"{command}")

if __name__ == "__main__":
    class MyFormatter(RawTextHelpFormatter):
        def _split_lines(self, text, width):
            return text.splitlines()

    def field_type_int(value):
        return [int(val) for val in (value[0].split(','))]

    def field_type_str(value):
        return value.split(',')

    #if os.getenv('SUDO_USER') is None:
    #    print("Script must run with root rights")
    #    exit()
    
    # arguments
    parser = argparse.ArgumentParser(description='Control service for a user button and display by the power led on the paspberry pi.', formatter_class=MyFormatter)
    parser.add_argument('-i', '--input', dest='input', default='22', type=int,
                        help='Raspberry pi input channel (default: %(default)s)')
    parser.add_argument('-t', '--times', nargs="+", dest='times', type=str, default=['5,10,15'],
                        help='Time within the action shall occure (default: %(default)s)')
    parser.add_argument('-b', '--blink_periods', nargs="+", dest='blink_periods', type=str, default=['500,250,50'],
                        help=textwrap.dedent('''\
                            Blink time periods in ms.
                            The blink time means the time for ON plus the same time for OFF
                            (default: %(default)s).'''))
    parser.add_argument('-c', '--commands', nargs="+", dest='commands', type=str, default=['echo No action 1,echo No action 2,sudo poweroff'],
                        help=textwrap.dedent('''\
                            Action which should proceed, in case the button is release within the given time
                            (default: %(default)s)'''))

    example_text = f"Example: sudo python {sys.argv[0]} -i {parser.get_default('input')} -t {parser.get_default('times')} -b {parser.get_default('blink_periods')} -c {parser.get_default('commands')}"
    example_text += "\n"
    example_text += "CAUTION: Count of blink_periods must be the same like times and commands"
    parser.epilog = example_text
    args = parser.parse_args()

    # print arguments from argpars
    print (f"{sys.argv[0]} was started with:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")

    times = [int(t) for t in args.times[0].split(',')]
    blink_periods = [int(b) for b in args.blink_periods[0].split(',')]
    commands = args.commands[0].split(',')
    
    #print (times)
    #print (blink_periods)
    #print (commands)
    
    # button definition
    CONFIG['BUTTON_CHANNEL'] = args.input
    CONFIG['BUTTON']         = CButton(args.input)

    if (len(times) != len(blink_periods) != len (commands)):
        raise Exception("CAUTION: Count of blink_periods must be the same like times and commands")

    for idx in range(0, len(args.times)):
        if idx == 0:
            last_time = 0
        CONFIG['PRESS_TIME_CFG'][range(last_time, times[idx])] = {'blink_period': blink_periods[idx], 'command':commands[idx]}

    CONFIG['RASP_POWER_LED'].on()
    GPIO.add_event_detect(CONFIG['BUTTON'].gpio_pin, GPIO.RISING, callback=button_callback, bouncetime=10)

    # you can continue doing other stuff here
    Event().wait() # wait until resumed
    pass




