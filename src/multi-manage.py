#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from collections import deque
from time import sleep, time
from PIL import Image

import multiprocessing

from doorway.doorway import Doorway

cam     = Camera(1, threaded=False, prop_set={"width":128, "height":96}) # Threaded by default, and boy if it doesn't freak everything out. Something something... multiple processes grabbing thread data at a time, wooo
# display = Display((640, 480))

sacred  = Doorway()

def proc_camera (manager_dict):
	"""
	Camera handling PROCESS. If the manager dictionary says there is light...
	unthreaded buffer an image from the camera and display.
	"""
	global sacred

	def draw_camera (sacred, image):
		# Process transition animation
		if not manager_dict['has_light']:
			sacred.put(2, rgb=(0, 0, 0))
			sacred.put(3, rgb=(0, 0, 0))
			sacred.put(4, rgb=(0, 0, 0))
			sacred.put(5, rgb=(0, 0, 0))
			sacred.put(6, rgb=(0, 0, 0))
			sacred.put(7, rgb=(0, 0, 0))

			start = time()
			while time() - start <= 3:
				sacred.put(1, rgb=(255, 255, 255))
				sacred.bow(0.5)
				sacred.put(1, rgb=(0, 0, 0))
				sacred.bow(0.5)

		 	return

		pilImage = image.rotate(90).resize((28, 7))
		pixels   = pilImage.load()

		#image.save(display)
		#sleep(0.04) #Eh?
		lines = []
		for y in range(pilImage.size[1]):
			xs = []
			for x in range(pilImage.size[0]):
				xs.append(pixels[x, y])

			lines.append(xs)
			del xs

		deq = deque(maxlen=7)

		for line in lines:
			deq.append(line)
			sheet_count = 1
			for deq_line in deq:
				pix_count = 0
				for l,r in sacred.sheets[sheet_count]:
					sacred.pixels[l] = deq_line[pix_count]
					sacred.pixels[r] = deq_line[pix_count]
					pix_count += 1

				sheet_count += 1
			sacred.bow(0)

	while True:
		if manager_dict['has_light'] and time() - manager_dict['cam_timer'] >= 5:
			""" It has been 5 seconds, is there still a light source? """
			if manager_dict['image'] != 0:
				draw_camera(sacred, manager_dict['image'])
			else:
				print "No image!"

		else:
			print "No camera."
			sleep(1)




def proc_animation (manager_dict):

	global sacred

	def draw_animation (sacred):
		for x in range(256):
			# Process transition animation
			if manager_dict['has_light']:
				sacred.put(2, rgb=(0, 0, 0))
				sacred.put(3, rgb=(0, 0, 0))
				sacred.put(4, rgb=(0, 0, 0))
				sacred.put(5, rgb=(0, 0, 0))
				sacred.put(6, rgb=(0, 0, 0))
				sacred.put(7, rgb=(0, 0, 0))

				start = time()
				while time() - start <= 3:
					sacred.put(1, rgb=(255, 255, 255))
					sacred.bow(0.5)
					sacred.put(1, rgb=(0, 0, 0))
					sacred.bow(0.5)

			 	return

			sacred.put(1, rgb = Doorway.color_wheel(x))
			sacred.put(2, rgb = Doorway.color_wheel(x+10))
			sacred.put(3, rgb = Doorway.color_wheel(x+20))
			sacred.put(4, rgb = Doorway.color_wheel(x+30))
			sacred.put(5, rgb = Doorway.color_wheel(x+20))
			sacred.put(6, rgb = Doorway.color_wheel(x+10))
			sacred.put(7, rgb = Doorway.color_wheel(x))
			sacred.bow(0.01)

	while True:
		if not manager_dict['has_light'] and time() - manager_dict['ani_timer'] >= 5:
			draw_animation(sacred)
		else:
			print "No animation."
			sleep(1)




def thread_control (d):
	"""
	Toggling state THREAD... if light is detected global manager dictionay will be updated, other processes respond accordingly.

	It will 'poll' every second to determine which process should be running
	"""

	global cam

	x = 0
	while True:
		img = cam.getImage().flipVertical()

		h, l, s = img.toHLS().splitChannels()
		l = l.threshold(150)

		# blobs = l.findBlobs(150, minsize=5)

		blobs = l.findBlobs(minsize=2)
		if blobs:
			mask = SimpleCV.Image(img.size())

			count = 1
			for blob in blobs:
				if count > 2:
					continue
				cx, cy = blob.centroid()

				mask.drawCircle((cx, cy), 8, color=Doorway.color_wheel(x), thickness=-1)
				mask.drawCircle((cx + 20, cy), 8, color=Doorway.color_wheel(x), thickness=-1)
				mask.drawCircle((cx - 20, cy), 8, color=Doorway.color_wheel(x), thickness=-1)
				x += 2

				count += 1

			mask = mask.applyLayers()
			mask = mask.flipHorizontal()
			# mask.save(display)

			d['image'] = mask.getPIL()

			d['has_light'] = True
			d['ani_timer'] = 0

			if not d['cam_timer']:
				d['cam_timer'] = time()
		else:
			d['has_light'] = False
			d['cam_timer'] = 0

			if not d['ani_timer']:
				d['ani_timer'] = time()

		if x > 250:
			x = 0

		sleep(1/30)

manager  = multiprocessing.Manager()
d = manager.dict({'has_light' : False, 'image' : 0, 'cam_timer' : 0, 'ani_timer' : 5})

camera = multiprocessing.Process(target=proc_camera, args=(d,))
camera.daemon = True
camera.start()

animation = multiprocessing.Process(target=proc_animation, args=(d,))
animation.daemon = True
animation.start()

thread_control(d)