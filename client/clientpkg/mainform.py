#!/usr/bin/python

import tkinter as tk
import threading as thread
from tkinter import ttk

from clientpkg.vars import color_bg,color_text,color_static_label,color_status_error,color_status_ok,color_status_active

from clientpkg.usscanwidget import USScanWidget
from clientpkg.joystickwidget import JoystickWidget
from clientpkg.carcontroller import CarController
from clientpkg.textconfig import num_import, replace_num


# TODO initiate network processing
    # TODO - create car status field on the form
    # TODO - receive car adjustment values and push to joysticks for calibration
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

    def __del__(self):
        self.car_connect.socket_disconnect()

    def configure_gui(self):
        self.parent.title('Adeept')  # Main window title
        self.parent.geometry('780x630')  # Main window size, middle of the English letter x.
        self.parent.config(bg=color_bg)  # Set the background color of root window

    def create_widgets(self):
        self.var_spd = tk.StringVar()  # Speed value saved in a StringVar
        self.var_spd.set(1)  # Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car

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

        self.l_connection_status = tk.Label(self.frm_connection, width=18, text='Disconnected', fg=color_text, bg=color_status_error)
        self.e_ip_address = tk.Entry(self.frm_connection, show=None, width=16, bg="#37474F", fg='#eceff1')
        self.e_ip_address.insert(0, num_import("ip.txt", "IP:"))
        self.btn_connect = ttk.Button(self.frm_connection, width=8, text='Connect', command=self.on_button_connect)

        self.frm_connection.pack(expand=1, anchor=tk.NW)
        self.l_connection_status.pack(side=tk.LEFT, padx=10, pady=5)
        self.e_ip_address.pack(side=tk.LEFT, padx=10, pady=5)
        self.btn_connect.pack(side=tk.LEFT, padx=10, pady=5)

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

        f_left = tk.Frame(self.frm_control)
        f_left.config(bg=color_bg)
        f_middle = tk.Frame(self.frm_control)
        f_middle.config(bg=color_bg)
        f_right = tk.Frame(self.frm_control)
        f_right.config(bg=color_bg)

        # left side control
        self.l_jstk = tk.Label(f_left, width=18, text='Navigation', fg=color_text, bg=color_static_label)
        self.JstkW = JoystickWidget(f_left)
        self.JstkW.OnThrottleStop += self.on_joystick_end

        self.JstkW.pack(side=tk.TOP, padx=10, pady=5)
        self.l_jstk.pack(side=tk.BOTTOM, padx=10, pady=5)

        # middle side control
        self.ScanW = USScanWidget(f_middle, self.var_x_scan.get())
        self.l_scan = tk.Label(f_middle, width=18, text='Ultrasonic sensor', fg=color_text, bg=color_static_label)

        self.ScanW.pack(side=tk.TOP, padx=10, pady=5)
        self.l_scan.pack(side=tk.BOTTOM, padx=10, pady=5)

        # right side control
        self.CameraW = JoystickWidget(f_right)
        self.l_camera = tk.Label(f_right, width=18, text='Camera', fg=color_text, bg=color_static_label)

        self.CameraW.pack(side=tk.TOP, padx=10, pady=5)
        self.l_camera.pack(side=tk.BOTTOM, padx=10, pady=5)

        self.frm_control.pack(side=tk.LEFT)

        f_left.pack(side=tk.LEFT)
        f_middle.pack(side=tk.LEFT)
        f_right.pack(side=tk.LEFT)

        # Event subscriptions
        self.car_controller.on_connection_status += self.on_connection_status_change
        self.car_controller.on_connection_error += self.on_connection_error
        self.car_controller.on_connection_success += self.on_connection_success
        self.car_controller.on_car_settings += self.on_car_settings
        self.car_controller.on_ultrasonic_data += self.ScanW.on_update_ultrasonic_data

    def call_opencv(self):  # Start OpenCV mode
        print("Start OpenCV mode")

    def call_SR3(self):
        print("Call SR3")

    ####### EVENT HANDLERS ########

    def on_button_connect(self):
        if self.car_controller.connection_status == 1:
            ip_adr = self.e_ip_address.get()  # Get the IP address from Entry

            if ip_adr == '':  # If no input IP address in Entry,import a default IP
                ip_adr = num_import("ip.txt", "IP:")
                self.e_ip_address.insert(0, ip_adr)
            self.btn_connect.config(state='disabled')  # Disable the Entry
            sc=thread.Thread(target=self.car_controller.socket_connect, args=(ip_adr,)) #Define a thread for connection
            sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
            sc.start()                              #Thread starts

        print("ButtonConnect")

    def on_joystick_end(self):
        print("JoystickReleased")

    def on_connection_status_change(self, status):
        print("ConnectionStatusChange: " + status)
        self.l_connection_status.config(text=status)
        self.l_connection_status.config(bg=color_status_active)


    def on_connection_success(self, status):
        print("OnConnectionSuccess: " + status)
        self.l_connection_status.config(text=status)
        self.l_connection_status.config(bg=color_status_ok)

        replace_num('IP.txt', 'IP:', self.e_ip_address.get())
        self.e_ip_address.config(state='disabled')  # Disable the Entry


    def on_connection_error(self, status):
        print("OnConnectionError: " + status)
        self.l_connection_status.config(text=status)
        self.l_connection_status.config(bg='#F44336')
        self.e_ip_address.config(state='normal')  # Disable the Entry
        self.btn_connect.config(state='normal')  # Disable the Entry

    def on_car_settings(self, settings):
        print("OnCarSettings: " + settings)
        set_list = settings.split()
        s1, s2, s3, s4, s5, s6 = set_list[1:]
        # camera center vertical           s1
        # camera center horisontal         s1
        # Motor A Speed Adjustment	       s3
        # Motor B Speed Adjustment	       s4
        # Motor A Turning Speed Adjustment s5
        # Motor B Turning Speed Adjustment s6

        # TODO: update controls with car settings
        # E_C1.delete(0, 50)
        # E_C2.delete(0, 50)
        # E_M1.delete(0, 50)
        # E_M2.delete(0, 50)
        # E_T1.delete(0, 50)
        # E_T2.delete(0, 50)
        #
        # E_C1.insert(0, '%d' % int(s1))
        # E_C2.insert(0, '%d' % int(s2))
        # E_M1.insert(0, '%d' % int(s3))
        # E_M2.insert(0, '%d' % int(s4))
        # E_T1.insert(0, '%d' % int(s5))
        # E_T2.insert(0, '%d' % int(s6))