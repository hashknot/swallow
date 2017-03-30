"""
Defines image filter classes.
"""
from PIL import Image

class BaseFilter(object):
    def __init__(*args, **kwargs):
        pass

    def apply(self, path):
        """
        Apply the filter on image located at `path`.
        """
        raise NotImplementedError

class BrightnessFilter(BaseFilter):
    """
    Control the brightness of the image.
    """
    def __init__(self, value=0.3, *args, **kwargs):
        self._value = value

    def apply(self, path):
        image = Image.open(path)
        image.point(lambda x: x*self._value).save(path)
