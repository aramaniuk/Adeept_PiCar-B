#!/usr/bin/python
import time
import threading as thread
from socket import socket, AF_INET, SOCK_STREAM
import enum
from clientpkg.eventhook import EventHook


# Using enum class create enumerations
class EventTypes(enum.Enum):
    ConnectionStatus = 1
    ConnectionError = 2
    ConnectionSuccess = 3
    CarSettings = 4
    UltraSonicData = 5


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

    @classmethod
    def CarSettings(cls, settings):
        cls.settings = settings
        return cls(EventTypes.CarSettings)

    @classmethod
    def UltraSonicData(cls, ultraSonicData):
        cls.ultraSonicData = ultraSonicData
        return cls(EventTypes.UltraSonicData)


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

        self.on_connection_status = EventHook()
        self.on_connection_success = EventHook()
        self.on_connection_error = EventHook()
        self.on_car_settings = EventHook()
        self.on_ultrasonic_data = EventHook()

    @property
    def connection_status(self):
        return self.ip_stu

    def fire_events(self, event):
        if event.type == EventTypes.ConnectionStatus:
            self.on_connection_status.fire(event.status)
        elif event.type == EventTypes.ConnectionSuccess:
            self.on_connection_success.fire(event.status)
        elif event.type == EventTypes.ConnectionError:
            self.on_connection_error.fire(event.status)
        elif event.type == EventTypes.CarSettings:
            self.on_connection_error.fire(event.settings)
        elif event.type == EventTypes.UltraSonicData:
            self.on_connection_error.fire(event.ultraSonicData)


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
        print("socket_connect thread connecting to " + ip_adr )
        self.fire_events(CarControllerEvent.ConnectionStatus('Connecting...'))

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

                    self.fire_events(CarControllerEvent.ConnectionSuccess('Connected'))

                    self.ip_stu = 0  # '0' means connected

                    at = thread.Thread(target=self.code_receive)  # Define a thread for data receiving
                    at.setDaemon(True)  # 'True' means it is a front thread,it would close when the mainloop() closes
                    at.start()  # Thread starts

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
                self.fire_events(CarControllerEvent.ConnectionStatus('Trying %d/5 time(s)' % i))
                print('Trying %d/5 time(s)' % i)
                ip_stu = 1
                self.tcpClientSock.close()
                time.sleep(1)
                continue
        if ip_stu == 1:
            self.fire_events(CarControllerEvent.ConnectionError('Disconnected'))

    def code_receive(self):  # A function for data receiving
        print("code receive thread started")
        # global led_status, ipcon, findline_status, auto_status, opencv_status, speech_status, TestMode
        while True:
            code_car = self.tcpClicSock.recv(self.BUFSIZ)  # Listening,and save the data in 'code_car'
            #l_ip.config(text=code_car)  # Put the data on the label
            print("received from car: " + code_car)
            if not code_car:
                continue
            elif 'SET' in str(code_car):    # settings received from car
                print('car settings')
                set_list = code_car.decode()
                self.fire_events(CarControllerEvent.CarSettings(set_list))
            elif 'list' in str(code_car):  # Scan result receiving start
                list_str = code_car.decode()
                while True:  # Save scan result in dis_list
                    code_car = self.tcpClicSock.recv(self.BUFSIZ)
                    if 'finished' in str(code_car):
                        break
                    list_str += code_car.decode()

                self.fire_events(CarControllerEvent.UltraSonicData(list_str))
            elif '1' in str(code_car):  # Translate the code to text
                # TODO: replace with event
                l_ip.config(text='Moving Forward')  # Put the text on the label
            elif '2' in str(code_car):  # Translate the code to text
                l_ip.config(text='Moving Backward')  # Put the text on the label
            elif '3' in str(code_car):  # Translate the code to text
                l_ip.config(text='Turning Left')  # Put the text on the label
            elif '4' in str(code_car):  # Translate the code to text
                l_ip.config(text='Turning Right')  # Put the text on the label
            elif '5' in str(code_car):  # Translate the code to text
                l_ip.config(text='Look Up')  # Put the text on the label
            elif '6' in str(code_car):  # Translate the code to text
                l_ip.config(text='Look Down')  # Put the text on the label
            elif '7' in str(code_car):  # Translate the code to text
                l_ip.config(text='Look Left')  # Put the text on the label
            elif '8' in str(code_car):  # Translate the code to text
                l_ip.config(text='Look Right')  # Put the text on the label
            elif '9' in str(code_car):  # Translate the code to text
                l_ip.config(text='Stop')  # Put the text on the label

            elif '0' in str(code_car):  # Translate the code to text
                l_ip.config(text='Follow Mode On')  # Put the text on the label
                Btn5.config(text='Following', fg='#0277BD', bg='#BBDEFB')
                auto_status = 1

            elif 'findline' in str(code_car):  # Translate the code to text
                BtnFL.config(text='Finding', fg='#0277BD', bg='#BBDEFB')
                l_ip.config(text='Find Line')
                findline_status = 1

            elif 'lightsON' in str(code_car):  # Translate the code to text
                BtnLED.config(text='Lights ON', fg='#0277BD', bg='#BBDEFB')
                led_status = 1
                l_ip.config(text='Lights On')  # Put the text on the label

            elif 'lightsOFF' in str(code_car):  # Translate the code to text
                BtnLED.config(text='Lights OFF', fg=color_text, bg=color_btn)
                led_status = 0
                l_ip.config(text='Lights OFF')  # Put the text on the label

            elif 'oncvon' in str(code_car):
                if TestMode == 0:
                    BtnOCV.config(text='OpenCV ON', fg='#0277BD', bg='#BBDEFB')
                    BtnFL.config(text='Find Line', fg=color_text, bg=color_btn)
                    l_ip.config(text='OpenCV ON')
                    opencv_status = 1

            elif 'auto_status_off' in str(code_car):
                if TestMode == 0:
                    BtnSR3.config(fg=color_text, bg=color_btn, state='normal')
                    BtnOCV.config(text='OpenCV', fg=color_text, bg=color_btn, state='normal')
                BtnFL.config(text='Find Line', fg=color_text, bg=color_btn)
                Btn5.config(text='Follow', fg=color_text, bg=color_btn, state='normal')
                findline_status = 0
                speech_status = 0
                opencv_status = 0
                auto_status = 0

            elif 'voice_3' in str(code_car):
                BtnSR3.config(fg='#0277BD', bg='#BBDEFB')
                # BtnSR1.config(state='disabled')
                # BtnSR2.config(state='disabled')
                l_ip.config(text='Sphinx SR')  # Put the text on the label
                speech_status = 1

            elif 'TestVersion' in str(code_car):
                TestMode = 1
                BtnSR3.config(fg='#FFFFFF', bg='#F44336')
                BtnOCV.config(fg='#FFFFFF', bg='#F44336')