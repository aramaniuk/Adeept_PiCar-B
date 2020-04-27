#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Product     : Raspberry PiCar-B
# File name   : main.py
# Description : client  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/12/18

import base64
import tkinter as tk
from tkinter import ttk
from socket import *
from clientpkg.vars import color_bg, color_text, \
    color_btn, color_can

from clientpkg.mainform import MainForm

# import speech_recognition as sr
import cv2
import numpy as np
import zmq


def video_show():
    while True:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)


def voice_input():
    global a2t
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     #r.adjust_for_ambient_noise(source)
    #     r.record(source,duration=2)
    #     print("Say something!")
    #     audio = r.listen(source)
    # try:
    #     a2t=r.recognize_sphinx(audio,keyword_entries=[('forward',1.0),('backward',1.0),('left',1.0),('right',1.0),('stop',1.0),('find line',0.95),('follow',1),('lights on',1),('lights off',1)])
    #     print("Sphinx thinks you said " + a2t)
    # except sr.UnknownValueError:
    #     print("Sphinx could not understand audio")
    # except sr.RequestError as e:
    #     print("Sphinx error; {0}".format(e))
    # BtnVIN.config(fg=color_text,bg=color_btn)
    return a2t


# def voice_command_thread():
# while 1:
#     if SR_mode == 1:
#         l_VIN.config(text='Command?')
#         v_command=voice_input()
#         if SR_mode == 1:
#             l_VIN.config(text='%s'%v_command)
#             if 'forward' in v_command:
#                 tcpClicSock.send(('forward').encode())
#             elif 'backward' in v_command:
#                 tcpClicSock.send(('backward').encode())
#             elif 'left' in v_command:
#                 tcpClicSock.send(('Left').encode())
#             elif 'right' in v_command:
#                 tcpClicSock.send(('Right').encode())
#             elif 'stop' in v_command:
#                 tcpClicSock.send(('stop').encode())
#                 tcpClicSock.send(('Stop').encode())
#             elif 'find line' in v_command:
#                 tcpClicSock.send(('findline').encode())
#             elif 'follow' in v_command:
#                 tcpClicSock.send(('auto').encode())
#             elif 'lights on' in v_command:
#                 tcpClicSock.send(('lightsON').encode())
#             elif 'lights off' in v_command:
#                 tcpClicSock.send(('lightsOFF').encode())
#             else:
#                 pass
#         else:
#             pass
#     else:
#         time.sleep(0.2)

def voice_command(event):
    global SR_mode
    if SR_mode == 0:
        SR_mode = 1
        BtnVIN.config(fg='#0277BD', bg='#BBDEFB')
    else:
        BtnVIN.config(fg=color_text, bg=color_btn)
        SR_mode = 0


def loop():  # GUI
    global tcpClicSock, BtnIP, led_status, BtnVIN, l_VIN, TestMode  # The value of tcpClicSock changes in the function loop(),would also changes in global so the other functions could use it.
    while True:
        root = tk.Tk()  # Define a window named root
        root.title('Adeept')  # Main window title
        root.geometry('950x630')  # Main window size, middle of the English letter x.
        root.config(bg=color_bg)  # Set the background color of root window

        var_spd = tk.StringVar()  # Speed value saved in a StringVar
        var_spd.set(
            1)  # Set a default speed,but change it would not change the default speed value in the car,you need to click button'Set' to send the value to the car

        var_x_scan = tk.IntVar()  # Scan range value saved in a IntVar
        var_x_scan.set(2)  # Set a default scan value

        # logo =tk.PhotoImage(file = 'logo.png')         #Define the picture of logo,but only supports '.png' and '.gif'
        # l_logo=tk.Label(root,image = logo,bg=color_bg) #Set a label to show the logo picture
        # l_logo.place(x=30,y=13)                        #Place the Label in a right position

        # BtnC1 = tk.Button(root, width=15, text='Camera Middle',fg=color_text,bg=color_btn,relief='ridge')
        BtnC1 = ttk.Button(root, width=15, text='Camera Middle')
        BtnC1.place(x=785, y=10)
        E_C1 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_C1.place(x=785, y=45)  # Define a Entry and put it in position

        BtnC2 = ttk.Button(root, width=15, text='Ultrasonic Middle')
        BtnC2.place(x=785, y=100)
        E_C2 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_C2.place(x=785, y=135)  # Define a Entry and put it in position

        BtnM1 = ttk.Button(root, width=15, text='Motor A Speed')
        BtnM1.place(x=785, y=190)
        E_M1 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_M1.place(x=785, y=225)  # Define a Entry and put it in position

        BtnM2 = ttk.Button(root, width=15, text='Motor B Speed')
        BtnM2.place(x=785, y=280)
        E_M2 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_M2.place(x=785, y=315)  # Define a Entry and put it in position

        BtnT1 = ttk.Button(root, width=15, text='Look Up Max')
        BtnT1.place(x=785, y=370)
        E_T1 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_T1.place(x=785, y=405)  # Define a Entry and put it in position

        BtnT2 = ttk.Button(root, width=15, text='Look Down Max')
        BtnT2.place(x=785, y=460)
        E_T2 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
        E_T2.place(x=785, y=495)  # Define a Entry and put it in position

        BtnLED = ttk.Button(root, width=15, text='Lights ON')
        BtnLED.place(x=300, y=420)

        BtnOCV = ttk.Button(root, width=15, text='OpenCV', command=call_opencv)
        BtnOCV.place(x=30, y=420)

        BtnFL = ttk.Button(root, width=15, text='Find Line')
        BtnFL.place(x=165, y=420)

        BtnSR3 = ttk.Button(root, width=15, text='Sphinx SR', command=call_SR3)
        BtnSR3.place(x=300, y=495)

        E_C1.insert(0, 'Default:425')
        E_C2.insert(0, 'Default:425')
        E_M1.insert(0, 'Default:100')
        E_M2.insert(0, 'Default:100')
        E_T1.insert(0, 'Default:662')
        E_T2.insert(0, 'Default:295')

        can_scan = tk.Canvas(root, bg=color_can, height=250, width=320, highlightthickness=0)  # define a canvas
        can_scan.place(x=440, y=330)  # Place the canvas
        line = can_scan.create_line(0, 62, 320, 62, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(0, 124, 320, 124, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(0, 186, 320, 186, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(160, 0, 160, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(80, 0, 80, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(240, 0, 240, 250, fill='darkgray')  # Draw a line on canvas
        x_range = var_x_scan.get()
        can_tex_11 = can_scan.create_text((27, 178), text='%sm' % round((x_range / 4), 2),
                                          fill='#aeea00')  # Create a text on canvas
        can_tex_12 = can_scan.create_text((27, 116), text='%sm' % round((x_range / 2), 2),
                                          fill='#aeea00')  # Create a text on canvas
        can_tex_13 = can_scan.create_text((27, 54), text='%sm' % round((x_range * 0.75), 2),
                                          fill='#aeea00')  # Create a text on canvas

        def spd_set():  # Call this function for speed adjustment
            tcpClicSock.send(
                ('spdset:%s' % var_spd.get()).encode())  # Get a speed value from IntVar and send it to the car
            l_ip_2.config(text='Speed:%s' % var_spd.get())  # Put the speed value on the speed status label

        def EC1_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('EC1set:%s' % E_C1.get()).encode())  # Get a speed value from IntVar and send it to the car

        def EC2_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('EC2set:%s' % E_C2.get()).encode())  # Get a speed value from IntVar and send it to the car

        def EM1_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('EM1set:%s' % E_M1.get()).encode())  # Get a speed value from IntVar and send it to the car

        def EM2_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('EM2set:%s' % E_M2.get()).encode())  # Get a speed value from IntVar and send it to the car

        def ET1_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('LUMset:%s' % E_T1.get()).encode())  # Get a speed value from IntVar and send it to the car

        def ET2_set(event):  # Call this function for speed adjustment
            tcpClicSock.send(
                ('LDMset:%s' % E_T2.get()).encode())  # Get a speed value from IntVar and send it to the car

        def connect(event):  # Call this function to connect with the server
            print("connect")
            # TODO: replace with call to CarConnect
            # if ip_stu == 1:
            #     sc=thread.Thread(target=socket_connect) #Define a thread for connection
            #     sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
            #     sc.start()                              #Thread starts

        def connect_2():  # Call this function to connect with the server
            print("connect2")
            # TODO: replace with call to CarConnect
            # if ip_stu == 1:
            #     sc=thread.Thread(target=socket_connect) #Define a thread for connection
            #     sc.setDaemon(True)                      #'True' means it is a front thread,it would close when the mainloop() closes
            #     sc.start()                              #Thread starts

        s1 = tk.Scale(root, label="               < Slow   Speed Adjustment   Fast >",
                      from_=0.4, to=1, orient=tk.HORIZONTAL, length=400,
                      showvalue=0.1, tickinterval=0.1, resolution=0.2, variable=var_spd, fg=color_text, bg=color_bg,
                      highlightthickness=0)
        s1.place(x=200, y=100)  # Define a Scale and put it in position

        s3 = tk.Scale(root, label="< Near   Scan Range Adjustment(Meter(s))   Far >",
                      from_=1, to=5, orient=tk.HORIZONTAL, length=300,
                      showvalue=1, tickinterval=1, resolution=1, variable=var_x_scan, fg=color_text, bg=color_bg,
                      highlightthickness=0)
        s3.place(x=30, y=320)

        # Define buttons and put these in position
        Btn0 = ttk.Button(root, width=8, text='Forward')
        Btn1 = ttk.Button(root, width=8, text='Backward')
        Btn2 = ttk.Button(root, width=8, text='Left')
        Btn3 = ttk.Button(root, width=8, text='Right')
        Btn4 = ttk.Button(root, width=8, text='Stop')
        Btn5 = ttk.Button(root, width=8, text='Follow')

        Btn6 = ttk.Button(root, width=8, text='Left')
        Btn7 = ttk.Button(root, width=8, text='Right')
        Btn8 = ttk.Button(root, width=8, text='Down')
        Btn9 = ttk.Button(root, width=8, text='Up')
        Btn10 = ttk.Button(root, width=8, text='Home')
        Btn11 = ttk.Button(root, width=8, text='Exit')

        Btn12 = ttk.Button(root, width=8, text='Set', command=spd_set)
        Btn13 = ttk.Button(root, width=8, text='Scan')

        Btn0.place(x=100, y=195)
        Btn1.place(x=100, y=230)
        Btn2.place(x=30, y=230)
        Btn3.place(x=170, y=230)
        Btn4.place(x=170, y=275)
        Btn5.place(x=30, y=275)

        Btn6.place(x=565, y=230)
        Btn7.place(x=705, y=230)
        Btn8.place(x=635, y=265)
        Btn9.place(x=635, y=195)
        Btn10.place(x=635, y=230)
        Btn11.place(x=705, y=10)

        Btn12.place(x=535, y=107)
        Btn13.place(x=350, y=330)

        # Bind the buttons with the corresponding callback function
        Btn0.bind('<ButtonPress-1>', call_forward)
        Btn1.bind('<ButtonPress-1>', call_back)
        Btn2.bind('<ButtonPress-1>', click_call_Left)
        Btn3.bind('<ButtonPress-1>', click_call_Right)
        Btn4.bind('<ButtonPress-1>', call_Stop)
        Btn5.bind('<ButtonPress-1>', call_auto)
        Btn6.bind('<ButtonPress-1>', call_look_left)
        Btn7.bind('<ButtonPress-1>', call_look_right)

        Btn8.bind('<ButtonPress-1>', call_look_down)
        Btn9.bind('<ButtonPress-1>', call_look_up)
        Btn10.bind('<ButtonPress-1>', call_ahead)
        Btn11.bind('<ButtonPress-1>', call_exit)
        Btn13.bind('<ButtonPress-1>', scan)

        Btn0.bind('<ButtonRelease-1>', call_stop)
        Btn1.bind('<ButtonRelease-1>', call_stop)
        Btn2.bind('<ButtonRelease-1>', call_stop)
        Btn3.bind('<ButtonRelease-1>', call_stop)
        Btn4.bind('<ButtonRelease-1>', call_stop)

        BtnC1.bind('<ButtonPress-1>', EC1_set)
        BtnC2.bind('<ButtonPress-1>', EC2_set)
        BtnM1.bind('<ButtonPress-1>', EM1_set)
        BtnM2.bind('<ButtonPress-1>', EM2_set)
        BtnT1.bind('<ButtonPress-1>', ET1_set)
        BtnT2.bind('<ButtonPress-1>', ET2_set)
        BtnFL.bind('<ButtonPress-1>', find_line)
        BtnVIN.bind('<ButtonPress-1>', voice_command)

        BtnLED.bind('<ButtonPress-1>', lights_ON)
        # Bind the keys with the corresponding callback function
        root.bind('<KeyPress-w>', call_forward)
        root.bind('<KeyPress-a>', call_Left)
        root.bind('<KeyPress-d>', call_Right)
        root.bind('<KeyPress-s>', call_back)

        # When these keys is released,call the function call_stop()
        root.bind('<KeyRelease-w>', call_stop)
        root.bind('<KeyRelease-a>', call_stop_2)
        root.bind('<KeyRelease-d>', call_stop_2)
        root.bind('<KeyRelease-s>', call_stop)
        root.bind('<KeyRelease-f>', lights_ON)
        root.bind('<KeyRelease-e>', find_line)
        root.bind('<KeyRelease-q>', voice_command)

        # Press these keyss to call the corresponding function()
        root.bind('<KeyPress-c>', call_Stop)
        root.bind('<KeyPress-z>', call_auto)
        root.bind('<KeyPress-j>', call_look_left)
        root.bind('<KeyPress-l>', call_look_right)
        root.bind('<KeyPress-h>', call_ahead)
        root.bind('<KeyPress-k>', call_look_down)
        root.bind('<KeyPress-i>', call_look_up)
        root.bind('<KeyPress-x>', scan)
        root.bind('<Return>', connect)
        root.bind('<Shift_L>', call_stop)

        global mainloop_status
        if mainloop_status == 0:  # Ensure the mainloop runs only once
            root.mainloop()  # Run the mainloop()
            mainloop_status = 1  # Change the value to '1' so the mainloop() would not run again.


if __name__ == '__main__':
    opencv_socket = socket()
    opencv_socket.bind(('0.0.0.0', 8080))
    opencv_socket.listen(0)

    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    footage_socket.bind('tcp://*:5555')
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    try:
        # loop()                   # Load GUI
        root = tk.Tk()
        MainForm(root).pack(side="top", fill="both", expand=True)
        root.mainloop()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()
