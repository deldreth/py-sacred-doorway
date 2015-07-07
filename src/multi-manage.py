from SimpleCV import *
from SimpleCV.Display import *
from collections import deque
from time import sleep
from PIL import Image, ImageOps

import multiprocessing

from doorway.doorway import Doorway

cam     = Camera(threaded=False) # Threaded by default, and boy if it doesn't freak everything out. Something something... multiple processes grabbing thread data at a time, wooo
#display = Display((640, 480))

sacred  = Doorway()

def proc_camera (manager_dict, images):
	"""
	Camera handling PROCESS. If the manager dictionary says there is light...
	unthreaded buffer an image from the camera and display.
	"""

	global cam
	#global display
	global sacred

	def draw_camera (sacred, image):
		print image	
		pilImage = image.getPIL().rotate(90).resize((28, 7))
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
				sacred.bow()

	while True:	
		if manager_dict['has_light']:
			#print "Light dectected!"

			""" It has been 5 seconds, is there still a light source? """

			if manager_dict['tick'] > 5:
				while manager_dict['has_light']:
					draw_camera(sacred, images.get())

		else:
			print "No light detected!"
			sleep(1)

def proc_animation (manager_dict):

	global sacred

	def draw_animation (sacred):
		for x in range(256):
			if manager_dict['has_light']:
				return

			sacred.put(1, rgb = wheel(x))
			sacred.put(2, rgb = wheel(x+10))
			sacred.put(3, rgb = wheel(x+20))
			sacred.put(4, rgb = wheel(x+30))
			sacred.put(5, rgb = wheel(x+20))
			sacred.put(6, rgb = wheel(x+10))
			sacred.put(7, rgb = wheel(x))
			sacred.bow(0.01)

	def wheel(value):
		""" Given 0-255, make an rgb color """

		if value < 85:
			return (value * 3, 255 - value * 3, 0)
		elif value < 170:
			value -= 85
			return (255 - value * 3, 0, value * 3)
		else:
			value -= 170
			return (0, value * 3, 255 - value * 3)

	while True:
		if not manager_dict['has_light']:
			draw_animation(sacred)
		else:
			print "Not animating..."
			sleep(1)

def thread_control (pipe):
	"""
	Toggling state THREAD... if light is detected global manager dictionay will be updated, other processes respond accordingly.

	It will 'poll' every second to determine which process should be running
	"""

	global cam
	global d

	while True:
		img = cam.getImage()

		hls = img.toHLS()
		h, l, s = img.splitChannels()
		l = l.threshold(200)

		blobs = l.findBlobs(150, minsize=200)

		if blobs:
			d['has_light'] = True
			d['tick'] += 1
			pipe.put(img)
		else:
			d['has_light'] = False
			d['tick'] = 0

		sleep(0.04)

manager  = multiprocessing.Manager()
d = manager.dict({'has_light' : False, 'tick' : 0})

img_pipe = multiprocessing.Queue()

camera = multiprocessing.Process(target=proc_camera, args=(d, img_pipe))
camera.daemon = True
camera.start()

animation = multiprocessing.Process(target=proc_animation, args=(d,))
animation.daemon = True
animation.start()

#t = threading.Timer(1, thread_control)
#t.start()

thread_control(img_pipe)