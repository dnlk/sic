from PIL import Image

def load_image(filename):
    im = Image.open(filename)
    pixels = list(im.getdata())
    width, height = im.size
    return width, height, pixels



#This file include methods that prepares the RGB image pixels arrays to be 
#fed into the inverse FFT processor

class SamplingOptions:

	RED = 		'red'
	GREEN = 	'green'
	BLUE = 		'blue'
	GREYSCALE = 'greyscale'



def pixel_sampler( width, height, data, sample_option ):
	print "lala"
	result = []

	for x in data:
		print x

	for x in data:
		pixel = ( 0, 0 )
		if sample_option == 'red':
			#RED
			pixel = ( x[0], x[0] )

		elif sample_option == 'green':
			#GREEN
			pixel = ( x[1], x[1] )

		elif sample_option == 'blue':
			#RED
			pixel = ( x[2], x[2] )

		elif sample_option == 'greyscale':
			#greyscale
			greyscale = 0.2126 * x[0] + 0.7152 * x[1] + 0.0722 * x[2]
			pixel = ( greyscale, greyscale )

		result.append( pixel )

	print( "finished sampling \n")
	for x in result:
		print( x )

	return 
