import numpy as np

class ImageBuf():
	def __init__(self, dims=None, count=None, dtype=np.float64):
		self._dims = dims
		self._count = count
		self._imgs = np.zeros((count,)+dims, dtype=dtype)
		self._next = 0
	def add(self, img):
		self._imgs[self._next] = img
		self._next += 1
		if self._next >= self._count:
			self._next = 0
	def avg(self):
		return np.average(self._imgs, axis=0) #.astype(np.uint8)
