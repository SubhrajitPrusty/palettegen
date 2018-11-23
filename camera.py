from PIL import Image, ImageDraw
import cv2
import numpy as np

class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)


	def __del__(self):
		self.video.release()


	def getFrame(self):
		ret, frame = self.video.read()

		# convert to RGB
		rgbimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img = Image.fromarray(rgbimg)

		# make into a palette
		pal = img.convert('P', palette=Image.ADAPTIVE, colors=6)
		pal.putalpha(0)

		# get the colors
		colors = pal.getcolors(16*10**5)
		colors = [c[1][:3] for c in colors]

		colors = sorted(colors)

		palheight = int(img.height*0.1)
		palwidth = img.width

		# create the palette image
		palimg = Image.new("RGB", (palwidth, palheight), "#000000")

		draw = ImageDraw.Draw(palimg)
		x = y = 0
		shift = palwidth//len(colors)
		for c in colors:
			draw.rectangle([x,y, x+shift, y+palheight], fill=c)
			x+= shift
		
		# merge both images
		newimg = Image.new("RGB", (img.width, img.height+palheight), "#000000")
		newimg.paste(img, (0,0))
		newimg.paste(palimg, (0, img.height))

		# convert back to BGR
		cimg = cv2.cvtColor(np.array(newimg), cv2.COLOR_RGB2BGR)
		ret, jpeg = cv2.imencode('.jpg', cimg)

		return jpeg.tobytes()