#!/usr/bin/python

from SimpleCV import *
from collections import deque
from time import sleep, time
from PIL import Image
from multiprocessing.managers import BaseManager
from doorway.doorway import Doorway, DoorwayEffects

import multiprocessing
import signal, sys
import datetime
import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight

print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Starting Camera"

cam = Camera(0, threaded=False, prop_set={"width":128, "height":96})

print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Camera Started"

# display = Display((640, 480))

def proc_camera (manager_dict, sacred):
	"""
	Camera handling PROCESS. If the manager dictionary says there is light...
	unthreaded buffer an image from the camera and display.
	"""

	def draw_camera (sacred, image, spixels):
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
					spixels[l] = deq_line[pix_count]
					spixels[r] = deq_line[pix_count]
					pix_count += 1

				sheet_count += 1

		sacred.set_pixels(spixels)
		sacred.bow(0)

	try:
		spixels = [(0, 0, 0) for x in range(392)]
		while True:
			if manager_dict['has_light']:
				""" It has been 5 seconds, is there still a light source? """
				sacred.set_renderable(False)
				if manager_dict['image'] != 0:
					draw_camera(sacred, manager_dict['image'], spixels)
			else:
				sacred.set_renderable(True)
				sleep(1)

	except KeyboardInterrupt:
		pass




def proc_animation (manager_dict, sacred):
	where = [0] # Why is this a list? Because memory that's why. Look it up.

	""" 
	p - a list that contains effects for the presentation state
	check DoorwayEffects for a list of functions 
	"""
	p = [
		{'images' : ['doorway/res/stripes/colorfuls/', 0.05, True]},
		{'images' : ['doorway/res/circles/', 0.07, True]},
		{'images' : ['doorway/res/stripes/', 0.07, True]},
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

	[p.append({'images' : ['doorway/res/pokes/', 0.05, True]}) for _ in range(5)]
	[p.append({'images' : ['doorway/res/elements/water/', 0.01]}) for _ in range(5)]
	[p.append({'images' : ['doorway/res/elements/fire/', 0.01]}) for _ in range(5)]
	[p.append({'images' : ['doorway/res/chakras/', 0.07, True]}) for _ in range(5)]
	[p.append({'images' : ['doorway/res/circles/colorfuls/', 0.01, True]}) for _ in range(5)]

	[p.append({'swipe_down' : [Doorway.color_wheel(random.randrange(255))]}) for _ in range(10)]
	[p.append({'swipe_up'   : [Doorway.color_wheel(random.randrange(255))]}) for _ in range(10)]

	for _ in range(20):
		p.append({'wipe_down' : [random.randrange(1,8), (random.randrange(255), random.randrange(255), random.randrange(255))]})
		p.append({'wipe_up'   : [random.randrange(1,8), (random.randrange(255), random.randrange(255), random.randrange(255))]})

		p.append({'wipe_down' : [random.randrange(1,8), (0, 0, 0)]})
		p.append({'wipe_up'   : [random.randrange(1,8), (0, 0, 0)]})

	[p.append({'picture' : ['doorway/res/chakras/{0}.jpg'.format(x), 0.1]})            for x in range(1, 8)]
	[p.append({'picture' : ['doorway/res/chakras/{0}.jpg'.format(x), 0.1]})            for x in range(1, 8)]
	[p.append({'picture' : ['doorway/res/circles/{0}.jpg'.format(x), 0.05]})           for x in range(1,10)]
	[p.append({'picture' : ['doorway/res/circles/colorfuls/{0}.jpg'.format(x), 0.02]}) for x in range(1,8)]
	[p.append({'picture' : ['doorway/res/circles/{0}.jpg'.format(x), 0.05]})           for x in range(1,10)]
	[p.append({'picture' : ['doorway/res/circles/colorfuls/{0}.jpg'.format(x), 0.05]}) for x in range(1,8)]
	[p.append({'picture' : ['doorway/res/stripes/{0}.jpg'.format(x), 0.07]})           for x in range(1,9)]
	[p.append({'picture' : ['doorway/res/stripes/colorfuls/{0}.jpg'.format(x), 0.07]}) for x in range(1,6)]
	[p.append({'picture' : ['doorway/res/stripes/{0}.jpg'.format(x), 0.05]})           for x in range(1,9)]
	[p.append({'picture' : ['doorway/res/stripes/colorfuls/{0}.jpg'.format(x), 0.05]}) for x in range(1,6)]

	for _ in range(20):
		p.append({'strobe_FtoB' : [5, 0.01, 
			(random.randrange(255), random.randrange(255), random.randrange(255)), 
			(random.randrange(255), random.randrange(255), random.randrange(255))]})
		p.append({'strobe_BtoF' : [5, 0.01, 
			(random.randrange(255), random.randrange(255), random.randrange(255)), 
			(random.randrange(255), random.randrange(255), random.randrange(255))]})
	
	for _ in range(10):
		p.append({'strobe_rainbow_FtoB' : [0.05]})
		p.append({'strobe_rainbow_BtoF' : [0.05]})

	for _ in range(10):
		p.append({'rainbow_FtoB' : [0.07]})
		p.append({'rainbow_BtoF' : [0.07]})

	random.shuffle(p)

	def draw_animation (sacred, pres):
		if where[0] == len(pres) - 1:
			random.shuffle(pres)
			where[0] = 0

		for i, x in enumerate(pres):
			if i < where[0]:
				continue

			where[0] = i
			
			for key, val in x.iteritems():
				if getattr(sacred, key)(*val):
					return

		sleep(0.1)

	try:
		while True:
			if not manager_dict['has_light']:
				draw_animation(sacred, p)
			else:
				sleep(1)
	except KeyboardInterrupt:
		pass



def thread_control (d):
	"""
	Toggling state THREAD... if light is detected global manager dictionay will be updated, other processes respond accordingly.

	It will 'poll' every second to determine which process should be running
	"""

	global cam
	

	def sigterm_handler (signal_no, frame):
		print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), signal_no, "received, exitting."
		sys.exit(0)	

	signal.signal(signal.SIGTERM, sigterm_handler)
	signal.signal(signal.SIGINT, sigterm_handler)

	camera_running = True
	@joystick.on(joystick.BUTTON)
	def handle_press (pin):
		lcd.clear()
		lcd.write("Stopping camera...")
		backlight.rgb(0, 0, 0)
		sleep(0.5)
		print "Stopping camera..."
		camera_running = False
		lcd.clear()
		lcd.write("Camera stopped...")
		sleep(0.5)
		print "Camera stopped..."

	blob_color = 1
	while True:
		print "Running thread control...", True
		if camera_running:
			img = cam.getImage()
			h, l, s = img.toHLS().splitChannels()
			l = l.threshold(145)
			
			blobs = l.findBlobs(minsize=2)
			if blobs:
				mask = SimpleCV.Image(img.size())


				for blob in blobs:
					mask.drawCircle(blob.centroid(), 10, color=Doorway.color_wheel(blob_color), thickness=-1)
				
				blob_color += 1

				if blob_color > 255:
					blob_color = 1

				mask = mask.applyLayers()
				mask = mask.flipVertical().flipHorizontal().rotate(90).scale(28, 7)
				# mask.save(display)

				d['image'] = mask.getPIL()

				d['has_light'] = True
			else:
				d['has_light'] = False
				sleep(1)

			del img
			sleep(0.01)
		else:
			print "Animating only..."
			d['has_light'] = False
			sleep(1)

# Proxy the DoorwayEffects class to the main process's daemonic children
bm = BaseManager()
bm.register('DoorwayEffects', DoorwayEffects)
bm.start()
sacred = bm.DoorwayEffects()

manager  = multiprocessing.Manager()
d = manager.dict({'has_light' : False, 'image' : 0})

print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Init proc_camera"

camera = multiprocessing.Process(name="sacred_camera",target=proc_camera, args=(d, sacred, ))
camera.daemon = True
camera.start()

print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Started proc_camera"


print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Init proc_animation"

animation = multiprocessing.Process(name="sacred_animations", target=proc_animation, args=(d, sacred, ))
animation.daemon = True
animation.start()

print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Started proc_animation"


print datetime.datetime.now().strftime('%b %d, %G %I:%M%p--'), "Init control, running..."

thread_control(d)