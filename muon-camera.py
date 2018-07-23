#!/usr/bin/python3
from pyv4l2.frame import Frame
from pyv4l2.control import Control
import ipdb as pdb
from math import *
import numpy as np
from PIL import Image
import PIL
import matplotlib.pyplot as plt
import kbnb
from imgbuf import *

# User settings

iw=352
ih=288
vdev="/dev/video0"

# Code:
#  Touch me and you'll understand what happiness is.
#  Look, a new day has begun.
#    - "Memory", Cats

def pauser():
	plt.pause(0.1) # My cheap camera fails sometimes. This slower
	               # framerate seems to help.
kbnb.init(cb=pauser)

print('''
* Please make sure to set your camera resolution
  in muon-camera.py
* Also, set your video device (default /dev/video0)
* Hit h and l to adjust the threshold multiplier
  (Lower (h) gives more frequent updates
* While it waits for some initial frames, it otherwise
  begins right away, so it doesn't have a proper average for the
  brightness peaks. The end result is you get some images
  showing quickly, then they should reduce in frequency.
''')
avg_over=5 # Number of frames for averaging, to remove noise.
           # This same count is used for figuring out the
		   # threshold of peak brightness. (I currently keep
		   # those entire images, but I could just keep their
		   # sums for detecting peaks. Should fix that later.)


frame = Frame(vdev)
pltimg = None
plt.ion()
	#def __init__(self, dims=None, count=None, dtype=np.uint8):
imgsbuf = ImageBuf(dims=(ih,iw,3), count=avg_over)
diffbuf = ImageBuf(dims=(ih,iw,3), count=avg_over)
framecount=0
anomalycount=0
#thresh = 217000
tmult = 1.15
while True:
	imgd = frame.get_frame()
	framecount += 1
	img = np.frombuffer(imgd, dtype=np.uint8)
	img = img.reshape((ih,iw,3))
	imgsbuf.add(img)
	if framecount > avg_over:
		if pltimg is None:
			pltimg = plt.imshow(img, vmin=0, vmax=255)
			#pltimg = plt.imshow(imgsbuf.avg(), vmin=0, vmax=255)
			plt.show()
		else:
			pimg = img.astype(np.float64)
			pimg -= imgsbuf.avg()
			pimg = np.clip(pimg, 0, 255)
			diffbuf.add(pimg)
			pimgsum = pimg.sum()
			thresh = diffbuf.avg().sum()
			#print("Sum={}, Thresh={}, TMult={}".format(pimgsum, thresh, thresh*tmult))
			if pimgsum > thresh*tmult:
				anomalycount += 1
				print("Sum {:.2f} > thresh of {:.2f}".format(\
					pimgsum, thresh*tmult))
				#pltimg.set_data(pimg)
				pimg = (255*(pimg/pimg.max())).astype(np.uint8)
				pltimg.set_data(pimg)
				plt.draw()
	pauser()
	#pltimg.set_data(imgsbuf.avg())
	#pltimg.norm.vmin = 0
	#pltimg.norm.vmax = 255
	#plt.draw()
	#pauser()
	#if framecount > 20: pdb.set_trace()
	#ch = kbnb.waitch("Any key to continue. q to quit: ")
	ch = kbnb.getch()
	#print("Ch: ", ch)
	if ch == b'q':
		break
	elif ch == b'h':
		tmult -= .01; print("Thresh now:", tmult)
	elif ch == b'l':
		tmult += .01; print("Thresh now:", tmult)
frame.close()
kbnb.reset_flags()

#pdb.set_trace()
#control = Control("/dev/video0")
#control.get_controls()
# control.get_control_value(9963776)
# control.set_control_value(9963776, 8)
