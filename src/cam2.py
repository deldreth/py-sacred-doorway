from doorway.doorway import Doorway
from time import sleep
from collections import deque
import picamera
import picamera.array
import PIL

import io

sacred  = Doorway(client="192.168.1.104:7890")

while True:
	with picamera.PiCamera() as camera:
		stream = io.BytesIO()
		for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
			stream.truncate()
			stream.seek(0)

			image = PIL.Image.open(stream.getvalue())

			image = stream.array

			pilImage = PIL.Image.fromarray(image).rotate(90).resize((28, 7))
			pixels   = pilImage.load()

			del image

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

"""
while True:
	with picamera.PiCamera() as camera:
		camera.resolution = (640, 480)
		camera.framerate = 30
		camera.shutter_speed = camera.exposure_speed
		camera.exposure_mode = 'off'
		g = camera.awb_gains
		camera.awb_mode = 'off'
		camera.awb_gains = g

		with picamera.array.PiRGBArray(camera) as stream:
			for cont in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
			camera.capture(stream, format='bgr', use_video_port=True)
			image = stream.array

			pilImage = PIL.Image.fromarray(image).rotate(90).resize((28, 7))
			pixels   = pilImage.load()

			del image

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
"""