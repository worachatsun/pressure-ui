import os
import sys
import serial
from time import sleep

class Arduino:
    def __init__(self, port):
        self.dev = serial.Serial(port, baudrate=9600)
        sleep(1)

    def query(self, message):
        self.dev.write(message.encode('ascii'))
        line = self.dev.readline().decode('ascii').strip()
        return line

ard = Arduino('COM3')
filename = "data/pressure/" + sys.argv[1] +".csv"
os.makedirs(os.path.dirname(filename), exist_ok=True)

while True:
    f = open(filename, "a")
    f.write(ard.query('0')+"\n")
    f.close()

