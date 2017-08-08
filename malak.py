import serial
import time
import pygame
from pygame.locals import *

savefilename = input("Save to .log file with base name: ")
savefilename = savefilename + ".log"
print("Saving data to " + savefilename)
print('\n')

try:
    arduino = serial.Serial('COM3', 9600)
    time.sleep(1) # Allow Arduino to reset after opening port
    print("Connection established succesfully!\n")
except Exception as e:
    print(e)

file2write = open(savefilename, 'w')

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Malak: Psychophysiology measurement')
screen.fill((55,55,55))
myFont = pygame.font.SysFont("Times New Roman", 18)

collecting = 1
discarding = 1
while collecting == 1:
	byteval = arduino.readline()
	val = byteval.decode()
	# Val is now a string with tabs
	val_list = val.split()
	if val:
		if discarding == 0:
			screen.fill((55,55,55))

			valDisplay = myFont.render(val_list[0] + ", " + val_list[1], 1, (0, 255, 0))
			screen.blit(valDisplay, (10, 50))

			for n in range(0, len(val_list)):
				t = (375 - 100) * int(val_list[n]) / 1000
				pygame.draw.rect(screen, (200, 200, 200), (50 + 20 * n, 375, 10, -t))

			pygame.display.flip()

			# print("val = >>>" + val + "<<<")
			file2write.write(val)
		else:
			discarding = 0
	else:
		print("Nothing on the line.")
	for event in pygame.event.get():
		# print(event);
		if (event.type == pygame.QUIT):
			print("Ending measurement...")
			collecting = 0

pygame.display.quit()
file2write.close()
arduino.close()

# C:\Users\Thomas\AppData\Local\Programs\Python\Python36-32\python "$(FULL_CURRENT_PATH)"