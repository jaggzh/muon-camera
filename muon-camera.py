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

def pauser():
	plt.pause(0.4)
kbnb.init(cb=pauser)

iw=352
ih=288
frame = Frame('/dev/video0')
pltimg = None
plt.ion()
	#def __init__(self, dims=None, count=None, dtype=np.uint8):
imgsbuf = ImageBuf(dims=(ih,iw,3), count=5)
diffbuf = ImageBuf(dims=(ih,iw,3), count=5)
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
	if framecount > 5:
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
				print("Sum {} > thresh of {}".format(pimgsum, thresh*tmult))
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
