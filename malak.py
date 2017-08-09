import serial
import time
import pygame
from pygame.locals import *
import os
import subprocess
import math
import random
import winsound

savefilename = input("Save to .log file with base name: ")
savefilename = savefilename + ".log"
print("Saving data to " + savefilename)
print('\n')

file2write = open(savefilename, 'w')

process = subprocess.Popen(['python','malak_sample.py'], stdout=subprocess.PIPE)

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Malak')
screen.fill((155,155,55))
myFont = pygame.font.SysFont("Times New Roman", 18)

Fs = 100
T = 4
nSamples = math.ceil(Fs * T)
HR_min = 40
HR_max = 140
IBI_min = 60 / HR_max
IBI_max = 60 / HR_min
IBI_min_samples = math.ceil(IBI_min * Fs)
signal = [0 for i in range(nSamples)]

newcalc_nSamples = math.ceil(0.2 * Fs) # 

collecting = 1
iSample = 0
while collecting == 1:
	val = process.stdout.readline()
	val = val.decode()
	val = val.strip()
	file2write.write(val)
	
	if (val == ""):
		continue

	val_list = val.split()
	PPG_val = int(val_list[0])
	light_val = int(val_list[1])
	
	# Update signal
	for i in range(len(signal) - 1):
		signal[i] = signal[i + 1]
	signal[len(signal) - 1] = PPG_val + 0.1 * random.random()
	
	iSample = (iSample + 1) % newcalc_nSamples
	if iSample != 0:
		continue

	# Detect peaks
	peakv = [0 for i in range(nSamples)]
	IBI_samples = []
	for i in range(len(signal) - 1):
		h = math.ceil(IBI_min_samples)
		a = max(0, i - h)
		b = min(len(peakv) - 1, i + h)
		i_is_peak = 1
		for j in range(a, b):
			if i == j:
				continue
			if (signal[i] <= signal[j]):
				i_is_peak = 0
		peakv[i] = i_is_peak
		if (i_is_peak == 1):
			IBI_samples.append(i)

	# Remove neighbouring samples with equal max values
	# ...

	print(IBI_samples)

	IBI_sum = 0
	IBI_N = 0
	for i in range(len(IBI_samples) - 1):
		this_IBI_samples = IBI_samples[i + 1] - IBI_samples[i]
		this_IBI = this_IBI_samples / Fs
		print(str(this_IBI) + " [" + str(IBI_min) + ", " + str(IBI_max) + "]")
		if (this_IBI < IBI_min or this_IBI > IBI_max):
			continue
		IBI_sum = IBI_sum + this_IBI
		IBI_N = IBI_N + 1

	# Calculate HR
	if IBI_N > 0:
		IBI_mean = IBI_sum / IBI_N
	else:
		IBI_mean = 1
	HR = 60 / IBI_mean

	# Visualization
	screen.fill((55,55,55))
	valDisplay = myFont.render("HR: " + str(HR), 1, (0, 255, 0))
	screen.blit(valDisplay, (10, 50))

	# Signal and peakdetection feedback
	for i in range(len(signal) - 1):
		dx = 1
		x1 = 10 + i * dx
		x2 = 10 + (i + 1) * dx
		y1 = 300 - signal[i] / 5
		y2 = 300 - signal[i + 1] / 5
		pygame.draw.line(screen, (200, 0, 70), (x1, y1), (x2, y2), 1)
		y1 = 300 - peakv[i] * 100
		y2 = 300 - peakv[i + 1] * 100
		pygame.draw.line(screen, (30, 140, 40), (x1, y1), (x2, y2), 3)

	# HR representation
	HR_normed = (HR - HR_min) / (HR_max - HR_min)
	t = (375 - 100) * HR_normed
	pygame.draw.rect(screen, (HR_normed * 200, 100, 100), (50, 375, 10, -t))
	pygame.display.flip()

	# HR audio representation
	f = int(2000 + 3000 * HR_normed)
	winsound.Beep(f, 50)
	
	# Light sensor
	t = (375 - 100) * light_val / 1000
	pygame.draw.rect(screen, (200, 200, 200), (350, 375, 10, -t))
	pygame.display.flip()	
	
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			print("Ending measurement...")
			collecting = 0

pygame.display.quit()
file2write.close()
