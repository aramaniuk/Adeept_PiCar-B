#!/usr/bin/python

import tkinter as tk
from tkinter import ttk

from vars import SR_mode,led_status,ipcon,findline_status,auto_status,\
    ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr,mainloop_status,\
    opencv_status,speech_status,TestMode,\
    c_f_stu,c_b_stu,c_l_stu,c_r_stu,b_l_stu,b_r_stu,l_stu,r_stu,\
    color_bg,color_text,color_btn,color_line,color_can,color_oval,target_color

from usscanwidget import USScanWidget
from joystickwidget import JoystickWidget

class MainForm(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.parent.title('Adeept')          # Main window title
        self.parent.geometry('950x630')      # Main window size, middle of the English letter x.
        self.parent.config(bg=color_bg)      # Set the background color of root window

    def create_widgets(self):
        self.frame = tk.Frame(self.parent)
        self.frame.config(bg=color_bg)

        var_spd = tk.StringVar()        # Speed value saved in a StringVar
        var_spd.set(1)                  # Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car

        var_x_scan = tk.IntVar()        # Scan range value saved in a IntVar
        var_x_scan.set(2)               # Set a default scan value

        BtnC1 = ttk.Button(self.parent, width=15, text='Camera Middle')
        BtnC1.place(x=785,y=10)
        E_C1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_C1.place(x=785,y=45)                             #Define a Entry and put it in position

        BtnC2 = ttk.Button(self.parent, width=15, text='Ultrasonic Middle')
        BtnC2.place(x=785,y=100)
        E_C2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_C2.place(x=785,y=135)                             #Define a Entry and put it in position

        BtnM1 = ttk.Button(self.parent, width=15, text='Motor A Speed')
        BtnM1.place(x=785,y=190)
        E_M1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_M1.place(x=785,y=225)                             #Define a Entry and put it in position

        BtnM2 = ttk.Button(self.parent, width=15, text='Motor B Speed')
        BtnM2.place(x=785,y=280)
        E_M2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_M2.place(x=785,y=315)                             #Define a Entry and put it in position

        BtnT1 = ttk.Button(self.parent, width=15, text='Look Up Max')
        BtnT1.place(x=785,y=370)
        E_T1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_T1.place(x=785,y=405)                             #Define a Entry and put it in position

        BtnT2 = ttk.Button(self.parent, width=15, text='Look Down Max')
        BtnT2.place(x=785,y=460)
        E_T2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        E_T2.place(x=785,y=495)                             #Define a Entry and put it in position

        BtnLED = ttk.Button(self.parent, width=15, text='Lights ON')
        BtnLED.place(x=300,y=420)

        BtnOCV = ttk.Button(self.parent, width=15, text='OpenCV',command=self.call_opencv)
        BtnOCV.place(x=30,y=420)

        BtnFL = ttk.Button(self.parent, width=15, text='Find Line')
        BtnFL.place(x=165,y=420)

        BtnSR3 = ttk.Button(self.parent, width=15, text='Sphinx SR',command=self.call_SR3)
        BtnSR3.place(x=300,y=495)

        E_C1.insert(0, 'Default:425')
        E_C2.insert(0, 'Default:425')
        E_M1.insert(0, 'Default:100')
        E_M2.insert(0, 'Default:100')
        E_T1.insert(0, 'Default:662')
        E_T2.insert(0, 'Default:295')

        ScanW = USScanWidget(self, var_x_scan.get())
        ScanW.place(x=440, y=330)

        JstkW = JoystickWidget(self)
        JstkW.place(x=20, y=20)

    def call_opencv(self):  # Start OpenCV mode
        print("Start OpenCV mode")

    def call_SR3(self):
        print("Call SR3")