#!/usr/bin/python

color_bg        = '#54545A'     #Set background color
color_text      = '#E1F5FE'     #Set text color
#color_btn      = '#212121'     #Set button color
color_btn       = '#08979B'     #Set button color
color_line      = '#01579B'     #Set line color
color_can       = '#212121'     #Set canvas color
color_oval      = '#2196F3'     #Set oval color
target_color    = '#FF6D00'

a2t             = ''
TestMode        = 0

ADDR            = ''
tcpClicSock     = ''            #A global variable,for future socket connection
BUFSIZ          = 1024          #Set a buffer size
ip_stu          = 1             #Shows connection status
mainloop_status = 0             #A status value,ensure the mainloop() runs only once

#Global variables of input status
c_f_stu = 0
c_b_stu = 0
c_l_stu = 0
c_r_stu = 0

b_l_stu = 0
b_r_stu = 0

l_stu = 0
r_stu = 0

BtnIP = ''
ipaddr = ''

led_status      = 0
opencv_status   = 0
auto_status     = 0
speech_status   = 0
findline_status = 0

ipcon           = 0
SR_mode         = 0
