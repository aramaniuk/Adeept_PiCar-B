#!/usr/bin/python

import tkinter as tk
from tkinter import ttk

from client.vars import SR_mode, ipcon, \
    ADDR, BUFSIZ, ip_stu, ipaddr, mainloop_status, TestMode, \
    color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color

from client.usscanwidget import USScanWidget
from client.joystickwidget import JoystickWidget
from client.carcontroller import CarController
from client.textconfig import num_import


# TODO initiate network connection
# TODO initiate network processing
# TODO calibration for camera and steering through joysticks
# TODO network disconnect when pressed button again
# TODO joystickwidget event translation to controler for car and for camera
# TODO ultrasound scan in realtime
# TODO load calibration settings from car once connected
# TODO load battery settings from car
# TODO see what other peripherial data from car can be read


class MainForm(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.car_controller = CarController()
        self.configure_gui()
        self.create_widgets()
        self.car_controller.socket_connect()

    def __del__(self):
        self.car_connect.socket_disconnect()

    def configure_gui(self):
        self.parent.title('Adeept')  # Main window title
        self.parent.geometry('780x630')  # Main window size, middle of the English letter x.
        self.parent.config(bg=color_bg)  # Set the background color of root window

    def create_widgets(self):
        self.var_spd = tk.StringVar()  # Speed value saved in a StringVar
        self.var_spd.set(
            1)  # Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car

        self.var_x_scan = tk.IntVar()  # Scan range value saved in a IntVar
        self.var_x_scan.set(2)  # Set a default scan value

        # self.BtnC1 = ttk.Button(self.parent, width=15, text='Camera Middle')
        # self.BtnC1.place(x=785,y=10)
        # self.E_C1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_C1.place(x=785,y=45)                             #Define a Entry and put it in position
        #
        # self.BtnC2 = ttk.Button(self.parent, width=15, text='Ultrasonic Middle')
        # self.BtnC2.place(x=785,y=100)
        # self.E_C2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_C2.place(x=785,y=135)                             #Define a Entry and put it in position
        #
        # self.BtnM1 = ttk.Button(self.parent, width=15, text='Motor A Speed')
        # self.BtnM1.place(x=785,y=190)
        # self.E_M1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_M1.place(x=785,y=225)                             #Define a Entry and put it in position
        #
        # self.BtnM2 = ttk.Button(self.parent, width=15, text='Motor B Speed')
        # self.BtnM2.place(x=785,y=280)
        # self.E_M2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_M2.place(x=785,y=315)                             #Define a Entry and put it in position
        #
        # self.BtnT1 = ttk.Button(self.parent, width=15, text='Look Up Max')
        # self.BtnT1.place(x=785,y=370)
        # self.E_T1 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_T1.place(x=785,y=405)                             #Define a Entry and put it in position
        #
        # self.BtnT2 = ttk.Button(self.parent, width=15, text='Look Down Max')
        # self.BtnT2.place(x=785,y=460)
        # self.E_T2 = tk.Entry(self.parent,show=None,width=16,bg="#37474F",fg='#eceff1',exportselection=0,justify='center')
        # self.E_T2.place(x=785,y=495)                             #Define a Entry and put it in position

        # self.BtnLED = ttk.Button(self.parent, width=15, text='Lights ON')
        # self.BtnLED.place(x=300,y=420)
        #
        # self.BtnOCV = ttk.Button(self.parent, width=15, text='OpenCV',command=self.call_opencv)
        # self.BtnOCV.place(x=30,y=420)
        #
        # self.BtnFL = ttk.Button(self.parent, width=15, text='Find Line')
        # self.BtnFL.place(x=165,y=420)

        # self.BtnSR3 = ttk.Button(self.parent, width=15, text='Sphinx SR',command=self.call_SR3)
        # self.BtnSR3.place(x=300,y=495)

        self.frm_connection = tk.LabelFrame(text="Connection")
        self.frm_connection.config(bg=color_bg)

        self.l_ip_4 = tk.Label(self.frm_connection, width=18, text='Disconnected', fg=color_text, bg='#F44336')
        self.E1 = tk.Entry(self.frm_connection, show=None, width=16, bg="#37474F", fg='#eceff1')
        self.E1.insert(0, num_import("ip.txt", "IP:"))
        self.Btn14 = ttk.Button(self.frm_connection, width=8, text='Connect', command=self.OnButtonConnect)

        self.frm_connection.pack(expand=1, anchor=tk.NW)
        self.l_ip_4.pack(side=tk.LEFT, padx=10, pady=5)
        self.E1.pack(side=tk.LEFT, padx=10, pady=5)
        self.Btn14.pack(side=tk.LEFT, padx=10, pady=5)

        self.l_inter = tk.Label(self.parent, width=45,
                                text='< Car Adjustment              Camera Adjustment>\nW:Move Forward                 Look Up:I\nS:Move Backward            Look Down:K\nA:Turn Left                          Turn Left:J\nD:Turn Right                      Turn Right:L\nZ:Auto Mode On          Look Forward:H\nC:Auto Mode Off      Ultrasdonic Scan:X',
                                fg='#212121', bg='#90a4ae')
        self.l_inter.place(x=240, y=180)  # Define a Label and put it in position

        # self.BtnVIN = ttk.Button(self.parent, width=15, text='Voice Input')
        # self.BtnVIN.place(x=30, y=495)
        #
        # self.l_VIN = tk.Label(self.parent, width=16, text='Voice commands', fg=color_text, bg=color_btn)
        # self.l_VIN.place(x=30, y=465)

        # self.E_C1.insert(0, 'Default:425')
        # self.E_C2.insert(0, 'Default:425')
        # self.E_M1.insert(0, 'Default:100')
        # self.E_M2.insert(0, 'Default:100')
        # self.E_T1.insert(0, 'Default:662')
        # self.E_T2.insert(0, 'Default:295')

        self.frm_control = tk.LabelFrame(text="Control")
        self.frm_control.config(bg=color_bg)

        self.ScanW = USScanWidget(self.frm_control, self.var_x_scan.get())
        # self.ScanW.place(x=440, y=80)

        self.JstkW = JoystickWidget(self.frm_control)
        # self.JstkW.place(x=20, y=80)
        self.JstkW.OnThrottleStop += self.OnJoystickEnd

        self.CameraW = JoystickWidget(self.frm_control)

        self.frm_control.pack(side=tk.LEFT)
        self.JstkW.pack(side=tk.LEFT, padx=10, pady=5)
        self.ScanW.pack(side=tk.LEFT, padx=10, pady=5)
        self.CameraW.pack(side=tk.LEFT, padx=10, pady=5)

        self.car_controller.OnConnectionStatus += self.OnConnectionStatusChange

    def call_opencv(self):  # Start OpenCV mode
        print("Start OpenCV mode")

    def call_SR3(self):
        print("Call SR3")

    def OnJoystickEnd(self):
        print("JoystickReleased")

    def OnConnectionStatusChange(self, status):
        print("ConnectionStatusChange: " + status)
        self.l_ip_4.config(text=status)

    def OnButtonConnect(self):
        print("Connect")
