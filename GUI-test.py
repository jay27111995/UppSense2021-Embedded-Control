import threading
from tkinter import *

from StateMachine import StateMachine


class BackgroundTask:

    def __init__(self, taskFuncPointer):
        self.__taskFuncPointer_ = taskFuncPointer
        self.__workerThread_ = None
        self.__isRunning_ = False

    def taskFuncPointer(self):
        return self.__taskFuncPointer_

    def isRunning(self):
        return self.__isRunning_ and self.__workerThread_.isAlive()

    def start(self):
        if not self.__isRunning_:
            self.__isRunning_ = True
            self.__workerThread_ = self.WorkerThread(self)
            self.__workerThread_.start()

    def stop(self):
        self.__isRunning_ = False

    class WorkerThread(threading.Thread):
        def __init__(self, bgTask):
            threading.Thread.__init__(self)
            self.__bgTask_ = bgTask

        def run(self):
            try:
                self.__bgTask_.taskFuncPointer()(self.__bgTask_.isRunning)
            except Exception as e:
                print(e)
            self.__bgTask_.stop()


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.sm = StateMachine("Test")

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("UppSense H1N1 Biosensor - Developed in Uppsala University, Sweden")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Buttons
        pump_two_stop = Button(text="Pump two stop",
                               width=10, height=5,
                               bg="purple", fg="white",
                               command=self.pump_two_stop)

        # Placement of buttons
        pump_two_stop.place(x=450, y=200)

    # Button event functions
    def pump_two_stop(self):
        self.sm.detect()


# Main Window 
root = Tk()

root.geometry("800x600")

# Creation of a window instance 
appWindow = Window(root, )

# Main loop 
root.mainloop()
