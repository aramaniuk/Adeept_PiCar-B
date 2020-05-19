#!/bin/sh

IP=192.168.10.16

ssh pi@${IP} 'sudo /home/pi/startup.sh stop'
scp *.py pi@${IP}:/home/pi/adeept_picar-b/server/
scp *.txt pi@${IP}:/home/pi/adeept_picar-b/server/
ssh pi@${IP} 'sudo /home/pi/startup.sh start &'