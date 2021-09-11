# Authors: Yifan Liu, Jayendra Ellamathy 
# 
# Date: 23-07-2021

from tkinter import * 
from readQRandSendResult import readQRCodeAndSendResult
from StateMachine import StateMachine
import os 
import cv2 
import numpy as np
import PIL.Image, PIL.ImageTk


# Main window 
class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        self.sm = StateMachine("Test")
        
        self.cap = None 
        self.ResultFrame = None 
        self.canvas = None 
        self.width = None
        self.height = None
        self.photo = None

        self.init_window()


    #Creation of init_window
    def init_window(self):
        
        # Note: height, width, placements measured in text units 
        MainFont = "MS Sans Serif"

        TitleFontSize = 22
        Title2FontSize = 16
        ButtonFontSize = 11
        TextFontSize = 10 

        MainColor = "purple"
        SecondaryColor = "Blue Violet"
        TextColor = "white"


        self.master.title("InfluSense 1.0 - H1N1 Biosensor - Developed by UppSense from Uppsala University, Sweden")
        self.master.config(bg = MainColor)
        
        # Main Title 
        TitleFrame = Frame()

        MainTitle = Label(text = "InfluSense 1.0 - H1N1 Biosensor", 
                fg = TextColor, bg = MainColor, 
                master=TitleFrame, 
                font = (MainFont, TitleFontSize, "bold"))
        MainTitle.pack(ipady=3)


        # Middle Frame: Contains instructions and buttons in the left and the result window on the right 
        MiddleFrame = Frame()
        MiddleFrame.config(bg=MainColor)

        MiddleLeftFrame = Frame(MiddleFrame)
        MiddleLeftFrame.config(bg=MainColor)

        MiddleRightFrame = Frame(MiddleFrame)
        MiddleRightFrame.config(bg=MainColor)


        # Instructions 
        InstructionsFrame = Frame(MiddleLeftFrame)
        InstructionsFrame.configure(bg = MainColor)

        InstructionsTitle = Label(text = "Instructions", 
                fg = TextColor, bg = MainColor, 
                master = InstructionsFrame, 
                font = (MainFont, Title2FontSize, "bold"))
        InstructionsTitle.pack(fill=X, ipady=3) # Fill along X axis: 
                                       # Cover all spaces along the X axis of the frame.
                                                
        Instructions = Label(text = """1. Insert patient saliva sample.\n2. Click the start measuremnt button.\n3. The status window shows the current progress\nand indicates completion once finished.\n4. Click the send result button to start scanning the QR code.\n5. Once the QR code is scanned, wait for the result to be sent.\n6. Restart from step 2 for next measurement""", 
                                       master = InstructionsFrame,
                                       fg = TextColor, bg = MainColor, 
                                       font = (MainFont, TextFontSize), 
                                       justify=LEFT) # Text Alignment 
        Instructions.pack(fill=X, ipadx=10)  # Provide padding        


        # Buttons 
        ButtonsFrame = Frame(MiddleLeftFrame)
        ButtonsFrame.config(bg=MainColor)

        SendMeasurement = Button(text="Start Measurement", 
                height=2, 
                master = ButtonsFrame,
                bg=SecondaryColor, fg=TextColor, 
                font = (MainFont, ButtonFontSize, "bold"),
                command = self.SendMeasurement)
        SendMeasurement.pack(side=LEFT) 

        SendResult = Button(text="Send result to patient", 
                height=2, 
                master = ButtonsFrame,
                bg=SecondaryColor, fg=TextColor, 
                font = (MainFont, ButtonFontSize, "bold"),
                command = self.SendResult)
        SendResult.pack(side=LEFT) 
        
        
        # Results and camera window 
        self.ResultFrame = Frame(MiddleRightFrame)

        StatusTitle = Label(text = "Status Window", 
                master = MiddleRightFrame, 
                bg = MainColor, fg = TextColor, 
                font = (MainFont, TextFontSize, "bold"))
        StatusTitle.pack(fill=X)

        self.canvas = Canvas(self.ResultFrame, 
                width=300, height=300, 
                bg=MainColor)
        
        # Status text
        self.Status_window()

        # Potentiostat Plot 
        # TODO 

        # Camera 
        self.cap = cv2.VideoCapture(0) # Open Pi Camera  
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.Camera_window()


        # Arrangement of frames 
        TitleFrame.pack() 

        InstructionsFrame.pack(fill = BOTH, anchor=N) # Place this frame at the left side of the window 
        ButtonsFrame.pack(anchor = S, ipady = 10)
        MiddleLeftFrame.pack(side = LEFT)
   
        self.canvas.pack()
        self.ResultFrame.pack()
        MiddleRightFrame.pack(side = RIGHT, ipadx = 10, ipady = 5)

        MiddleFrame.pack()

        # Allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
 

    # ~~~~~~~~~~~~~~~~~ Button event functions ~~~~~~~~~~~~~~~~~ #
    def SendResult(self):
        readQRCodeAndSendResult(1) # 1 == "-ve", 0 == "+ve"
        
    def SendMeasurement(self):
        self.sm.detect() 
        
    def Camera_window(self):
        # Capture frame 
        ret, frame = self.cap.read()
        
        # frame2 = cv2.resize(frame, (300, 300))
        # self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        # self.canvas.create_image(0, 0, image=self.photo, anchor=CENTER)
        # self.ResultFrame.after(20, self.Camera_window)
    
    def Status_window():
        

# Main Window 
root = Tk()

# Window configurations  
# root.geometry("800x480") # Change to screen size 

# Creation of a window instance 
appWindow = Window(root)

# Main loop 
root.mainloop()
