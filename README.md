<snippet>
  <content>
#py-sacred-doorway 

Py-Sacred-Doorway brings SimpleCV (light detection) control to The Sacred Doorway using a Raspberry Pi 2, Raspicam, and fadecandy.

The application is built around python multiprocessing and utilizes two processes: one to routinely collect images from the camera and another to process them and render state to the fadecandys. Normally it would be connected to "the doorway" but because it uses Fadecandy to render state to the LEDs you can run it against the facecandy OPC server and render that way. 

The playground contains some examples of using it with a KinectV1 (my original intent) as well as some examples of switching out the primary camera instance for a webcam.

[Videos of Development Progress](https://www.youtube.com/playlist?list=PLGxNYpiwnl8WbpT4YQmWQo3IXhWxgW8jh)

Previous state of the project can be seen in the history section.


## History

Mid 2013 I built a small little frame box with several acrylic sheets in it. These sheets were dremmel etched
with various geometric shapes with an arduino duemilanove controlling the fade state of 7 LEDs placed on the edge 
of the sheets. The prototype project can be seen here:

[Metatron Box](https://youtu.be/ysFEq5-h-6k)

Fast forward to early 2014 when I decided to make what would be the rather big final product: "The Sacred Doorway" 
(it's more of a window). Overall it stands 8 feet tall and is 4 feet wide. 7 8'x4' acrylic sheets are placed within
the frame with WS2812 NeoPixel strands lining the left and right edges of the acrylic. These were controlled with an
arduino mega. Final production can be seen here (sorry for some foul language, I was excited!):

[SD 1](https://youtu.be/poWdaNr34EA)

[SD 2](https://youtu.be/1jxQJL8qlaU)

[SD 3](https://youtu.be/ZUS4uXscfkQ)

Processing sketches for 2014-state can be found here:

https://github.com/deldreth/SacredDoorway

## Credits

Everybody that helped. So many people...

## License

GPLv3

</content>
</snippet>
