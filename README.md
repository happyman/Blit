Blit
====

Simple pixel-composition library for Python.

Blit can combine images and colors using different image blend modes, inspired
by the layers palette in GIMP or Adobe Photoshop. You can create a layer from
an image or color, and add new layers on top of it with a combination of opacity
(0 - 1), mask image, and blend mode.

    >>> from Blit import Bitmap, adjustments
    >>> photo = Bitmap('photo.jpg')
    >>> sepia = adjustments.curves2([(0, 64), (128, 158), (255, 255)], [(0, 23), (128, 140), (255, 255)], [(0, 0), (128, 98), (255, 194)])
    >>> oldphoto = photo.adjust(sepia)
    
    >>> from Blit import Color
    >>> purple = Color(50, 0, 100)
    >>> orange = Color(255, 220, 180)
    >>> duotone = purple.blend(orange, mask=photo)
