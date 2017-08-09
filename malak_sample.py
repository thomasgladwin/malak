import sys
import serial
import time

try:
    arduino = serial.Serial('COM5', 9600)
    time.sleep(1) # Allow Arduino to reset after opening port
except Exception as e:
    print(e)

collecting = 1
discarding = 1
while collecting == 1:
	byteval = arduino.readline()
	try:
		val = byteval.decode()
	except:
		continue
	val_list = val.split()
	if (len(val_list) >= 2):
		print(val_list[0] + "\t" + val_list[1] + "\n")
		sys.stdout.flush()

arduino.close()
