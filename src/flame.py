#!/usr/bin/python

from doorway.doorway import Doorway
from time import sleep
from PIL import Image
from collections import deque

sacred = Doorway()

sleep(5)

deq = deque(maxlen=7)

while True:
	for line in sacred.pics():
		deq.append(line)
		sheet_count = 1
		for deq_line in deq:
			pix_count = 0
			for l,r in sacred.sheets[sheet_count]:
				sacred.pixels[l] = deq_line[pix_count]
				sacred.pixels[r] = deq_line[pix_count]
				pix_count += 1
				
			sheet_count += 1
			sacred.bow()
		sleep(0.01)