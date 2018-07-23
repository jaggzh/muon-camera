Script to monitor usb camera for muon events.

Currently in testing, it just looks for peaks in brightness, above the average brightness * a threshold multiplier.

Run muon-camera.py.
Hit h and l to decrease/increase the threshold.

Note: It normalizes images, so very dark noisy images will show their noise.

References:
http://via.library.depaul.edu/cgi/viewcontent.cgi?article=1021&context=ahac
"Detecting cosmic rays using CMOS sensors in consumer devices"
