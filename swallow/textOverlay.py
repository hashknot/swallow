"""
Implements image text overlay
"""
import math
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

FONTS = [
    'amiri-regular',
    'Caladea-Regular',
    'DejaVuSerif',
    'EBGaramond12-Italic',
    'EBGaramond-InitialsF1',
    'EBGaramond-InitialsF2',
    'FreeSerif',
    'GenBkBasR',
    'Gentium-R',
    'GenBasR',
    'GenBkBasR',
    'GentiumAlt-R',
    'Georgia',
    'ipamp',
    'ipaexm',
    'ipam',
    'Junicode',
    'LiberationSerif-Regular',
    'Times_New_Roman',
    'ume-pmo3',
    'UnBatang',
    'UnGungseo',
]

class FontConfig(object):
    def __init__(self, name=None, minSize=18, maxSize=22,
                 color=(200, 200, 200), linespace=4):
        self.name = name if name else random.choice(FONTS)
        self.minSize = minSize
        self.maxSize = maxSize
        self.color = color
        self.linespace = linespace

class TextOverlayEngine(object):

    def __init__(self, fontConfig=None):
        self._fontConfig = fontConfig if fontConfig else FontConfig()

    def _getLargestFontSizeFit(self, text, width, low=None, high=None):
        """
        Get highest font size that can be fit within 'width' image for the
        given 'text'.
        'low' and 'high' support recursion.
        """
        low = low if low is not None else self._fontConfig.minSize
        high = high if high is not None else self._fontConfig.maxSize

        if low >= high:
            raise RuntimeError

        mid = (low + high)//2
        font = ImageFont.truetype(self._fontConfig.name, size=mid)
        if font.getsize(text)[0] <= width:
            try:
                return self._getLargestFontSizeFit(text, width, mid+1, high)
            except RuntimeError:
                return mid
        return self._getLargestFontSizeFit(text, width, low, mid-1)

    def overlay(self, path, quote, attribution=None, width=1000):
        image = Image.open(path)
        draw = ImageDraw.Draw(image)

        imageWidth, imageHeight = image.size
        width = min(width, imageWidth)

        lines, fontSize = self._getTextFit(quote, width)
        lines.append(' ')
        lines.append(u' \u2014 {}'.format(attribution))

        font = ImageFont.truetype(self._fontConfig.name, fontSize)
        fontHeight = font.getsize(' ')[1]
        textHeight = len(lines)*fontHeight + \
                         (len(lines) - 1)*self._fontConfig.linespace
        textY = (imageHeight - textHeight)//2
        lineY = textY
        for line in lines:
            lineImg = self._getRasterizedText(line, font)
            lineW, lineH = lineImg.size
            lineX = (imageWidth-lineW)//2
            image.paste(lineImg, (lineX, lineY), lineImg)
            lineY += lineH + self._fontConfig.linespace
        image.save(path)

    def _getRasterizedText(self, text, font):
        textW, textH = font.getsize(text)
        scaledFont = ImageFont.truetype(font.path, font.size*2)
        textImg = Image.new('RGBA', (scaledFont.getsize(text)))
        textDraw = ImageDraw.Draw(textImg)
        textDraw.text((0, 0), text, self._fontConfig.color, font=scaledFont)
        textImg = textImg.resize((textW, textH), Image.ANTIALIAS)
        return textImg

    def _getTextFit(self, text, width):
        nSplits = 1
        lines = text.splitlines()
        if len(lines) > 1:
            # We do not want to split the existing lines, so treat them as words.
            words = lines
        else:
            words = text.split()

        while True:
            try:
                splitLen = int(math.ceil(float(len(words))/nSplits))
                lines = [' '.join(words[i:i + splitLen])
                         for i in xrange(0, len(words), splitLen)]
                size = min((self._getLargestFontSizeFit(l, width) for l in lines))
                return lines, size
            except RuntimeError:
                nSplits += 1
                if nSplits > len(words):
                    raise
