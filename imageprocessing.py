from PIL import Image

def LoadImage( filename ):
    im = Image.open( filename )

    pixels = list(im.getdata())
    width, height = im.size

    return ( width, height, pixels )