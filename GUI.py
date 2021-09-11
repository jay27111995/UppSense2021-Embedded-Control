from tkinter import *

from Motor import Motor
# from readQRandSendResult import readQRCodeAndSendResult
from ServoValve import *


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.valve2 = ThreeWayValve(8, 2000)
        self.valve3 = ThreeWayValve(25, 1750)
        self.pump_1 = Motor(1, 3000)
        self.pump_2 = Motor(2, 3000)
        self.pump2_speed = 2
        self.pump1_speed = 6

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("UppSense H1N1 Biosensor - Developed in Uppsala University, Sweden")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Buttons 
        SendResult = Button(text="Send result to patient",
                            width=25, height=5,
                            bg="purple", fg="white",
                            command=self.SendResult)

        valve2_open_one = Button(text="1-Valve one open",
                                 width=15, height=5,
                                 bg="red", fg="green",
                                 command=self.valve2_open_one)

        valve2_open_two = Button(text="1-Valve two open",
                                 width=15, height=5,
                                 bg="red", fg="green",
                                 command=self.valve2_open_two)

        valve2_open_three = Button(text="1-Valve three open",
                                   width=15, height=5,
                                   bg="red", fg="green",
                                   command=self.valve2_open_three)

        valve3_open_one = Button(text="2-Valve one open",
                                 width=15, height=5,
                                 bg="yellow", fg="red",
                                 command=self.valve3_open_one)

        valve3_open_two = Button(text="2-Valve two open",
                                 width=15, height=5,
                                 bg="yellow", fg="red",
                                 command=self.valve3_open_two)

        valve3_open_three = Button(text="2-Valve three open",
                                   width=15, height=5,
                                   bg="yellow", fg="red",
                                   command=self.valve3_open_three)

        pump_one_suck = Button(text="Pump one suck",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_one_suck)

        pump_one_blow = Button(text="Pump one blow",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_one_blow)

        pump_one_stop = Button(text="Pump one stop",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_one_stop)

        pump_two_suck = Button(text="Pump two suck",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_two_suck)

        pump_two_blow = Button(text="Pump two blow",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_two_blow)

        pump_two_stop = Button(text="Pump two stop",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_two_stop)

        # Placement of buttons 
        SendResult.place(x=3, y=3)
        valve2_open_one.place(x=3, y=100)
        valve2_open_two.place(x=3, y=200)
        valve2_open_three.place(x=3, y=300)
        valve3_open_one.place(x=150, y=100)
        valve3_open_two.place(x=150, y=200)
        valve3_open_three.place(x=150, y=300)

        pump_one_suck.place(x=300, y=3)
        pump_one_blow.place(x=300, y=100)
        pump_two_suck.place(x=300, y=200)
        pump_two_blow.place(x=300, y=300)

        pump_one_stop.place(x=450, y=3)

        pump_two_stop.place(x=450, y=200)

    # Button event functions 
    def SendResult(self):
        readQRCodeAndSendResult(1)  # 1 == "-ve", 0 == "+ve"

    def valve2_open_one(self):
        self.valve2.open_one()

    def valve2_open_two(self):
        self.valve2.open_two()

    def valve2_open_three(self):
        self.valve2.open_three()

    def valve3_open_one(self):
        self.valve3.open_one()

    def valve3_open_two(self):
        self.valve3.open_two()

    def valve3_open_three(self):
        self.valve3.open_three()

    def pump_one_suck(self):
        self.pump_1.Start(False, self.pump1_speed)

    def pump_one_blow(self):
        self.pump_1.Start(True, self.pump1_speed)

    def pump_two_suck(self):
        self.pump_2.Start(False, self.pump2_speed)

    def pump_two_blow(self):
        self.pump_2.Start(True, self.pump2_speed)

    def pump_one_stop(self):
        self.pump_1.Stop()

    def pump_two_stop(self):
        self.pump_2.Stop()


# Main Window 
root = Tk()

root.geometry("800x600")

# Creation of a window instance 
appWindow = Window(root)

# Main loop 
root.mainloop()
