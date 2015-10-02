	try:
		from PIL import Image
	except ImportError:
		import Image

	try:
		from cStringIO import StringIO
	except ImportError:
		from StringIO import StringIO

	
	class ImageConvert(object):
		
		def _png_to_jpeg(image):
			bg = Image.new('RGBA', image.size, (255, 255, 255))
			bg.paste(image, image)
			image = bg.convert('RGB')
			return image
			
		def _gif_to_jpeg(image):
			image = self._gif_to_png(image)
			image = self._png_to_jpeg(image)
			return image
			
		def _gif_to_png(image):
			im = Image.new('RGBA', image.size)
			im.paste(image)
			return im
		
		@classmethod
		def convert(image):
			if image.format == 'PNG' and image.mode == 'RGBA':
				image = self._png_to_jpeg(image)
			elif image.format == 'GIF':
				image = self._gif_to_jpeg(image)
        	elif image.mode != 'RGB':
        		image = image.convert('RGB')
        	return image		

	if __name__ == "__main__":
		image = Image.open()
		buf = StringIO()
		
		jpeg = ImageConvert.convert(image)
		jpeg.save(buf, 'JPEG')
	
		buf.getvalues()