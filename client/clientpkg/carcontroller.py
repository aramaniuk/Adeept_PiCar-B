#!/usr/bin/python
import time
from socket import socket, AF_INET, SOCK_STREAM
import enum
from clientpkg.eventhook import EventHook


# Using enum class create enumerations
class EventTypes(enum.Enum):
    ConnectionStatus = 1
    ConnectionError = 2
    ConnectionSuccess = 3


class CarControllerEvent(object):
    def __init__(self, type):
        self.type = type

    @classmethod
    def ConnectionStatus(cls, status):
        cls.status = status
        return cls(EventTypes.ConnectionStatus)

    @classmethod
    def ConnectionError(cls, status):
        cls.status = status
        return cls(EventTypes.ConnectionError)

    @classmethod
    def ConnectionSuccess(cls, status):
        cls.status = status
        return cls(EventTypes.ConnectionSuccess)


class CarController(object):
    def __init__(self):
        # input status
        self.c_f_stu = 0
        self.c_b_stu = 0
        self.c_l_stu = 0
        self.c_r_stu = 0

        self.b_l_stu = 0
        self.b_r_stu = 0

        self.l_stu = 0
        self.r_stu = 0
        self.ip_stu = 1         # Shows connection status
        self.BUFSIZ = 1024      # Define buffer size for reading from socket

        self.led_status = 0
        self.opencv_status = 0
        self.auto_status = 0
        self.speech_status = 0
        self.findline_status = 0
        self.tcpClientSock = ''

        self.OnConnectionStatus = EventHook()
        self.OnConnectionSuccess = EventHook()
        self.OnConnectionError = EventHook()

    @property
    def connection_status(self):
        return self.ip_stu

    def fireEvents(self, event):
        if event.type == EventTypes.ConnectionStatus:
            self.OnConnectionStatus.fire(event.status)
        elif event.type == EventTypes.ConnectionSuccess:
            self.OnConnectionSuccess.fire(event.status)
        elif event.type == EventTypes.ConnectionError:
            self.OnConnectionError.fire(event.status)


    def call_forward(self):         #When this function is called,client commands the car to move forward
        if self.c_f_stu == 0:
            self.tcpClientSock.send(('forward').encode())
            self.c_f_stu=1

    def call_back(self):            #When this function is called,client commands the car to move backward
        if self.c_b_stu == 0:
            self.tcpClientSock.send(('backward').encode())
            self.c_b_stu=1

    def call_stop(self):            #When this function is called,client commands the car to stop moving
        self.c_f_stu=0
        self.c_b_stu=0
        self.tcpClientSock.send(('stop').encode())

    def call_stop_2(self):            #When this function is called,client commands the car go straight
        self.c_r_stu=0
        self.c_l_stu=0
        self.tcpClientSock.send(('middle').encode())

    def click_call_Left(self):            #When this function is called,client commands the car to turn left
        self.tcpClientSock.send(('Left').encode())

    def click_call_Right(self):           #When this function is called,client commands the car to turn right
        self.tcpClientSock.send(('Right').encode())

    def call_Left(self):            #When this function is called,client commands the car to turn left
        if self.c_l_stu == 0 :
            self.tcpClientSock.send(('Left').encode())
            self.c_l_stu=1

    def call_Right(self):           #When this function is called,client commands the car to turn right
        if self.c_r_stu == 0 :
            self.tcpClientSock.send(('Right').encode())
            self.c_r_stu=1

    def call_look_left(self):               #Camera look left
        self.tcpClientSock.send(('l_le').encode())

    def call_look_right(self):              #Camera look right
        self.tcpClientSock.send(('l_ri').encode())

    def call_look_up(self):                 #Camera look up
        self.tcpClientSock.send(('l_up').encode())

    def call_look_down(self):               #Camera look down
        self.tcpClientSock.send(('l_do').encode())

    def call_ahead(self):                   #Camera look ahead
        self.tcpClientSock.send(('ahead').encode())
        print('ahead')

    def call_auto(self):            #When this function is called,client commands the car to start auto mode
        if self.auto_status == 0:
            self.tcpClientSock.send(('auto').encode())
        else:
            self.tcpClientSock.send(('Stop').encode())

    def call_exit(self):            #When this function is called,client commands the car to shut down
        self.tcpClientSock.send(('exit').encode())

    def call_Stop(self):            #When this function is called,client commands the car to switch off auto mode
        self.tcpClientSock.send(('Stop').encode())

    def scan(self):                 #When this function is called,client commands the ultrasonic to scan
        self.tcpClientSock.send(('scan').encode())
        print('scan')

    def find_line(self):            #Line follow mode
        if self.findline_status == 0:
            self.tcpClientSock.send(('findline').encode())
        else:
            self.tcpClientSock.send(('Stop').encode())

    def lights_ON(self):  # Turn on the LEDs
        if self.led_status == 0:
            self.tcpClientSock.send(('lightsON').encode())
        else:
            self.tcpClientSock.send(('lightsOFF').encode())

    def call_SR3(self):  # Start speech recognition mode
        if self.speech_status == 0:
            self.tcpClientSock.send(('voice_3').encode())
        else:
            self.tcpClientSock.send(('Stop').encode())

    def call_opencv(self):  # Start OpenCV mode
        if self.opencv_status == 0:
            self.tcpClientSock.send(('opencv').encode())
        else:
            self.tcpClientSock.send(('Stop').encode())

    def socket_disconnect(self):
        print("socket disconnect")
        if self.tcpClientSock != '':
            self.tcpClientSock.close()  # Close socket or it may not connect with the server again


    def socket_connect(self, ip_adr):  # Call this function to connect with the server
        #ip_adr = '192.168.10.6'
        print("socket_connect thread connecting to " + ip_adr )
        self.fireEvents(CarControllerEvent.ConnectionStatus('Connecting...'))

        server_ip = ip_adr
        server_port = 10223  # Define port serial
        addr = (server_ip, server_port)
        self.tcpClientSock = socket(AF_INET, SOCK_STREAM)  # Set connection value for socket

        for i in range(1, 6):  # Try 5 times if disconnected
            try:
                if ip_stu == 1:
                    print("Connecting to server @ %s:%d..." % (server_ip, server_port))
                    print("Connecting")
                    self.tcpClientSock.connect(addr)  # Connection with the server

                    print("Connected")

                    self.fireEvents(CarControllerEvent.ConnectionSuccess('Connected'))

                    self.ip_stu = 0  # '0' means connected

                    # at = thread.Thread(target=code_receive)  # Define a thread for data receiving
                    # at.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
                    # at.start()  # Thread starts

                    # SR_threading = thread.Thread(target=voice_command_thread)  # Define a thread for ultrasonic tracking
                    # SR_threading.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
                    # SR_threading.start()  # Thread starts

                    # video_thread = thread.Thread(target=video_show)  # Define a thread for data receiving
                    # video_thread.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
                    # print('Video Connected')
                    # video_thread.start()                            #Thread starts

                    # ipaddr = self.tcpClientSock.getsockname()[0]
                    break
                else:
                    break
            except Exception:
                print("Cannot connect to server")
                self.fireEvents(CarControllerEvent.ConnectionStatus('Trying %d/5 time(s)' % i))
                print('Trying %d/5 time(s)' % i)
                ip_stu = 1
                self.tcpClientSock.close()
                time.sleep(1)
                continue
        if ip_stu == 1:
            self.fireEvents(CarControllerEvent.ConnectionError('Disconnected'))

    def code_receive(self):  # A function for data receiving
        print("code receive thread")
        # global led_status, ipcon, findline_status, auto_status, opencv_status, speech_status, TestMode
        # while True:
        #     code_car = tcpClicSock.recv(BUFSIZ)  # Listening,and save the data in 'code_car'
        #     l_ip.config(text=code_car)  # Put the data on the label
        #     # print(code_car)
        #     if not code_car:
        #         continue
        #     elif 'SET' in str(code_car):
        #         print('set get')
        #         set_list = code_car.decode()
        #         set_list = set_list.split()
        #         s1, s2, s3, s4, s5, s6 = set_list[1:]
        #         E_C1.delete(0, 50)
        #         E_C2.delete(0, 50)
        #         E_M1.delete(0, 50)
        #         E_M2.delete(0, 50)
        #         E_T1.delete(0, 50)
        #         E_T2.delete(0, 50)
        #
        #         E_C1.insert(0, '%d' % int(s1))
        #         E_C2.insert(0, '%d' % int(s2))
        #         E_M1.insert(0, '%d' % int(s3))
        #         E_M2.insert(0, '%d' % int(s4))
        #         E_T1.insert(0, '%d' % int(s5))
        #         E_T2.insert(0, '%d' % int(s6))
        #
        #     elif 'list' in str(code_car):  # Scan result receiving start
        #         dis_list = []
        #         f_list = []
        #         list_str = code_car.decode()
        #
        #         while True:  # Save scan result in dis_list
        #             code_car = tcpClicSock.recv(BUFSIZ)
        #             if 'finished' in str(code_car):
        #                 break
        #             list_str += code_car.decode()
        #             l_ip.config(text='Scanning')
        #
        #         dis_list = list_str.split()  # Save the data as a list
        #         l_ip.config(text='Finished')
        #
        #         for i in range(0, len(dis_list)):  # Translate the String-type value in the list to Float-type
        #             try:
        #                 new_f = float(dis_list[i])
        #                 f_list.append(new_f)
        #             except:
        #                 continue
        #
        #         dis_list = f_list
        #         # can_scan.delete(line)
        #         # can_scan.delete(point_scan)
        #         can_scan_1 = tk.Canvas(root, bg=color_can, height=250, width=320,
        #                                highlightthickness=0)  # define a canvas
        #         can_scan_1.place(x=440, y=330)  # Place the canvas
        #         line = can_scan_1.create_line(0, 62, 320, 62, fill='darkgray')  # Draw a line on canvas
        #         line = can_scan_1.create_line(0, 124, 320, 124, fill='darkgray')  # Draw a line on canvas
        #         line = can_scan_1.create_line(0, 186, 320, 186, fill='darkgray')  # Draw a line on canvas
        #         line = can_scan_1.create_line(160, 0, 160, 250, fill='darkgray')  # Draw a line on canvas
        #         line = can_scan_1.create_line(80, 0, 80, 250, fill='darkgray')  # Draw a line on canvas
        #         line = can_scan_1.create_line(240, 0, 240, 250, fill='darkgray')  # Draw a line on canvas
        #
        #         x_range = var_x_scan.get()  # Get the value of scan range from IntVar
        #
        #         for i in range(0, len(dis_list)):  # Scale the result to the size as canvas
        #             try:
        #                 len_dis_1 = int((dis_list[i] / x_range) * 250)  # 600 is the height of canvas
        #                 pos = int((i / len(dis_list)) * 320)  # 740 is the width of canvas
        #                 pos_ra = int(((i / len(dis_list)) * 140) + 20)  # Scale the direction range to (20-160)
        #                 len_dis = int(
        #                     len_dis_1 * (math.sin(math.radians(pos_ra))))  # len_dis is the height of the line
        #
        #                 x0_l, y0_l, x1_l, y1_l = pos, (250 - len_dis), pos, (250 - len_dis)  # The position of line
        #                 x0, y0, x1, y1 = (pos + 3), (250 - len_dis + 3), (pos - 3), (
        #                             250 - len_dis - 3)  # The position of arc
        #
        #                 if pos <= 160:  # Scale the whole picture to a shape of sector
        #                     pos = 160 - abs(int(len_dis_1 * (math.cos(math.radians(pos_ra)))))
        #                     x1_l = (x1_l - math.cos(math.radians(pos_ra)) * 130)
        #                 else:
        #                     pos = abs(int(len_dis_1 * (math.cos(math.radians(pos_ra))))) + 160
        #                     x1_l = x1_l + abs(math.cos(math.radians(pos_ra)) * 130)
        #
        #                 y1_l = y1_l - abs(math.sin(math.radians(pos_ra)) * 130)  # Orientation of line
        #
        #                 line = can_scan_1.create_line(pos, y0_l, x1_l, y1_l,
        #                                               fill=color_line)  # Draw a line on canvas
        #                 point_scan = can_scan_1.create_oval((pos + 3), y0, (pos - 3), y1, fill=color_oval,
        #                                                     outline=color_oval)  # Draw a arc on canvas
        #             except:
        #                 pass
        #         can_tex_11 = can_scan_1.create_text((27, 178), text='%sm' % round((x_range / 4), 2),
        #                                             fill='#aeea00')  # Create a text on canvas
        #         can_tex_12 = can_scan_1.create_text((27, 116), text='%sm' % round((x_range / 2), 2),
        #                                             fill='#aeea00')  # Create a text on canvas
        #         can_tex_13 = can_scan_1.create_text((27, 54), text='%sm' % round((x_range * 0.75), 2),
        #                                             fill='#aeea00')  # Create a text on canvas
        #
        #     elif '1' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Moving Forward')  # Put the text on the label
        #     elif '2' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Moving Backward')  # Put the text on the label
        #     elif '3' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Turning Left')  # Put the text on the label
        #     elif '4' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Turning Right')  # Put the text on the label
        #     elif '5' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Look Up')  # Put the text on the label
        #     elif '6' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Look Down')  # Put the text on the label
        #     elif '7' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Look Left')  # Put the text on the label
        #     elif '8' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Look Right')  # Put the text on the label
        #     elif '9' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Stop')  # Put the text on the label
        #
        #     elif '0' in str(code_car):  # Translate the code to text
        #         l_ip.config(text='Follow Mode On')  # Put the text on the label
        #         Btn5.config(text='Following', fg='#0277BD', bg='#BBDEFB')
        #         auto_status = 1
        #
        #     elif 'findline' in str(code_car):  # Translate the code to text
        #         BtnFL.config(text='Finding', fg='#0277BD', bg='#BBDEFB')
        #         l_ip.config(text='Find Line')
        #         findline_status = 1
        #
        #     elif 'lightsON' in str(code_car):  # Translate the code to text
        #         BtnLED.config(text='Lights ON', fg='#0277BD', bg='#BBDEFB')
        #         led_status = 1
        #         l_ip.config(text='Lights On')  # Put the text on the label
        #
        #     elif 'lightsOFF' in str(code_car):  # Translate the code to text
        #         BtnLED.config(text='Lights OFF', fg=color_text, bg=color_btn)
        #         led_status = 0
        #         l_ip.config(text='Lights OFF')  # Put the text on the label
        #
        #     elif 'oncvon' in str(code_car):
        #         if TestMode == 0:
        #             BtnOCV.config(text='OpenCV ON', fg='#0277BD', bg='#BBDEFB')
        #             BtnFL.config(text='Find Line', fg=color_text, bg=color_btn)
        #             l_ip.config(text='OpenCV ON')
        #             opencv_status = 1
        #
        #     elif 'auto_status_off' in str(code_car):
        #         if TestMode == 0:
        #             BtnSR3.config(fg=color_text, bg=color_btn, state='normal')
        #             BtnOCV.config(text='OpenCV', fg=color_text, bg=color_btn, state='normal')
        #         BtnFL.config(text='Find Line', fg=color_text, bg=color_btn)
        #         Btn5.config(text='Follow', fg=color_text, bg=color_btn, state='normal')
        #         findline_status = 0
        #         speech_status = 0
        #         opencv_status = 0
        #         auto_status = 0
        #
        #     elif 'voice_3' in str(code_car):
        #         BtnSR3.config(fg='#0277BD', bg='#BBDEFB')
        #         # BtnSR1.config(state='disabled')
        #         # BtnSR2.config(state='disabled')
        #         l_ip.config(text='Sphinx SR')  # Put the text on the label
        #         speech_status = 1
        #
        #     elif 'TestVersion' in str(code_car):
        #         TestMode = 1
        #         BtnSR3.config(fg='#FFFFFF', bg='#F44336')
        #         BtnOCV.config(fg='#FFFFFF', bg='#F44336')