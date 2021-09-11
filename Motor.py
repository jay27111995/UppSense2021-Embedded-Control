import RPi.GPIO as GPIO


class Motor:
    def __init__(self, pump_num: int, frequency: int):
        """
        Create a motor instance
        :param pump_num: Pump number (1 or 2)
        :param frequency: The frequency of the PWM pulse
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        if pump_num == 1:
            self.AN = 12
            self.DIG = 26
        else:
            self.AN = 13
            self.DIG = 24

        GPIO.setup(self.AN, GPIO.OUT)
        GPIO.setup(self.DIG, GPIO.OUT)
        self.pwm = GPIO.PWM(self.AN, frequency)

    def Start(self, direction: bool, duty_cycle: int) -> bool:
        """
        Start the motor.
        :param direction: false - suck from input, true - blow from input
        :param duty_cycle: the duty cycle of the pmw (0-100)
        :return: Success or not
        """

        def boolToGpio(d_bool: bool):
            if d_bool:
                return GPIO.LOW
            else:
                return GPIO.HIGH

        try:
            GPIO.output(self.DIG, boolToGpio(direction))
            self.pwm.start(duty_cycle)
            return True
        except:
            return False

    def Stop(self):
        """
        Stop the motor
        :return: True if success
        """
        try:
            self.pwm.start(0)
            return True
        except:
            return False
