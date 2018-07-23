Script to monitor usb camera for muon events.

Currently in testing, it just looks for peaks in brightness, above the average brightness * a threshold multiplier.

The paper (see references below) says it's possible. This is the idea, from them:
![CMOS cosmic event diagram](imgref/pdf-diag.png)

They get results like this:
![CMOS cosmic event result](imgref/pdf-result.png)

I'm using my worst camera currently, and get mostly noise. Even the bright specks in the image are likely noise.  I'll update when I switch to a higher quality camera.
![CMOS noise, with maybe-special dots](imgref/local-result.png)

Run muon-camera.py.
Hit h and l to decrease/increase the threshold.

Note: It normalizes images, so very dark noisy images will show their noise.

References:
http://via.library.depaul.edu/cgi/viewcontent.cgi?article=1021&context=ahac
"Detecting cosmic rays using CMOS sensors in consumer devices"

