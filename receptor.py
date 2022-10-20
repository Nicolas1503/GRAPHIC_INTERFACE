import serial
import glob
import time
from threading import Lock, Thread
import threading
import sys
from datetime import datetime

print("Opening port from platform : {}".format(sys.platform))

# Create serial port 
#ser = serial.Serial('/dev/tty.usbserial-0001',115200)

# Bytearray to send
rgb = bytearray([3,100,100,150])
upstairs = bytearray([4,0,0,10])
downstaris = bytearray([5,0,0,10])
timer1 = bytearray([6,0,0,10])
timer2 = bytearray([7,0,0,1])

to_send = [rgb,upstairs,downstaris,timer1,timer2]

# Mutex
lock = threading.Lock()

class SerialthreadReceive(Thread):

    def __init__(self,name):
        super().__init__()
        self.name = name

    def run(self):

        # Thread started
        ser = serial.Serial(serial_choose(),9600)
        print("Start thread : {}".format(self.name))
        
        # Forever
        while True:
            lock.acquire()
            line = ser.readline().decode('ascii')
            lock.release()
            print(line)

            data = line.split("'")[1]
            with open('log.txt', 'a') as f:
                f.write(data+ "\n" )

            time.sleep(0.01)

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []

    for port in ports:
        try:
            ser = serial.Serial(port)
            # ser.port = port
            # ser.open()
            ser.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    print(result)
    return result


def serial_choose():
    # serial port
    # levanto la lista de los serial que se pueden abrir.
    available_serial = serial_ports()
    print(available_serial)
    if(len(available_serial) == 0):
        print("No existen puertos serie disponibles para correr el script")
        return

    # if(len(available_serial) == 1):
    #     return available_serial[0]

    # for i in available_serial:
    #     print(i)
    #     if 'usbserial' in i:
    #         return i

    print("SerialPorts available " + str(available_serial))
    print("Choose a SerialPort")
    chosen_serial = str(input())

    print("Puerto serie elegido : " + chosen_serial)
    return chosen_serial

# ser = serial.Serial(serial_choose(),9600)

def start_rcv():
    rcv_loop = SerialthreadReceive('RECEIVE LOOP')
    rcv_loop.start()


# while True:
#     lock.acquire()
#     line = ser.readline().decode('ascii')
#     lock.release()
#     print(line)

#     data = line.split("'")[1]
#     with open('log.txt', 'a') as f:
#         f.write(data+ "\n" )

#     time.sleep(0.01)



