import numpy
import Image

from . import blends
from . import utils

class Layer:
    """ Represents a raster layer that can be combined with other layers.
    """
    def __init__(self, channels):
        """ Channels is a four-element list of numpy arrays: red, green, blue, alpha.
        """
        self._rgba = channels

    def size(self):
        return self._rgba[0].shape
    
    def rgba(self, width, height):
        """
        """
        w, h = self.size()
        
        if w == width and h == height:
            return self._rgba

        #
        # In theory, this should bring back a right-sized image.
        #
        r, g, b, a = [numpy.zeros((width, height), dtype=float) for i in '1234']

        w = min(w, width)
        h = min(h, height)
        
        r[:w,:h] = self._rgba[0]
        g[:w,:h] = self._rgba[1]
        b[:w,:h] = self._rgba[2]
        a[:w,:h] = self._rgba[3]
        
        return r, g, b, a
    
    def image(self):
        """
        """
        return utils.rgba2img(self._rgba)
    
    def blend(self, other, mask=None, opacity=1, mode=None):
        """ Return a new Layer, with data from another layer blended on top.
        """
        #
        # Choose an output size based on the first input that has one.
        #
        if self.size():
            dim = self.size()
        elif other.size():
            dim = other.size()
        elif mask and mask.size():
            dim = mask.size()
        else:
            dim = 1, 1
        
        bottom_rgba = self.rgba(*dim)
        alpha_chan = other.rgba(*dim)[3]
        top_rgb = other.rgba(*dim)[0:3]
        
        if mask is not None:
            #
            # Use the RGB information from the supplied mask,
            # but convert it to a single channel as in YUV:
            # http://en.wikipedia.org/wiki/YUV#Conversion_to.2Ffrom_RGB
            #
            mask_r, mask_g, mask_b = mask.rgba(*dim)[0:3]
            mask_lum = 0.299 * mask_r + 0.587 * mask_g + 0.114 * mask_b
            alpha_chan *= mask_lum
        
        output_rgba = blends.combine(bottom_rgba, top_rgb, alpha_chan, opacity, mode)
        
        return Layer(output_rgba)

class Bitmap (Layer):
    """ Raster layer instantiated with a bitmap image.
    """
    def __init__(self, input):
        """ Input is a PIL Image or file name.
        """
        if type(input) in (str, unicode):
            input = Image.open(input)
        
        self._rgba = utils.img2rgba(input)

class Color (Layer):
    """
    """
    def __init__(self, red, green, blue, alpha=0xFF):
        self._components = red / 255., green / 255., blue / 255., alpha / 255.
    
    def size(self):
        return None
    
    def rgba(self, width, height):
        """
        """
        r = numpy.ones((width, height)) * self._components[0]
        g = numpy.ones((width, height)) * self._components[1]
        b = numpy.ones((width, height)) * self._components[2]
        a = numpy.ones((width, height)) * self._components[3]
        
        return r, g, b, a
