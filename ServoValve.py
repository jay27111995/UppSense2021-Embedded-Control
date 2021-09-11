import RPi.GPIO as GPIO
import pigpio


class TwoWayValve:

    @staticmethod
    def degree_to_pulse_width(degree):
        return round(((degree * 1733.3) / 180.0) + 500, 1)

    def __init__(self):
        self.servo_pin = 8
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.servo_pin, 50)

    def turn(self, angle):
        self.pwm.set_servo_pulsewidth(self.servo_pin, TwoWayValve.degree_to_pulse_width(angle))

    def shut_off(self):
        self.pwm.set_PWM_dutycycle(self.servo_pin, 0)
        self.pwm.set_PWM_frequency(self.servo_pin, 0)
        
    def open_two(self):
        self.turn(130)
        
    def open_one(self):
        self.turn(40)



class ThreeWayValve:

    def degree_to_pulse_width(self, degree):
        return round(((degree * self.offset) / 180.0) + 500, 1)

    def __init__(self, pin, offset):
        # 25, valve-1 ; 8 valve-2
        self.servo_pin = pin
        self.offset = offset
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(self.servo_pin, 50)

    def turn(self, angle):
        self.pwm.set_servo_pulsewidth(self.servo_pin, self.degree_to_pulse_width(angle))

    def shut_off(self):
        self.pwm.set_PWM_dutycycle(self.servo_pin, 0)
        self.pwm.set_PWM_frequency(self.servo_pin, 0)
        
    def open_three(self):
        self.turn(0)        
        
    def open_two(self):
        self.turn(90)
        
    def open_one(self):
        self.turn(170)

