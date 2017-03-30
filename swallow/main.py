#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from wallpaper import BingWallpaperOTD
from quote import BookReporterQuoteOTD
from filter import BrightnessFilter
from textOverlay import TextOverlayEngine

def main():
    filepath = sys.argv[1]
    quote, attribution = BookReporterQuoteOTD().get()
    BingWallpaperOTD().download(filepath)
    BrightnessFilter().apply(filepath)
    TextOverlayEngine().overlay(filepath, quote, attribution)

if __name__ == '__main__':
    main()
