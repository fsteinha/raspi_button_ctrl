"""File for button class
"""
import RPi.GPIO as GPIO

class CButton():
    """button class
    """
    def __init__(self, gpio_pin = 22) -> None:
        """init given gpio as button
        Args:
            gpio_button (int, optional): gpio pin number. Defaults to 22.
        """

        self.gpio_pin = gpio_pin

        # Set GPIO-mode
        GPIO.setmode(GPIO.BCM)

        # Set GPIO-Pin
        GPIO.setup(gpio_pin, GPIO.IN)
        pass

    def status(self):
        """returns the Button status

        Returns:
            int: 0 Button low, 1 Button high
        """
        return GPIO.input(self.gpio_pin)
