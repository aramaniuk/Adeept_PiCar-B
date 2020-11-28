#!/usr/bin/python
import time
import threading as thread
from socket import socket, AF_INET, SOCK_STREAM
import enum
from clientpkg.eventhook import EventHook


# Event types received from the car
class EventTypes(enum.Enum):
    ConnectionStatus = 1
    ConnectionError = 2
    ConnectionSuccess = 3
    CarSettings = 4
    UltraSonicData = 5
    CarStatus = 6


# CarStatus event subitems
class CarStatus(enum.Enum):
    csMoveForward = 1
    csMoveBackward = 2
    csTurnLeft = 3
    csTurnRight = 4
    csLookUp = 5
    csLookDown = 6
    csLookLeft = 7
    csLookRight = 8
    csStop = 9
    csFollowModeOn = 0
    csFindLine = 10
    csLightsOn = 11
    csLightsOff = 12
    csOpenCVOn = 13
    csOpenCVOff = 14
    csSphinxSR = 15
    csTestVersion = 16


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

    @classmethod
    def CarStatus(cls, carStatus, statusCode):
        cls.carStatus = carStatus
        cls.statusCode = statusCode
        return cls(EventTypes.CarStatus)


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
        self.ip_stu = 1  # Shows connection status
        self.BUFSIZ = 1024  # Define buffer size for reading from socket

        self.led_status = 0
        self.opencv_status = 0
        self.auto_status = 0
        self.speech_status = 0
        self.findline_status = 0
        self.tcpClientSock = ''
        self.TestMode = 0

        self.on_connection_status = EventHook()
        self.on_connection_success = EventHook()
        self.on_connection_error = EventHook()
        self.on_car_settings = EventHook()
        self.on_ultrasonic_data = EventHook()
        self.on_car_status = EventHook()

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
            self.on_car_settings.fire(event.settings)
        elif event.type == EventTypes.UltraSonicData:
            self.on_ultrasonic_data.fire(event.ultraSonicData)
        elif event.type == EventTypes.CarStatus:
            self.on_car_status.fire(event.carStatus, event.statusCode)

    def call_forward(self, speed):  # When this function is called,client commands the car to move forward
        if self.c_f_stu == 0:
            #normalize speed
            speed = 0.4+0.6*speed
            command='forward:'+str(speed)
            self.tcpClientSock.send(command.encode())
            self.c_f_stu = 1

    def call_back(self, speed):  # When this function is called,client commands the car to move backward
        if self.c_b_stu == 0:
            # normalize speed
            speed = 0.4 + 0.6 * speed
            command = 'backward:' + str(speed)
            self.tcpClientSock.send(command.encode())
            self.c_b_stu = 1

    def call_stop(self):  # When this function is called,client commands the car to stop moving
        self.c_f_stu = 0
        self.c_b_stu = 0
        self.tcpClientSock.send('stop'.encode())

    def call_center(self):  # When this function is called,client commands the car go straight
        self.c_r_stu = 0
        self.c_l_stu = 0
        self.tcpClientSock.send('middle'.encode())

    def call_Left(self):  # When this function is called,client commands the car to turn left
        if self.c_l_stu == 0:
            #self.tcpClientSock.send('Left'.encode())
            self.c_l_stu = 1

    def call_Right(self):  # When this function is called,client commands the car to turn right
        if self.c_r_stu == 0:
            #self.tcpClientSock.send('Right'.encode())
            self.c_r_stu = 1

    def call_look_left(self):  # Camera look left
        self.tcpClientSock.send('l_le'.encode())

    def call_look_right(self):  # Camera look right
        self.tcpClientSock.send('l_ri'.encode())

    def call_look_up(self):  # Camera look up
        self.tcpClientSock.send('l_up'.encode())

    def call_look_down(self):  # Camera look down
        self.tcpClientSock.send('l_do'.encode())

    def call_ahead(self):  # Camera look ahead
        self.tcpClientSock.send('ahead'.encode())
        print('ahead')

    def call_auto(self):  # When this function is called,client commands the car to start auto mode
        if self.auto_status == 0:
            self.tcpClientSock.send('auto'.encode())
        else:
            self.tcpClientSock.send('Stop'.encode())

    def call_exit(self):  # When this function is called,client commands the car to shut down
        self.tcpClientSock.send('exit'.encode())

    def call_Stop(self):  # When this function is called,client commands the car to switch off auto mode
        self.tcpClientSock.send('Stop'.encode())

    def scan(self):  # When this function is called,client commands the ultrasonic to scan
        self.tcpClientSock.send('scan'.encode())
        print('scan')

    def find_line(self):  # Line follow mode
        if self.findline_status == 0:
            self.tcpClientSock.send('findline'.encode())
        else:
            self.tcpClientSock.send('Stop'.encode())

    def lights_ON(self):  # Turn on the LEDs
        if self.led_status == 0:
            self.tcpClientSock.send('lightsON'.encode())
        else:
            self.tcpClientSock.send('lightsOFF'.encode())

    def call_SR3(self):  # Start speech recognition mode
        if self.speech_status == 0:
            self.tcpClientSock.send('voice_3'.encode())
        else:
            self.tcpClientSock.send('Stop'.encode())

    def call_opencv(self):  # Start OpenCV mode
        if self.opencv_status == 0:
            self.tcpClientSock.send('opencv'.encode())
        else:
            self.tcpClientSock.send('Stop'.encode())

    def socket_disconnect(self):
        print("socket disconnect")
        if self.tcpClientSock != '':
            self.tcpClientSock.close()  # Close socket or it may not connect with the server again

    def socket_connect(self, ip_adr):  # Call this function to connect with the server
        print("socket_connect thread connecting to " + ip_adr)
        self.fire_events(CarControllerEvent.ConnectionStatus('Connecting...'))

        server_ip = ip_adr
        server_port = 10223  # Define port serial
        addr = (server_ip, server_port)
        self.tcpClientSock = socket(AF_INET, SOCK_STREAM)  # Set connection value for socket

        for i in range(1, 6):  # Try 5 times if disconnected
            try:
                if self.ip_stu == 1:
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
            except Exception as e:
                print("Cannot connect to server " + str(e))
                self.fire_events(CarControllerEvent.ConnectionStatus('Trying %d/5 time(s)' % i))
                print('Trying %d/5 time(s)' % i)
                self.ip_stu = 1
                self.tcpClientSock.close()
                time.sleep(1)
                continue
        if self.ip_stu == 1:
            self.fire_events(CarControllerEvent.ConnectionError('Disconnected'))

    def code_receive(self):  # A function for data receiving
        print("code receive thread started")
        # global led_status, ipcon, findline_status, auto_status, opencv_status, speech_status, TestMode
        while True:
            code_car = self.tcpClientSock.recv(self.BUFSIZ)  # Listening,and save the data in 'code_car'
            # l_ip.config(text=code_car)  # Put the data on the label
            print("received from car: " + str(code_car))
            if not code_car:
                continue
            elif 'SET' in str(code_car):  # settings received from car
                print('car settings')
                set_list = code_car.decode()
                self.fire_events(CarControllerEvent.CarSettings(set_list))

            elif 'list' in str(code_car):  # Scan result receiving start
                list_str = code_car.decode()
                while True:  # Save scan result in dis_list
                    code_car = self.tcpClientSock.recv(self.BUFSIZ)
                    if 'finished' in str(code_car):
                        break
                    list_str += code_car.decode()
                self.fire_events(CarControllerEvent.UltraSonicData(list_str))

            elif '1' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Moving Forward', CarStatus.csMoveForward))
                self.c_f_stu = 0
            elif '2' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Moving Backward', CarStatus.csMoveBackward))
                self.c_b_stu = 0
            elif '3' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Turning Left', CarStatus.csTurnLeft))
                self.c_l_stu = 0
            elif '4' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Turning Right', CarStatus.csTurnRight))
                self.c_r_stu = 0
            elif '5' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Look Up', CarStatus.csLookUp))
            elif '6' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Look Down', CarStatus.csLookDown))
            elif '7' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Look Left', CarStatus.csLookLeft))
            elif '8' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Look Right', CarStatus.csLookRight))
            elif '9' in str(code_car):  # Translate the code to text
                self.fire_events(CarControllerEvent.CarStatus('Stop', CarStatus.csStop))
            elif '0' in str(code_car):  # Translate the code to text
                self.auto_status = 1
                self.fire_events(CarControllerEvent.CarStatus('Follow Mode On', CarStatus.csFollowModeOn))

            elif 'findline' in str(code_car):  # Translate the code to text
                self.findline_status = 1
                self.fire_events(CarControllerEvent.CarStatus('Find Line', CarStatus.csFindLine))

            elif 'lightsON' in str(code_car):  # Translate the code to text
                self.led_status = 1
                self.fire_events(CarControllerEvent.CarStatus('Lights On', CarStatus.csLightsOn))

            elif 'lightsOFF' in str(code_car):  # Translate the code to text
                self.led_status = 0
                self.fire_events(CarControllerEvent.CarStatus('Lights OFF', CarStatus.csLightsOff))

            elif 'oncvon' in str(code_car):
                if self.TestMode == 0:
                    self.opencv_status = 1
                    self.fire_events(CarControllerEvent.CarStatus('OpenCV ON', CarStatus.csOpenCVOn))

            elif 'auto_status_off' in str(code_car):
                self.findline_status = 0
                self.speech_status = 0
                self.opencv_status = 0
                self.auto_status = 0
                self.fire_events(CarControllerEvent.CarStatus('Auto Status Off', CarStatus.csOpenCVOff))

            elif 'voice_3' in str(code_car):
                self.speech_status = 1
                self.fire_events(CarControllerEvent.CarStatus('Sphinx SR', CarStatus.csSphinxSR))

            elif 'TestVersion' in str(code_car):
                self.TestMode = 1
                self.fire_events(CarControllerEvent.CarStatus('Test Version', CarStatus.csTestVersion))
