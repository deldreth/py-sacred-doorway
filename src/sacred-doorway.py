#!/usr/bin/python

from SimpleCV import *
from SimpleCV.Display import *
from collections import deque
from time import sleep, time
from PIL import Image

import multiprocessing
import numpy

from multiprocessing.managers import BaseManager

from doorway.doorway import Doorway, DoorwayEffects

cam = Camera(0, prop_set={"width":128, "height":96}) # Threaded by default, and boy if it doesn't freak everything out. Something something... multiple processes grabbing thread data at a time, wooo
#display = Display((640, 480))

def proc_camera (manager_dict, sacred):
	"""
	Camera handling PROCESS. If the manager dictionary says there is light...
	unthreaded buffer an image from the camera and display.
	"""

	def draw_camera (sacred, image):
		pixels   = image.load()

		lines = []
		for y in range(image.size[1]):
			xs = []
			for x in range(image.size[0]):
				xs.append(pixels[x, y])

			lines.append(xs)
			del xs

		deq = deque(maxlen=7)

		for line in lines:
			deq.append(line)
			sheet_count = 1
			for deq_line in deq:
				pix_count = 0
				for l,r in sacred.get_sheets()[sheet_count]:
					sacred.set_pixel(l, deq_line[pix_count])
					sacred.set_pixel(r, deq_line[pix_count])
					pix_count += 1

				sheet_count += 1
			sacred.bow(0)

	while True:
		if manager_dict['has_light']:
			""" It has been 5 seconds, is there still a light source? """
			sacred.set_renderable(False)
			if manager_dict['image'] != 0:
				draw_camera(sacred, manager_dict['image'])
		else:
			sacred.set_renderable(True)
			sleep(1)




def proc_animation (manager_dict, sacred):
	where = [0]

	""" 
	p - a list that contains effects for the presentation state
	check DoorwayEffects for a list of functions 
	"""
	p = [
		{'images' : ['doorway/res/stripes/colorfuls/', 0.02]},
		{'images' : ['doorway/res/circles/', 0.01]},
		{'images' : ['doorway/res/stripes/', 0.01]},
		{'rainbow_FtoB' : [ 0.01 ] },
		{'rainbow_BtoF' : [ 0.01 ] },
		{'wipe_down' : [ 1 ] },
		{'wipe_up' : [ 2 ] },
		{'wipe_down' : [ 3 ] },
		{'wipe_up' : [ 4 ] },
		{'wipe_down' : [ 5 ] },
		{'wipe_up' : [ 6 ] },
		{'wipe_down' : [ 7 ] },
		{'strobe_FtoB' : [] },
		]

	[p.append({'images' : ['doorway/res/elements/water/', 0.05]}) for _ in range(1)]
	[p.append({'images' : ['doorway/res/elements/fire/', 0.05]}) for _ in range(1)]

	[p.append({'picture' : ['doorway/res/circles/colorfuls/{0}.jpg'.format(x), 0.02]}) for x in range(1,8)]

	[p.append({'swipe_down' : [Doorway.rand_color()]}) for _ in range(5)]
	[p.append({'swipe_up' : [Doorway.rand_color()]}) for _ in range(5)]

	for _ in range(20):
		p.append({'wipe_down' : [random.randrange(1,8), (random.randrange(255), random.randrange(255), random.randrange(255))]})
		p.append({'wipe_up' : [random.randrange(1,8), (random.randrange(255), random.randrange(255), random.randrange(255))]})

	[p.append({'picture' : ['doorway/res/chakras/{0}.jpg'.format(x), 0.1]})            for x in range(1, 8)]
	[p.append({'picture' : ['doorway/res/chakras/vectors/{0}.jpg'.format(x), 0.1]})    for x in range(8)]
	[p.append({'picture' : ['doorway/res/chakras/{0}.jpg'.format(x), 0.1]})            for x in range(1, 8)]
	[p.append({'picture' : ['doorway/res/chakras/vectors/{0}.jpg'.format(x), 0.1]})    for x in range(8)]
	[p.append({'picture' : ['doorway/res/circles/{0}.jpg'.format(x), 0.05]})           for x in range(1,10)]
	[p.append({'picture' : ['doorway/res/circles/colorfuls/{0}.jpg'.format(x), 0.02]}) for x in range(1,8)]
	[p.append({'picture' : ['doorway/res/circles/{0}.jpg'.format(x), 0.05]})           for x in range(1,10)]
	[p.append({'picture' : ['doorway/res/circles/colorfuls/{0}.jpg'.format(x), 0.02]}) for x in range(1,8)]
	[p.append({'picture' : ['doorway/res/stripes/{0}.jpg'.format(x), 0.01]})           for x in range(1,9)]
	[p.append({'picture' : ['doorway/res/stripes/colorfuls/{0}.jpg'.format(x), 0.01]}) for x in range(1,6)]
	[p.append({'picture' : ['doorway/res/stripes/{0}.jpg'.format(x), 0.01]})           for x in range(1,9)]
	[p.append({'picture' : ['doorway/res/stripes/colorfuls/{0}.jpg'.format(x), 0.01]}) for x in range(1,6)]

	for _ in range(5):
		p.append({'strobe_FtoB' : [5, 0.01, 
			(random.randrange(255), random.randrange(255), random.randrange(255)), 
			(random.randrange(255), random.randrange(255), random.randrange(255))]})
		p.append({'strobe_BtoF' : [5, 0.01, 
			(random.randrange(255), random.randrange(255), random.randrange(255)), 
			(random.randrange(255), random.randrange(255), random.randrange(255))]})
	
	for _ in range(2):
		p.append({'strobe_rainbow_FtoB' : []})
		p.append({'strobe_rainbow_BtoF' : []})

	for _ in range(2):
		p.append({'rainbow_FtoB' : [0.01]})
		p.append({'rainbow_BtoF' : [0.01]})

	def draw_animation (sacred):
		if where[0] == len(p) - 1:
			random.shuffle(p)
			where[0] = 0

		for i, x in enumerate(p):
			if i < where[0]:
				continue

			where[0] = i
			for key, val in x.iteritems():
				if getattr(sacred, key)(*val):
					return

	while True:
		if not manager_dict['has_light']:
			print "animating"
			draw_animation(sacred)
		else:
			sleep(1)



def thread_control (d):
	"""
	Toggling state THREAD... if light is detected global manager dictionay will be updated, other processes respond accordingly.

	It will 'poll' every second to determine which process should be running
	"""

	global cam

	x = 1
	while True:
		img = cam.getImage().flipVertical()

		h, l, s = img.toHLS().splitChannels()
		l = l.threshold(200)

		# blobs = l.findBlobs(150, minsize=5) # For a capture, like, 640 x 480

		blobs = l.findBlobs(minsize=5)
		if blobs:
			mask = SimpleCV.Image(img.size())

			for blob in blobs:
				cx, cy = blob.centroid()
				# mask.drawRectangle(cx-20, cy-30, 20, 20, color=Doorway.color_wheel(x+20), width=0)
				# mask.drawRectangle(cx, cy-40, 20, 40, color=Doorway.color_wheel(x), width=0)
				# mask.drawRectangle(cx+20, cy-30, 20, 20, color=Doorway.color_wheel(x+20), width=0)
				mask.drawCircle((cx, cy), 15, color=Doorway.nog_color_wheel(x), thickness=-1)
				# mask.drawCircle((cx + 20, cy), 10, color=Doorway.color_wheel(x+5), thickness=-1)
				# mask.drawCircle((cx - 20, cy), 10, color=Doorway.color_wheel(x+10), thickness=-1)
				# mask.drawCircle((cx, cy+10), 10, color=Doorway.color_wheel(x+15), thickness=-1)
				# mask.drawCircle((cx, cy-10), 10, color=Doorway.color_wheel(x+20), thickness=-1)
			x += 1

			mask = mask.applyLayers()
			mask = mask.flipHorizontal().rotate(90).scale(28, 7)

			d['image'] = mask.getPIL()

			d['has_light'] = True
			# d['ani_timer'] = 0

			# if not d['cam_timer']:
			# 	d['cam_timer'] = time()
			sleep(0.01)
		else:
			d['has_light'] = False
			# d['cam_timer'] = 0

			# if not d['ani_timer']:
			# 	d['ani_timer'] = time()
			sleep(1)

		if x > 230:
			x = 1

bm = BaseManager()
bm.register('DoorwayEffects', DoorwayEffects)
bm.start()
sacred = bm.DoorwayEffects()

manager  = multiprocessing.Manager()
d = manager.dict({'has_light' : False, 'image' : 0, 'cam_timer' : 0, 'ani_timer' : 5})

camera = multiprocessing.Process(target=proc_camera, args=(d, sacred, ))
camera.daemon = True
camera.start()

animation = multiprocessing.Process(target=proc_animation, args=(d, sacred, ))
animation.daemon = True
animation.start()

thread_control(d)
